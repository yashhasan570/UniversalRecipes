from uuid import UUID

from pydantic import UUID4, ConfigDict

from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel


class GroupPreferencesUpdate(UniversalRecipesModel):
    private_group: bool = True
    show_announcements: bool = True


class GroupPreferencesCreate(GroupPreferencesUpdate):
    group_id: UUID


class GroupPreferencesOut(GroupPreferencesCreate, UniversalRecipesOutModel):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)
