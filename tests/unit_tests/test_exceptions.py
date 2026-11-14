from universalrecipes.core import exceptions
from universalrecipes.lang import get_locale_provider


def test_universalrecipes_registered_exceptions() -> None:
    provider = get_locale_provider()

    lookup = exceptions.universalrecipes_registered_exceptions(provider)

    assert lookup[exceptions.PermissionDenied] == "You do not have permission to perform this action"
    assert "The requested resource was not found" in lookup[exceptions.NoEntryFound]
    assert "integrity" in lookup[exceptions.IntegrityError]
