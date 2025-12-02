from typing import List, Optional, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from datetime import date, datetime
from app.core.repository import BaseRepository
from app.modules.inventory.models import (
    IncomingOutgoing, IncomingOutgoingItems, IncomingOutgoingPayment,
    TransactionMillOperations, TransactionStockItem, TransactionPaymentDetails,
    TransactionPackagingDetails, TransactionAllowanceDeductionsDetails,
    TransactionUnloadingPointDetails, BagDetails, BagsStatus, StockLedger
)
from app.modules.inventory.schemas import (
    IncomingOutgoingCreate, IncomingOutgoingUpdate,
    TransactionStockItemCreate, TransactionPaymentCreate,
    TransactionPackagingCreate, AllowanceDeductionCreate,
    TransactionUnloadingPointCreate
)
from app.modules.master_data.models import (
    PartyDetails, BrokerDetails, TransportorDetails,
    GodownDetails, StockItems, PackagingDetails, WeightBridgeOperator
)
from app.modules.users.models import User

class IncomingOutgoingRepository(BaseRepository[IncomingOutgoing, IncomingOutgoingCreate, IncomingOutgoingUpdate]):
    def get_multi_with_filters(
        self,
        db: Session,
        *,
        brought_by: Optional[str] = None,
        vehicle_no: Optional[str] = None,
        party_through: Optional[str] = None,
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        is_incoming: Optional[bool] = None
    ) -> List[IncomingOutgoing]:
        query = db.query(IncomingOutgoing).options(
            joinedload(IncomingOutgoing.incoming_outgoing_items),
            joinedload(IncomingOutgoing.users),
            joinedload(IncomingOutgoing.incoming_outgoing_payment)
        )

        if is_incoming is not None:
            query = query.filter(IncomingOutgoing.is_incoming == is_incoming)

        if from_date:
            query = query.filter(IncomingOutgoing.io_date >= from_date)
        if to_date:
            query = query.filter(IncomingOutgoing.io_date <= to_date)
        
        if brought_by:
            query = query.filter(IncomingOutgoing.brought_by.ilike(f"%{brought_by}%"))
        if party_through:
            query = query.filter(IncomingOutgoing.party_through.ilike(f"%{party_through}%"))
        if vehicle_no:
            query = query.filter(IncomingOutgoing.vehicle_no.ilike(f"%{vehicle_no}%"))

        return query.all()

    def get_by_id(self, db: Session, id: int) -> Optional[IncomingOutgoing]:
        return db.query(IncomingOutgoing).options(
            joinedload(IncomingOutgoing.incoming_outgoing_items),
            joinedload(IncomingOutgoing.incoming_outgoing_payment)
        ).filter(IncomingOutgoing.id == id).first()

    def create_with_items(
        self, db: Session, *, obj_in: IncomingOutgoingCreate
    ) -> IncomingOutgoing:
        # Extract non-nested fields
        incoming_data = obj_in.model_dump(exclude={"incoming_outgoing_items", "incoming_outgoing_payment"})
        
        db_obj = IncomingOutgoing(**incoming_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create nested items
        if obj_in.incoming_outgoing_items:
            for item in obj_in.incoming_outgoing_items:
                db_item = IncomingOutgoingItems(
                    incoming_outgoing_id=db_obj.id,
                    **item.model_dump()
                )
                db.add(db_item)

        # Create nested payments
        if obj_in.incoming_outgoing_payment:
            for payment in obj_in.incoming_outgoing_payment:
                db_payment = IncomingOutgoingPayment(
                    incoming_outgoing_id=db_obj.id,
                    payment_amount=payment.payment_amount or 0,
                    payment_date=payment.payment_date
                )
                db.add(db_payment)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_items(
        self, db: Session, *, db_obj: IncomingOutgoing, obj_in: IncomingOutgoingUpdate
    ) -> IncomingOutgoing:
        # Update parent fields
        update_data = obj_in.model_dump(exclude={"incoming_outgoing_items", "incoming_outgoing_payment"}, exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        # Update nested items
        if obj_in.incoming_outgoing_items is not None:
            # Delete existing
            db.query(IncomingOutgoingItems).filter(IncomingOutgoingItems.incoming_outgoing_id == db_obj.id).delete()
            # Add new
            for item in obj_in.incoming_outgoing_items:
                db_item = IncomingOutgoingItems(
                    incoming_outgoing_id=db_obj.id,
                    **item.model_dump()
                )
                db.add(db_item)

        # Update nested payments
        if obj_in.incoming_outgoing_payment is not None:
            db.query(IncomingOutgoingPayment).filter(IncomingOutgoingPayment.incoming_outgoing_id == db_obj.id).delete()
            for payment in obj_in.incoming_outgoing_payment:
                db_payment = IncomingOutgoingPayment(
                    incoming_outgoing_id=db_obj.id,
                    **payment.model_dump()
                )
                db.add(db_payment)

        db.commit()
        db.refresh(db_obj)
        return db_obj


class TransactionRepository(BaseRepository[TransactionMillOperations, Any, Any]):
    def get_multi_with_filters(
        self,
        db: Session,
        *,
        party_name: Optional[str] = None,
        broker_name: Optional[str] = None,
        transporter_name: Optional[str] = None,
        stock_item_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        transaction_type: Optional[bool] = None
    ) -> List[TransactionMillOperations]:
        query = db.query(TransactionMillOperations).options(
            joinedload(TransactionMillOperations.users).load_only(User.user_login_id),
            joinedload(TransactionMillOperations.bag_details).joinedload(BagDetails.packaging),
            joinedload(TransactionMillOperations.transaction_allowance_deduction_details),
            joinedload(TransactionMillOperations.transaction_payments_mill_operations),
            joinedload(TransactionMillOperations.transaction_packaging_details).joinedload(TransactionPackagingDetails.packaging),
            joinedload(TransactionMillOperations.transaction_unloading_point_details),
            joinedload(TransactionMillOperations.transaction_stock_items).joinedload(TransactionStockItem.stock_items),
            joinedload(TransactionMillOperations.party),
            joinedload(TransactionMillOperations.broker),
            joinedload(TransactionMillOperations.transportor),
            joinedload(TransactionMillOperations.weight_bridge_operator),
        )

        if party_name:
            query = query.join(PartyDetails).filter(PartyDetails.party_name.ilike(f"%{party_name}%"))
        if broker_name:
            query = query.join(BrokerDetails).filter(BrokerDetails.broker_name.ilike(f"%{broker_name}%"))
        if transporter_name:
            query = query.join(TransportorDetails).filter(TransportorDetails.transportor_name.ilike(f"%{transporter_name}%"))
        if stock_item_name:
            query = query.join(TransactionStockItem).join(StockItems).filter(StockItems.stock_item_name.ilike(f"%{stock_item_name}%"))
        if start_date:
            query = query.filter(TransactionMillOperations.transaction_date >= start_date)
        if end_date:
            query = query.filter(TransactionMillOperations.transaction_date <= end_date)
        if transaction_type is not None:
            query = query.filter(TransactionMillOperations.transaction_type == transaction_type)

        return query.all()

    def get_by_id(self, db: Session, id: int) -> Optional[TransactionMillOperations]:
        return db.query(TransactionMillOperations).options(
            joinedload(TransactionMillOperations.users),
            joinedload(TransactionMillOperations.transaction_allowance_deduction_details),
            joinedload(TransactionMillOperations.transaction_payments_mill_operations),
            joinedload(TransactionMillOperations.transaction_stock_items),
            joinedload(TransactionMillOperations.transaction_unloading_point_details),
            joinedload(TransactionMillOperations.transaction_packaging_details)
        ).filter(TransactionMillOperations.id == id).first()

    def get_stock_summary(
        self,
        db: Session,
        godown_name: Optional[str] = None,
        stock_item_name: Optional[str] = None
    ):
        # 1. Query the raw stock ledger totals (Bags & Weight)
        query = db.query(
            GodownDetails.godown_name.label("godown_name"),
            StockItems.stock_item_name.label("stock_item_name"),
            func.sum(StockLedger.stock_quantity_bags).label("total_bags"),
            func.sum(StockLedger.stock_weight_quintal).label("total_weight_quintal")
        ).join(
            GodownDetails, GodownDetails.id == StockLedger.godown_id
        ).join(
            StockItems, StockItems.id == StockLedger.stock_item_id
        ).group_by(
            GodownDetails.godown_name, StockItems.stock_item_name
        )

        if godown_name:
            query = query.filter(GodownDetails.godown_name.ilike(f"%{godown_name}%"))

        if stock_item_name:
            query = query.filter(StockItems.stock_item_name.ilike(f"%{stock_item_name}%"))

        results = query.all()

        # 2. Compute packaging weight adjustments for all sales (transaction_type == False).
        bag_weight_adjustments = {}  # key: (godown_name, stock_item_name) -> quintals to subtract
        sales_txn_q = db.query(TransactionMillOperations).options(
            joinedload(TransactionMillOperations.transaction_packaging_details).joinedload(TransactionPackagingDetails.packaging),
            joinedload(TransactionMillOperations.transaction_unloading_point_details).joinedload(TransactionUnloadingPointDetails.godown),
            joinedload(TransactionMillOperations.transaction_stock_items).joinedload(TransactionStockItem.stock_items),
        ).filter(TransactionMillOperations.transaction_type == False)

        if godown_name:
            sales_txn_q = sales_txn_q.join(TransactionUnloadingPointDetails).join(GodownDetails).filter(GodownDetails.godown_name.ilike(f"%{godown_name}%"))
        if stock_item_name:
            sales_txn_q = sales_txn_q.join(TransactionStockItem).join(StockItems).filter(StockItems.stock_item_name.ilike(f"%{stock_item_name}%"))

        sales_transactions = sales_txn_q.all()

        for tx in sales_transactions:
            pkgs = tx.transaction_packaging_details or []
            unloads = tx.transaction_unloading_point_details or []
            t_stock_items = tx.transaction_stock_items or []

            total_pack_bags = sum((p.bag_nos or 0) for p in pkgs) if pkgs else 0
            total_bag_weight_grams = 0
            for p in pkgs:
                if getattr(p, "packaging", None) and getattr(p.packaging, "bag_weight", None):
                    total_bag_weight_grams += (p.packaging.bag_weight or 0) * (p.bag_nos or 0)

            total_unload_bags = sum((u.number_of_bags or 0) for u in unloads) if unloads else 0
            if total_unload_bags == 0 or not t_stock_items:
                continue

            total_stock_bags_in_txn = sum((si.number_of_bags or 0) for si in t_stock_items) if t_stock_items else 0
            
            for u in unloads:
                godown = getattr(u, "godown", None)
                if not godown:
                    continue
                unload_bags = (u.number_of_bags or 0)
                
                if total_stock_bags_in_txn == 0:
                    base = unload_bags // len(t_stock_items)
                    remainder = unload_bags % len(t_stock_items)
                    item_allocations = [(si, base + (1 if idx < remainder else 0)) for idx, si in enumerate(t_stock_items)]
                else:
                    remaining_bags_to_assign = unload_bags
                    item_allocations = []
                    for idx, si in enumerate(t_stock_items):
                        if idx < len(t_stock_items) - 1:
                            proportion = ((si.number_of_bags or 0) / total_stock_bags_in_txn)
                            item_bags_for_unload = int(proportion * unload_bags)
                            item_bags_for_unload = min(item_bags_for_unload, remaining_bags_to_assign)
                        else:
                            item_bags_for_unload = remaining_bags_to_assign
                        
                        remaining_bags_to_assign -= item_bags_for_unload
                        item_allocations.append((si, item_bags_for_unload))

                for si, item_bags_for_unload in item_allocations:
                    if item_bags_for_unload <= 0:
                        continue
                        
                    allocated_bag_weight_grams = total_bag_weight_grams * (item_bags_for_unload / total_unload_bags)
                    allocated_quintal = allocated_bag_weight_grams / 100000.0
                    
                    key = (godown.godown_name, si.stock_items.stock_item_name if si.stock_items else None)
                    bag_weight_adjustments[key] = bag_weight_adjustments.get(key, 0.0) + allocated_quintal

        godown_totals = {}
        for row in results:
            godown = row.godown_name
            item_name = row.stock_item_name
            if godown not in godown_totals:
                godown_totals[godown] = {
                    "godown_name": godown,
                    "items": [],
                    "total_bags": 0,
                    "total_weight_quintal": 0.0
                }

            adj = bag_weight_adjustments.get((godown, item_name), 0.0)
            adjusted_weight_quintal = float(((row.total_weight_quintal or 0) - adj))

            godown_totals[godown]["items"].append({
                "stock_item_name": item_name,
                "bags": int(row.total_bags or 0),
                "weight_quintal": adjusted_weight_quintal
            })

            godown_totals[godown]["total_bags"] += int(row.total_bags or 0)
            godown_totals[godown]["total_weight_quintal"] += adjusted_weight_quintal

        grand_total_bags = sum(g["total_bags"] for g in godown_totals.values())
        grand_total_weight = sum(g["total_weight_quintal"] for g in godown_totals.values())

        return {
            "summary": list(godown_totals.values()),
            "grand_total": {
                "total_bags": grand_total_bags,
                "total_weight_quintal": grand_total_weight
            }
        }

incoming_outgoing_repository = IncomingOutgoingRepository(IncomingOutgoing)
transaction_repository = TransactionRepository(TransactionMillOperations)
