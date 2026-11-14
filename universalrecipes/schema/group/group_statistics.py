from universalrecipes.pkgs.stats import fs_stats
from universalrecipes.schema._universalrecipes import UniversalRecipesModel


class GroupStorage(UniversalRecipesModel):
    used_storage_bytes: int
    used_storage_str: str
    total_storage_bytes: int
    total_storage_str: str

    @classmethod
    def bytes(cls, used_storage_bytes: int, total_storage_bytes: int) -> GroupStorage:
        return cls(
            used_storage_bytes=used_storage_bytes,
            used_storage_str=fs_stats.pretty_size(used_storage_bytes),
            total_storage_bytes=total_storage_bytes,
            total_storage_str=fs_stats.pretty_size(total_storage_bytes),
        )
