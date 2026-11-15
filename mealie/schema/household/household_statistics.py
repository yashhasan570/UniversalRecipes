from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesModel


class HouseholdStatistics(UniversalRecipesModel):
    total_recipes: int
    total_users: int
    total_categories: int
    total_tags: int
    total_tools: int
