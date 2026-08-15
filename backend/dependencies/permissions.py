from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.roles import OrganizationRole
from database.session import get_db
from dependencies.auth import get_current_user
from models.organization_member import OrganizationMember
from models.user import User
from repositories.member_repository import MemberRepository
from repositories.organization_repository import OrganizationRepository


async def get_current_membership(
    organization_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OrganizationMember:
    """
    Return the authenticated user's membership within an organization.
    """

    organization_repo = OrganizationRepository(db)
    member_repo = MemberRepository(db)

    organization = await organization_repo.get_by_id(
        organization_id,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    membership = await member_repo.get_member(
        organization_id=organization_id,
        user_id=current_user.id,
    )

    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization.",
        )

    return membership


async def require_member(
    membership: OrganizationMember = Depends(get_current_membership),
) -> OrganizationMember:
    """
    Require that the current user is a member.
    """
    return membership


async def require_admin(
    membership: OrganizationMember = Depends(get_current_membership),
) -> OrganizationMember:
    """
    Require administrator access.
    """

    if membership.role not in (
        OrganizationRole.ADMIN,
        OrganizationRole.OWNER,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator permission required.",
        )

    return membership


async def require_owner(
    membership: OrganizationMember = Depends(get_current_membership),
) -> OrganizationMember:
    """
    Require owner access.
    """

    if membership.role != OrganizationRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Owner permission required.",
        )

    return membership


async def require_admin_or_owner(
    membership: OrganizationMember = Depends(get_current_membership),
) -> OrganizationMember:
    """
    Require administrator or owner access.
    """

    if membership.role not in (
        OrganizationRole.ADMIN,
        OrganizationRole.OWNER,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator or owner permission required.",
        )

    return membership