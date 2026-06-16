from typing import Any

from app.ai.groq_client import call_groq_with_image


def suggest_materials(image_path: str) -> dict[str, Any]:
    prompt = """Analyze this house exterior and recommend renovation materials per structural zone.

Available material IDs:
- exterior_paint_smooth (paint)
- texture_finish_sand (texture)
- terracotta_brick_cladding (cladding)
- vitrified_tiles_exterior (tile)
- glass_railing (railing)
- metal_railing (railing)
- stone_cladding (cladding)
- aluminium_composite_panel (panel)

Return JSON only with this exact structure:
{
  "suggestions": [
    {
      "zone_key": "upper_wall",
      "recommended_material_ids": ["exterior_paint_smooth"],
      "reason": "brief reason"
    }
  ],
  "overall_style": "modern" or "traditional" or "contemporary"
}

Return ONLY valid JSON. No markdown. No explanation. No extra text."""

    return call_groq_with_image(image_path, prompt)
