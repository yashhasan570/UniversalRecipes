from pydantic import ConfigDict

from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class RecipeSettings(UniversalRecipesModel):
    public: bool = False
    show_nutrition: bool = False
    show_assets: bool = False
    landscape_view: bool = False
    disable_comments: bool = True
    locked: bool = False
    model_config = ConfigDict(from_attributes=True)
