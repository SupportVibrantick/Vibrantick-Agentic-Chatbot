from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from database.session import get_db
from dependencies.auth import get_current_user
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