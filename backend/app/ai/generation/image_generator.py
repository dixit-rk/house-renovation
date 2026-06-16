import os
import threading
from pathlib import Path

import torch
from diffusers import AutoPipelineForImage2Image
from PIL import Image

from app.core.config import settings

# The pipeline is heavy (~3-4 GB in RAM) and slow to load, so we build it once
# per worker process and reuse it across tasks. Guarded by a lock because Celery
# prefork workers are single-process but the FastAPI dev server may be threaded.
_pipe = None
_lock = threading.Lock()


def _get_pipeline():
    global _pipe
    if _pipe is not None:
        return _pipe
    with _lock:
        if _pipe is None:
            threads = int(os.getenv("IMAGE_NUM_THREADS", "0"))
            if threads > 0:
                torch.set_num_threads(threads)
            # Download the fp16 weight files (smaller on disk) but run in fp32,
            # which is what CPU inference needs. Fall back to full-precision
            # weights if the model has no fp16 variant published.
            try:
                pipe = AutoPipelineForImage2Image.from_pretrained(
                    settings.HF_IMAGE_MODEL,
                    torch_dtype=torch.float32,
                    variant="fp16",
                    safety_checker=None,
                    requires_safety_checker=False,
                )
            except Exception:
                pipe = AutoPipelineForImage2Image.from_pretrained(
                    settings.HF_IMAGE_MODEL,
                    torch_dtype=torch.float32,
                    safety_checker=None,
                    requires_safety_checker=False,
                )
            pipe.to("cpu")
            pipe.set_progress_bar_config(disable=True)
            _pipe = pipe
    return _pipe


def _prepare_image(path: str, target: int) -> Image.Image:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    scale = target / max(w, h)
    nw = max(8, int(w * scale) - (int(w * scale) % 8))
    nh = max(8, int(h * scale) - (int(h * scale) % 8))
    return img.resize((nw, nh), Image.LANCZOS)


def generate_image(image_path: str, prompt: str, output_path: str) -> str:
    pipe = _get_pipeline()
    init_image = _prepare_image(image_path, settings.IMAGE_MAX_SIZE)

    full_prompt = (
        f"{prompt}, photorealistic exterior of a residential house, "
        "preserve the original building structure and layout, "
        "realistic materials and lighting, high quality"
    )

    # SD-Turbo: classifier-free guidance disabled (guidance_scale=0) and a low
    # step count. Effective denoising steps = round(num_inference_steps * strength),
    # so keep strength high enough that at least 1-2 steps actually run.
    result = pipe(
        prompt=full_prompt,
        image=init_image,
        num_inference_steps=settings.IMAGE_STEPS,
        strength=settings.IMAGE_STRENGTH,
        guidance_scale=0.0,
    ).images[0]

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.save(out)
    return str(out)
