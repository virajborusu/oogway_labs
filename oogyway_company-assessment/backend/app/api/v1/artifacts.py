from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Session, Artifact
from app.schemas.artifact import ArtifactCreate, ArtifactResponse
from app.services.artifacts.sanitizer import sanitize_html

router = APIRouter()


@router.post("/sessions/{session_id}/artifacts", response_model=ArtifactResponse, status_code=status.HTTP_201_CREATED)
async def create_artifact(
    session_id: str,
    art_in: ArtifactCreate,
    db: AsyncSession = Depends(get_db)
):
    """Manually create an artifact associated with a session."""
    res_session = await db.execute(select(Session).where(Session.id == session_id))
    session_obj = res_session.scalar_one_or_none()

    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "SESSION_NOT_FOUND", "message": f"Session ID '{session_id}' does not exist."}}
        )

    sanitized = sanitize_html(art_in.content) if art_in.artifact_type == "html" else art_in.content

    artifact = Artifact(
        session_id=session_id,
        title=art_in.title,
        artifact_type=art_in.artifact_type,
        content=art_in.content,
        sanitized_content=sanitized
    )
    db.add(artifact)
    await db.commit()
    await db.refresh(artifact)

    return ArtifactResponse.model_validate(artifact)


@router.get("/sessions/{session_id}/artifacts", response_model=List[ArtifactResponse])
async def list_session_artifacts(session_id: str, db: AsyncSession = Depends(get_db)):
    """List all generated artifacts for a session."""
    res = await db.execute(
        select(Artifact)
        .where(Artifact.session_id == session_id)
        .order_by(Artifact.created_at.desc())
    )
    artifacts = res.scalars().all()
    return [ArtifactResponse.model_validate(a) for a in artifacts]


@router.get("/artifacts/{artifact_id}", response_model=ArtifactResponse)
async def get_artifact(artifact_id: str, db: AsyncSession = Depends(get_db)):
    """Fetch details of a single artifact by artifact_id."""
    res = await db.execute(select(Artifact).where(Artifact.id == artifact_id))
    artifact = res.scalar_one_or_none()

    if not artifact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "ARTIFACT_NOT_FOUND", "message": f"Artifact ID '{artifact_id}' does not exist."}}
        )

    return ArtifactResponse.model_validate(artifact)
