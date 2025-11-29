from pydantic import BaseModel
from datetime import datetime
from app.modules.master_data.schemas import GodownDetails, StockItemsDetails

class StockLedgerDetails(BaseModel):
    id: int
    godown: GodownDetails
    stock_item: StockItemsDetails
    stock_quantity_bags: int
    stock_weight_quintal: float
    last_updated: datetime

    class Config:
        from_attributes = True
