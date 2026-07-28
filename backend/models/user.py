from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.base import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,                 
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    organizations = relationship(
        "Organization",
        foreign_keys="Organization.owner_id",
        back_populates="owner",
    )

    organization_memberships = relationship(
        "OrganizationMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    created_chatbots = relationship(
        "Chatbot",
        foreign_keys="Chatbot.created_by",
        back_populates="creator",
        cascade="all, delete-orphan",
    )