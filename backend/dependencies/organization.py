from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from database.session import get_db
from dependencies.auth import get_current_user
from models.chatbot import Chatbot
from models.knowledge_base import KnowledgeBase
from models.organization import Organization
from models.organization_member import OrganizationMember
from models.user import User


async def _get_membership(
    organization_id: int,
    db: AsyncSession,
    current_user: User,
) -> tuple[Organization, OrganizationMember]:
    organization_result = await db.execute(
        select(Organization).where(
            Organization.id == organization_id
        )
    )

    organization = organization_result.scalar_one_or_none()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    membership_result = await db.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == current_user.id,
        )
    )

    membership = membership_result.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    return organization, membership


async def require_member(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:
    organization, _ = await _get_membership(
        organization_id,
        db,
        current_user,
    )

    return organization


async def require_admin(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:
    organization, membership = await _get_membership(
        organization_id,
        db,
        current_user,
    )

    if membership.role not in (
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return organization


async def require_owner(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:
    organization, membership = await _get_membership(
        organization_id,
        db,
        current_user,
    )

    if membership.role != OrganizationRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner access required",
        )

    return organization


# ==========================================================
# Chatbot authorization
# ==========================================================


async def _get_chatbot_membership(
    chatbot_id: int,
    db: AsyncSession,
    current_user: User,
) -> tuple[Chatbot, Organization, OrganizationMember]:

    chatbot_result = await db.execute(
        select(Chatbot).where(
            Chatbot.id == chatbot_id
        )
    )

    chatbot = chatbot_result.scalar_one_or_none()

    if chatbot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chatbot not found.",
        )

    return (
        chatbot,
        *await _get_membership(
            chatbot.organization_id,
            db,
            current_user,
        ),
    )


async def require_chatbot_member(
    chatbot_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Chatbot:
    chatbot, _, _ = await _get_chatbot_membership(
        chatbot_id,
        db,
        current_user,
    )

    return chatbot


async def require_chatbot_admin(
    chatbot_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Chatbot:
    chatbot, _, membership = await _get_chatbot_membership(
        chatbot_id,
        db,
        current_user,
    )

    if membership.role not in (
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return chatbot


# ==========================================================
# Knowledge Base authorization
# ==========================================================


async def _get_knowledge_base_membership(
    knowledge_base_id: int,
    db: AsyncSession,
    current_user: User,
) -> tuple[
    KnowledgeBase,
    Chatbot,
    Organization,
    OrganizationMember,
]:

    kb_result = await db.execute(
        select(KnowledgeBase).where(
            KnowledgeBase.id == knowledge_base_id
        )
    )

    knowledge_base = kb_result.scalar_one_or_none()

    if knowledge_base is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge Base not found.",
        )

    chatbot, organization, membership = (
        await _get_chatbot_membership(
            knowledge_base.chatbot_id,
            db,
            current_user,
        )
    )

    return (
        knowledge_base,
        chatbot,
        organization,
        membership,
    )


async def require_knowledge_base_member(
    knowledge_base_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> KnowledgeBase:
    knowledge_base, _, _, _ = (
        await _get_knowledge_base_membership(
            knowledge_base_id,
            db,
            current_user,
        )
    )

    return knowledge_base


async def require_knowledge_base_admin(
    knowledge_base_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> KnowledgeBase:
    knowledge_base, _, _, membership = (
        await _get_knowledge_base_membership(
            knowledge_base_id,
            db,
            current_user,
        )
    )

    if membership.role not in (
        OrganizationRole.OWNER,
        OrganizationRole.ADMIN,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return knowledge_base