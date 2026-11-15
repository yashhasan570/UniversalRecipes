import datetime
import enum

from isodate import parse_time
from pydantic import UUID4, ConfigDict, field_validator

from universalrecipes.schema._universalrecipes import UniversalRecipesModel
from universalrecipes.schema._universalrecipes.datetime_parse import parse_datetime
from universalrecipes.schema._universalrecipes.universalrecipes_model import UniversalRecipesOutModel
from universalrecipes.schema.response.pagination import PaginationBase


class WebhookType(enum.StrEnum):
    mealplan = "mealplan"


class WebhookCreate(UniversalRecipesModel):
    enabled: bool = True
    name: str = ""
    url: str = ""

    webhook_type: WebhookType = WebhookType.mealplan
    scheduled_time: datetime.time

    @field_validator("scheduled_time", mode="before")
    @classmethod
    def validate_scheduled_time(cls, v):
        """
        Validator accepts both datetime and time values from external sources.
        DateTime types are parsed and converted to time objects without timezones

        type: time is treated as a UTC value
        type: datetime is treated as a value with a timezone
        """
        parser_funcs = [
            lambda x: parse_datetime(x).astimezone(datetime.UTC).time(),
            parse_time,
        ]

        if isinstance(v, datetime.time):
            return v

        for parser_func in parser_funcs:
            try:
                return parser_func(v)
            except ValueError:
                continue

        raise ValueError(f"Invalid scheduled time: {v}")


class WebhookSave(WebhookCreate):
    group_id: UUID4
    household_id: UUID4


class WebhookOut(WebhookSave, UniversalRecipesOutModel):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)


class WebhookPagination(PaginationBase):
    items: list[WebhookOut]
