from pydantic import ConfigDict

from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class RecipeAsset(UniversalRecipesModel):
    name: str
    icon: str
    file_name: str | None = None
    model_config = ConfigDict(from_attributes=True)
