from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.session import get_db
from dependencies.auth import get_current_user
from dependencies.organization import (
    require_member,
    require_owner,
)

from models.user import User
from models.organization import Organization

from schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
)

from services.organization_service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrganizationService(db)

    return service.create_organization(
        owner_id=current_user.id,
        name=data.name,
        description=data.description,
        logo=data.logo,
    )


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def get_my_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = OrganizationService(db)

    return service.get_my_organizations(current_user.id)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization: Organization = Depends(require_member),
):
    return organization


@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def update_organization(
    data: OrganizationUpdate,
    organization: Organization = Depends(require_owner),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(organization, field, value)

    return service.update_organization(organization)


@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization(
    organization: Organization = Depends(require_owner),
    db: Session = Depends(get_db),
):
    service = OrganizationService(db)

    service.delete_organization(organization)

    return None