import enum

from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema.recipe.recipe_settings import RecipeSettings

from .recipe_organizers import CategoryDraft, TagDraft


class ExportTypes(enum.StrEnum):
    JSON = "json"


class ExportBase(UniversalRecipesModel):
    recipes: list[str]


class ExportRecipes(ExportBase):
    export_type: ExportTypes = ExportTypes.JSON


class AssignCategories(ExportBase):
    categories: list[CategoryDraft]


class AssignTags(ExportBase):
    tags: list[TagDraft]


class AssignSettings(ExportBase):
    settings: RecipeSettings


class DeleteRecipes(ExportBase):
    pass
