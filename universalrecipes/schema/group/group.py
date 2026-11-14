from pydantic import UUID4

from universalrecipes.schema._universalrecipes import UniversalRecipesModel

from .ai_providers import AIProviderSettingsUpdate
from .group_preferences import GroupPreferencesUpdate


class GroupAdminUpdate(UniversalRecipesModel):
    id: UUID4
    name: str
    preferences: GroupPreferencesUpdate | None = None
    ai_provider_settings: AIProviderSettingsUpdate | None = None
