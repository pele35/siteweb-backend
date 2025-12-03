from typing import List
from typing import Optional

from offers.models import AdvertisingPlacement
from offers.repositories.ad_placement_repository import AdPlacementRepository


class AdPlacementService:
    @staticmethod
    def list_active_advertising_placements() -> List[AdvertisingPlacement]:
        return AdPlacementRepository.get_active_advertising_placements()

    @staticmethod
    def retrieve_advertising_placement(
        advertising_placement_id: int,
    ) -> Optional[AdvertisingPlacement]:
        return AdPlacementRepository.get_advertising_placement_by_id(
            advertising_placement_id
        )

    @staticmethod
    def list_active_advertising_placements_by_frontpage(
        frontpage_path: str,
    ) -> List[AdvertisingPlacement]:
        return (
            AdPlacementRepository.get_active_advertising_placements_by_frontpage_path(
                frontpage_path
            )
        )
