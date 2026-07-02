from sqlalchemy.orm import Session

from models import invitation
from models.invitation import Invitation
from core.roles import InvitationStatus

class InvitationRepository:

    def __init__(self, db: Session):
        self.db = db
        
        
    def create(self, invitation: Invitation) -> Invitation:
        self.db.add(invitation)
        self.db.commit()
        self.db.refresh(invitation)
        return invitation
    
    def get_by_id(self, invitation_id: int) -> Invitation | None:
        return (
            self.db.query(Invitation)
            .filter(Invitation.id == invitation_id)
            .first()
            )
        
    def get_by_token(self, token: str) -> Invitation | None:
        return (
            self.db.query(Invitation)
            .filter(Invitation.token == token)
            .first()
            )
        
    def get_pending(
        self,
        organization_id: int,
        email: str,
        ) -> Invitation | None:
        return (
        self.db.query(Invitation)
        .filter(
            Invitation.organization_id == organization_id,
            Invitation.email == email,
            Invitation.status == InvitationStatus.PENDING,
        )
        .first()
        )
        
    def list_by_organization(
        self,
        organization_id: int,
        ) -> list[Invitation]:
        return (
        self.db.query(Invitation)
        .filter(
            Invitation.organization_id == organization_id
        )
        .order_by(Invitation.created_at.desc())
        .all()
    )
        
    def cancel(
        self,
        invitation: Invitation,
        ) -> Invitation:
        invitation.status = InvitationStatus.CANCELLED
        self.db.commit()
        self.db.refresh(invitation)
        return invitation
    
    def get_by_email(
        self,
        organization_id: int,
        email: str,
        ) -> Invitation | None:
        return (
        self.db.query(Invitation)
        .filter(
            Invitation.organization_id == organization_id,
            Invitation.email == email,
        )
        .first()
    )