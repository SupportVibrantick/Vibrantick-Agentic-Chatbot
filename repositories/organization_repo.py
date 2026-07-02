from sqlalchemy.orm import Session

from models.organization import Organization, OrganizationMember


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, organization: Organization) -> Organization:
        self.db.add(organization)
        self.db.flush()
        return organization

    

    def get_by_id(self, organization_id: int) -> Organization | None:
        return (
            self.db.query(Organization)
            .filter(Organization.id == organization_id)
            .first()
        )

    def get_by_slug(self, slug: str) -> Organization | None:
        return (
            self.db.query(Organization)
            .filter(Organization.slug == slug)
            .first()
        )

    def get_user_organizations(
        self,
        user_id: int,
    ) -> list[Organization]:
        return (
            self.db.query(Organization)
            .join(OrganizationMember)
            .filter(OrganizationMember.user_id == user_id)
            .all()
        )

    def update(self, organization: Organization) -> Organization:
        self.db.commit()
        self.db.refresh(organization)
        return organization

    def delete(self, organization: Organization) -> None:
        self.db.delete(organization)
        self.db.commit()