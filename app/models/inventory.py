from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base import Base
from datetime import datetime

class StockLedger(Base):
    __tablename__ = "stock_ledger"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    godown_id = Column(Integer, ForeignKey("godown_details_operations.id"), index=True)
    stock_item_id = Column(Integer, ForeignKey("stock_items_operations.id"), index=True)
    stock_quantity_bags = Column(Integer, default=0)  # Bags
    stock_weight_quintal = Column(Float, default=0.0)  # Quintals
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    godown = relationship("GodownDetails")
    stock_item = relationship("StockItems")

    def apply_stock_movement(self, transaction_type: bool, bags: int, weight_quintal: float):
        """
        Updates the stock ledger based on transaction type.
        :param transaction_type: True = Purchase (add), False = Sale (subtract)
        :param bags: number of bags moved
        :param weight_quintal: weight in quintals moved
        """
        if transaction_type:  # Purchase / Incoming
            self.stock_quantity_bags = (self.stock_quantity_bags or 0) + bags
            self.stock_weight_quintal = (self.stock_weight_quintal or 0.0) + weight_quintal
        else:  # Sale / Outgoing
            self.stock_quantity_bags = (self.stock_quantity_bags or 0) - bags
            self.stock_weight_quintal = (self.stock_weight_quintal or 0.0) - weight_quintal

    @hybrid_property
    def godown_name(self):
        return self.godown.godown_name if self.godown else None
