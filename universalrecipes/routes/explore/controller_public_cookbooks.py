from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from universalrecipes.repos.public_visibility import is_cookbook_publicly_visible, public_cookbooks_clause
from universalrecipes.routes._base import controller
from universalrecipes.routes._base.base_controllers import BasePublicHouseholdExploreController
from universalrecipes.schema.cookbook.cookbook import CookBookOut
from universalrecipes.schema.make_dependable import make_dependable
from universalrecipes.schema.response.pagination import PaginationBase, PaginationQuery

router = APIRouter(prefix="/cookbooks")


@controller(router)
class PublicCookbooksController(BasePublicHouseholdExploreController):
    @property
    def cross_household_cookbooks(self):
        return self.cross_household_repos.cookbooks

    @router.get("", response_model=PaginationBase[CookBookOut])
    def get_all(
        self,
        q: PaginationQuery = Depends(make_dependable(PaginationQuery)),
        search: str | None = None,
    ) -> PaginationBase[CookBookOut]:
        response = self.cross_household_cookbooks.page_all(
            pagination=q,
            override=CookBookOut,
            search=search,
            extra_filter=public_cookbooks_clause(),
        )

        response.set_pagination_guides(self.get_explore_url_path(router.url_path_for("get_all")), q.model_dump())
        return response

    @router.get("/{item_id}", response_model=CookBookOut)
    def get_one(self, item_id: UUID4 | str) -> CookBookOut:
        NOT_FOUND_EXCEPTION = HTTPException(404, "cookbook not found")
        if isinstance(item_id, UUID):
            match_attr = "id"
        else:
            try:
                UUID(item_id)
                match_attr = "id"
            except ValueError:
                match_attr = "slug"
        cookbook = self.cross_household_cookbooks.get_one(item_id, match_attr)

        household = cookbook and self.repos.households.get_one(cookbook.household_id)
        if not is_cookbook_publicly_visible(cookbook, household):
            raise NOT_FOUND_EXCEPTION

        return cookbook
