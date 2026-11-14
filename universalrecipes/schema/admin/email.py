from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class EmailReady(UniversalRecipesModel):
    ready: bool


class EmailSuccess(UniversalRecipesModel):
    success: bool
    error: str | None = None


class EmailTest(UniversalRecipesModel):
    email: str
