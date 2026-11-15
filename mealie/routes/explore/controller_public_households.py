from fastapi import APIRouter, Depends

from universalrecipes.repos.public_visibility import public_households_clause
from universalrecipes.routes._base import controller
from universalrecipes.routes._base.base_controllers import BasePublicGroupExploreController
from universalrecipes.schema.household.household import HouseholdSummary
from universalrecipes.schema.make_dependable import make_dependable
from universalrecipes.schema.response.pagination import PaginationBase, PaginationQuery

router = APIRouter(prefix="/households")


@controller(router)
class PublicHouseholdsController(BasePublicGroupExploreController):
    @property
    def households(self):
        return self.repos.households

    @router.get("", response_model=PaginationBase[HouseholdSummary])
    def get_all(
        self, q: PaginationQuery = Depends(make_dependable(PaginationQuery))
    ) -> PaginationBase[HouseholdSummary]:
        response = self.households.page_all(
            pagination=q, override=HouseholdSummary, extra_filter=public_households_clause()
        )
        response.set_pagination_guides(self.get_explore_url_path(router.url_path_for("get_all")), q.model_dump())
        return response

    @router.get("/{household_slug}", response_model=HouseholdSummary)
    def get_household(self, household_slug: str) -> HouseholdSummary:
        household = self.get_public_household(household_slug)
        return household.cast(HouseholdSummary)
