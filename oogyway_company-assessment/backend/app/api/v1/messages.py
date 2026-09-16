from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.db.models import Session, Message, Artifact
from app.schemas.message import MessageCreate, MessageResponse
from app.services.llm.factory import get_llm_provider
from app.services.skills.agent_router import process_user_message

router = APIRouter()


@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def list_session_messages(session_id: str, db: AsyncSession = Depends(get_db)):
    """Fetch all messages for a given session sorted chronologically."""
    res_session = await db.execute(select(Session).where(Session.id == session_id))
    session_obj = res_session.scalar_one_or_none()

    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "SESSION_NOT_FOUND", "message": f"Session ID '{session_id}' does not exist."}}
        )

    res_msgs = await db.execute(
        select(Message)
        .options(selectinload(Message.artifacts))
        .where(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
    )
    messages = res_msgs.scalars().all()

    response = []
    for m in messages:
        art_id = m.artifacts[0].id if m.artifacts else None
        response.append(
            MessageResponse(
                id=m.id,
                session_id=m.session_id,
                role=m.role,
                content=m.content,
                sources=m.sources,
                created_at=m.created_at,
                meta_info=m.meta_info,
                artifact_id=art_id
            )
        )
    return response


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def post_message(
    session_id: str,
    msg_in: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    """Post a user message to a session, execute agent routing/retrieval, and return assistant response."""
    res_session = await db.execute(
        select(Session)
        .options(selectinload(Session.messages))
        .where(Session.id == session_id)
    )
    session_obj = res_session.scalar_one_or_none()

    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "SESSION_NOT_FOUND", "message": f"Session ID '{session_id}' does not exist."}}
        )

    # Auto-generate title for first user message if default
    if len(session_obj.messages) == 0 and session_obj.title == "New Growth Conversation":
        new_title = msg_in.content.strip()[:40] + ("..." if len(msg_in.content) > 40 else "")
        session_obj.title = new_title

    # Save user message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=msg_in.content
    )
    db.add(user_msg)
    await db.flush()

    # Build conversation history for session context
    history = [
        {"role": m.role, "content": m.content}
        for m in session_obj.messages
    ]

    llm = get_llm_provider()

    # Agent processing
    assistant_content, sources, artifact_obj = await process_user_message(
        session_id=session_id,
        user_content=msg_in.content,
        db=db,
        llm=llm,
        conversation_history=history,
        skill_override=msg_in.skill_override
    )

    # Save assistant message
    assistant_msg = Message(
        session_id=session_id,
        role="assistant",
        content=assistant_content,
        sources=sources,
        meta_info={"provider": llm.provider_name, "model": llm.model_name}
    )
    db.add(assistant_msg)

    if artifact_obj:
        artifact_obj.message_id = assistant_msg.id

    from datetime import datetime
    session_obj.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(assistant_msg)

    artifact_id = artifact_obj.id if artifact_obj else None

    return MessageResponse(
        id=assistant_msg.id,
        session_id=session_id,
        role=assistant_msg.role,
        content=assistant_msg.content,
        sources=sources,
        created_at=assistant_msg.created_at,
        meta_info=assistant_msg.meta_info,
        artifact_id=artifact_id
    )
