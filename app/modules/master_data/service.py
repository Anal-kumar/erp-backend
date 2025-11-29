from app.core.service import BaseService
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
from app.modules.master_data.repository import (
    party_repository, broker_repository, transportor_repository,
    godown_repository, stock_item_repository, packaging_repository,
    weight_bridge_operator_repository
)

class PartyService(BaseService[PartyDetails, PartyCreate, PartyUpdate]):
    pass

class BrokerService(BaseService[BrokerDetails, BrokerCreate, BrokerUpdate]):
    pass

class TransportorService(BaseService[TransportorDetails, TransportorCreate, TransportorUpdate]):
    pass

class GodownService(BaseService[GodownDetails, GodownCreate, GodownUpdate]):
    pass

class StockItemService(BaseService[StockItems, StockItemsCreate, StockItemsUpdate]):
    pass

class PackagingService(BaseService[PackagingDetails, PackagingCreate, PackagingUpdate]):
    pass

class WeightBridgeOperatorService(BaseService[WeightBridgeOperator, WeightBridgeOperatorCreate, WeightBridgeOperatorUpdate]):
    pass

party_service = PartyService(party_repository)
broker_service = BrokerService(broker_repository)
transportor_service = TransportorService(transportor_repository)
godown_service = GodownService(godown_repository)
stock_item_service = StockItemService(stock_item_repository)
packaging_service = PackagingService(packaging_repository)
weight_bridge_operator_service = WeightBridgeOperatorService(weight_bridge_operator_repository)
