from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesModel
from universalrecipes.schema.recipe.recipe import RecipeSummary
from universalrecipes.schema.recipe.recipe_ingredient import IngredientFoodOut, IngredientFoodSummary
from universalrecipes.schema.response.pagination import RequestQuery

from .recipe_organizers import ToolOut


class RecipeSuggestionQuery(RequestQuery):
    limit: int = 10

    max_missing_foods: int = 5
    max_missing_tools: int = 5

    include_foods_on_hand: bool = True
    include_tools_on_hand: bool = True
    include_substitutions: bool = True


class RecipeSuggestionSubstitutedFood(UniversalRecipesModel):
    """A food the recipe calls for that the user doesn't have, and the one covering it."""

    food: IngredientFoodOut
    substitute_food: IngredientFoodSummary


class RecipeSuggestionResponseItem(UniversalRecipesModel):
    recipe: RecipeSummary
    missing_foods: list[IngredientFoodOut]
    substituted_foods: list[RecipeSuggestionSubstitutedFood]
    missing_tools: list[ToolOut]


class RecipeSuggestionResponse(UniversalRecipesModel):
    items: list[RecipeSuggestionResponseItem]
