from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class DebugResponse(UniversalRecipesModel):
    success: bool
    response: str | None = None
