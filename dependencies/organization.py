from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.roles import OrganizationRole
from database.session import get_db
from dependencies.auth import get_current_user

from models.user import User
from models.organization import Organization, OrganizationMember


def _get_membership(
    organization_id: int,
    db: Session,
    current_user: User,
) -> tuple[Organization, OrganizationMember]:

    organization = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    membership = (
        db.query(OrganizationMember)
        .filter(
            OrganizationMember.organization_id == organization_id,
            OrganizationMember.user_id == current_user.id,
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    return organization, membership



def require_member(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:

    organization, _ = _get_membership(
        organization_id,
        db,
        current_user,
    )

    return organization

def require_admin(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:

    organization, membership = _get_membership(
        organization_id,
        db,
        current_user,
    )

    if membership.role not in (OrganizationRole.OWNER,OrganizationRole.ADMIN,):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return organization

def require_owner(
    organization_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Organization:

    organization, membership = _get_membership(
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