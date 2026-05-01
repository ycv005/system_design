from abc import ABC, abstractmethod
from datetime import datetime
from math import ceil
from typing import Optional

from parking_lot.models import FeeStrategy, ParkingBuilding, ParkingSlot, ParkingTicket, User, Vechicle, VechicleType


class ParkingManager:
    def __init__(self, parking_building: ParkingBuilding):
        self.parking_building = parking_building
        self.arrangeParkingSlot()

    def parkAVechicle(self, vechicle: Vechicle, user: User) -> Optional[ParkingTicket]:
        slot = self.findASlot(vechicle.type)
        if not slot:
            raise Exception(f"No slot available for {vechicle.type}")
        parking_ticket = ParkingTicket(vechicle, slot, user)
        try:
            self.parking_building.groupParkingSlotByVechicleType[parking_ticket.vechicle.type].pop()
        except Exception as e:
            raise Exception("Failed to book slot")
        parking_ticket.parking_slot.update_slot(parking_ticket.vechicle)
        return parking_ticket

    def findASlot(self, vechicleType: VechicleType) -> Optional[ParkingSlot]:
        if self.parking_building.groupParkingSlotByVechicleType[vechicleType]:
            return self.parking_building.groupParkingSlotByVechicleType[vechicleType][-1]
        return None
    

    def exitAndFreeSlot(self, parking_ticket: ParkingTicket):
        parking_ticket.parking_slot.update_slot(None)
        self.parking_building.groupParkingSlotByVechicleType[parking_ticket.vechicle.type].append(parking_ticket.parking_slot)

    def arrangeParkingSlot(self):
        for slot in self.parking_building.parkingSlots:
            self.parking_building.groupParkingSlotByVechicleType[slot.vechicle_type].append(slot)
            if not self.parking_building.slotsPerVechicleType.get(slot.vechicle_type):
                self.parking_building.slotsPerVechicleType[slot.vechicle_type] = 0
            self.parking_building.slotsPerVechicleType[slot.vechicle_type] += 1


class ParkingFeeCalculator:
    FEES_PER_SECOND = {
        VechicleType.BIKE: 0.1,
        VechicleType.CAR: 0.15,
        VechicleType.BUS: 0.20,
    }

    def __init__(self, fee_straetgy: FeeStrategy) -> None:
        self.fee_straetgy = fee_straetgy

    def calculateFee(self, parking_ticket: ParkingTicket) -> float:
        current_vechicle = parking_ticket.vechicle

        base_fare = ParkingFeeCalculator.FEES_PER_SECOND.get(current_vechicle.type) # cannot access type here why ?
        exit_time = parking_ticket.exit_time if parking_ticket.exit_time else datetime.now()
        total_time = (exit_time - parking_ticket.entry_time).seconds

        total_amount = self.fee_straetgy.calculateFee(base_rate=base_fare, total_time_in_sec=total_time)

        return max(1, ceil(total_amount))