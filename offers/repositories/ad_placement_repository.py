from typing import List
from typing import Optional

from offers.models import AdvertisingPlacement


class AdPlacementRepository:
    @staticmethod
    def get_active_advertising_placements() -> List[AdvertisingPlacement]:
        return AdvertisingPlacement.objects.filter(is_active=True)

    @staticmethod
    def get_advertising_placement_by_id(
        advertising_placement_id: int,
    ) -> Optional[AdvertisingPlacement]:
        return AdvertisingPlacement.objects.filter(id=advertising_placement_id).first()

    @staticmethod
    def get_active_advertising_placements_by_frontpage_path(
        frontpage_path: str,
    ) -> List[AdvertisingPlacement]:
        return AdvertisingPlacement.objects.filter(
            is_active=True, front_page__path=frontpage_path
        )
