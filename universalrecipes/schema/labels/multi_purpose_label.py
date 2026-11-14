from __future__ import annotations

from typing import ClassVar

from pydantic import UUID4, ConfigDict

from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel
from universalrecipes.schema.response.pagination import PaginationBase


class MultiPurposeLabelCreate(UniversalRecipesModel):
    name: str
    color: str = "#959595"


class MultiPurposeLabelSave(MultiPurposeLabelCreate):
    group_id: UUID4


class MultiPurposeLabelUpdate(MultiPurposeLabelSave):
    id: UUID4


class MultiPurposeLabelSummary(MultiPurposeLabelUpdate, UniversalRecipesOutModel):
    _searchable_properties: ClassVar[list[str]] = ["name"]
    model_config = ConfigDict(from_attributes=True)


class MultiPurposeLabelPagination(PaginationBase):
    items: list[MultiPurposeLabelSummary]


class MultiPurposeLabelOut(MultiPurposeLabelUpdate, UniversalRecipesOutModel):
    model_config = ConfigDict(from_attributes=True)


class MultiPurposeLabelMerge(UniversalRecipesModel):
    from_id: UUID4
    to_id: UUID4
