from pydantic import UUID4, ConfigDict

from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel


class MealPlanICalTokenOut(UniversalRecipesOutModel):
    household_id: UUID4
    mealplan_ical_token: str | None = None
    model_config = ConfigDict(from_attributes=True)
