from pydantic import UUID4

from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class SetPermissions(UniversalRecipesModel):
    user_id: UUID4
    can_manage_household: bool = False
    can_manage: bool = False
    can_invite: bool = False
    can_organize: bool = False
