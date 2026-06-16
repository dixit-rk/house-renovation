from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.estimation_crud import GenerationCRUD
from app.db.session import get_db
from app.schemas.task_schema import GenerationStatusResponseSchema, TaskStatusResponseSchema

router = APIRouter(prefix="/projects/{project_id}/generate", tags=["generation"])


@router.post("/")
def trigger_generation(project_id: UUID, db: Session = Depends(get_db)):
    return GenerationCRUD(db).trigger_generation(project_id)


@router.get("/status")
def get_generation_status(project_id: UUID, db: Session = Depends(get_db)):
    result = GenerationCRUD(db).get_generation_status(project_id)
    if not result["success"]:
        return result
    task = result["data"]["task"]
    return {
        "success": True,
        "msg": result["msg"],
        "data": GenerationStatusResponseSchema(
            status=result["data"]["status"],
            task=TaskStatusResponseSchema.model_validate(task) if task else None,
        ),
    }
