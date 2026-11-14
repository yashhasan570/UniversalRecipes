from datetime import datetime

from pydantic import UUID4, ConfigDict

from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class GroupDataExport(UniversalRecipesModel):
    id: UUID4
    group_id: UUID4
    name: str
    filename: str
    path: str
    size: str
    expires: datetime
    model_config = ConfigDict(from_attributes=True)
