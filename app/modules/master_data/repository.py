from app.core.repository import BaseRepository
from app.modules.master_data.models import (
    PartyDetails, BrokerDetails, TransportorDetails, GodownDetails,
    StockItems, PackagingDetails, WeightBridgeOperator
)
from app.modules.master_data.schemas import (
    PartyCreate, PartyUpdate,
    BrokerCreate, BrokerUpdate,
    TransportorCreate, TransportorUpdate,
    GodownCreate, GodownUpdate,
    StockItemsCreate, StockItemsUpdate,
    PackagingCreate, PackagingUpdate,
    WeightBridgeOperatorCreate, WeightBridgeOperatorUpdate
)

class PartyRepository(BaseRepository[PartyDetails, PartyCreate, PartyUpdate]):
    pass

class BrokerRepository(BaseRepository[BrokerDetails, BrokerCreate, BrokerUpdate]):
    pass

class TransportorRepository(BaseRepository[TransportorDetails, TransportorCreate, TransportorUpdate]):
    pass

class GodownRepository(BaseRepository[GodownDetails, GodownCreate, GodownUpdate]):
    pass

class StockItemRepository(BaseRepository[StockItems, StockItemsCreate, StockItemsUpdate]):
    pass

class PackagingRepository(BaseRepository[PackagingDetails, PackagingCreate, PackagingUpdate]):
    pass

class WeightBridgeOperatorRepository(BaseRepository[WeightBridgeOperator, WeightBridgeOperatorCreate, WeightBridgeOperatorUpdate]):
    pass

party_repository = PartyRepository(PartyDetails)
broker_repository = BrokerRepository(BrokerDetails)
transportor_repository = TransportorRepository(TransportorDetails)
godown_repository = GodownRepository(GodownDetails)
stock_item_repository = StockItemRepository(StockItems)
packaging_repository = PackagingRepository(PackagingDetails)
weight_bridge_operator_repository = WeightBridgeOperatorRepository(WeightBridgeOperator)
