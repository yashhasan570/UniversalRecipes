from uuid import UUID

from pydantic import ConfigDict

from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel


class InviteTokenCreate(UniversalRecipesModel):
    uses: int
    group_id: UUID | None = None
    household_id: UUID | None = None


class InviteTokenSave(UniversalRecipesModel):
    uses_left: int
    group_id: UUID
    household_id: UUID
    token: str


class InviteTokenOut(UniversalRecipesOutModel):
    token: str
    uses_left: int
    group_id: UUID
    household_id: UUID
    model_config = ConfigDict(from_attributes=True)


class EmailInvitation(UniversalRecipesModel):
    email: str
    token: str


class EmailInvitationResponse(UniversalRecipesModel):
    success: bool
    error: str | None = None
