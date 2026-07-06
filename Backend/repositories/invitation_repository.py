from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from models.invitation import Invitation

from core.roles import InvitationStatus

class InvitationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db
        
        
    async def create(
        self,
        invitation: Invitation,
    ) -> Invitation:
        self.db.add(invitation)

        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation
  
    async def get_by_id(
        self,
        invitation_id: int,
    ) ->  Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.id == invitation_id
                )
            )
        return result.scalar_one_or_none()
        
    async def get_by_token(
        self,
        token: str,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.token == token
            )
        )
        return result.scalar_one_or_none()
        
    async def get_pending(
        self,
        organization_id: int,
        email: str,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.organization_id == organization_id,
                Invitation.email == email,
                Invitation.status == InvitationStatus.PENDING,
            )
        )
        return result.scalar_one_or_none()
    async def list_by_organization(
        self,
        organization_id: int,
    ) -> list[Invitation]:
        result = await self.db.execute(
            select(Invitation)
            .where(
                Invitation.organization_id == organization_id
            )
            .order_by(Invitation.created_at.desc())
        )
        return list(result.scalars().all())
        
    async def cancel(
        self,
        invitation: Invitation,
    ) -> Invitation:
        invitation.status = InvitationStatus.CANCELLED
        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation
    
    async def get_by_email(
        self,
        organization_id: int,
        email: str,
    ) -> Invitation | None:
        result = await self.db.execute(
            select(Invitation).where(
                Invitation.organization_id == organization_id,
                Invitation.email == email,
            )
        )
        return result.scalar_one_or_none()
    
    async def update(
        self,
        invitation: Invitation,
    ) -> Invitation:
        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation