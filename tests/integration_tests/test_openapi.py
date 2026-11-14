from fastapi.testclient import TestClient

from universalrecipes.schema.household.household import HouseholdRecipeSummary
from universalrecipes.schema.recipe.recipe import RecipeOut, RecipeSummary


def test_openapi_returns_json(api_client: TestClient):
    response = api_client.get("openapi.json")
    assert response.status_code == 200


def test_last_made_is_only_exposed_on_household_recipes():
    assert "last_made" not in RecipeOut.model_fields
    assert "last_made" not in RecipeSummary.model_fields
    assert "last_made" in HouseholdRecipeSummary.model_fields


def test_last_made_update_route_remains_available(api_client: TestClient):
    response = api_client.get("openapi.json")
    assert "/api/recipes/{slug}/last-made" in response.json()["paths"]
