from abc import ABC, abstractmethod
from enum import Enum
from math import ceil
from typing import List, Optional
from datetime import datetime
from collections import defaultdict

class User:
    pass

class VechicleType(Enum):
    BIKE = "bike"
    CAR = "car"
    BUS = "bus"

class Vechicle(ABC):
    @property
    @abstractmethod
    def type(self) -> VechicleType:
        pass

    @property
    @abstractmethod
    def license_plate(self) -> str:
        pass
    
    @abstractmethod
    def owner(self) -> User:
        pass


class Bike(Vechicle):
    def __init__(self, user: User, license_no: str) -> None:
        self._user = user
        self._license_no = license_no
    
    @property
    def license_plate(self):
        return self._license_no
    
    def owner(self) -> User:
        return self._user
    
    @property
    def type(self):
        return VechicleType.BIKE

class Car(Vechicle):
    def __init__(self, user: User, license_no: str) -> None:
        self._user = user
        self._license_no = license_no
    
    @property
    def license_plate(self):
        return self._license_no
    
    def owner(self) -> User:
        return self._user
    
    @property
    def type(self):
        return VechicleType.CAR

class Bus(Vechicle):
    def __init__(self, user: User, license_no: str) -> None:
        self._user = user
        self._license_no = license_no
    
    @property
    def license_plate(self):
        return self._license_no
    
    def owner(self) -> User:
        return self._user
    
    @property
    def type(self):
        return VechicleType.BUS


class ParkingSlot:
    def __init__(self, vechicleType: VechicleType, vechicle: Optional[Vechicle]) -> None:
        self.slot_id = ""
        self.vechicle: Optional[Vechicle] = vechicle
        self.is_free = True
        self.vechicle_type = vechicleType

    def update_slot(self, vechicle: Optional[Vechicle]) -> None:
        if vechicle:
            self.vechicle = vechicle
            self.is_free = False
        else:
            self.vechicle = None
            self.is_free = True

class FeeStrategy(ABC):
    @abstractmethod
    def calculateFee(self, base_rate, total_time_in_sec: int) -> int:
        pass

class HourlyFeeStrategy(FeeStrategy):
    def calculateFee(self, base_rate, total_time_in_sec: int) -> int:
        return ceil((base_rate * total_time_in_sec) / 3600)
    
class MinuteFeeStrategy(FeeStrategy):
    def calculateFee(self, base_rate, total_time_in_sec: int) -> int:
        return ceil((base_rate * total_time_in_sec) / 60)
    
class SecondFeeStrategy(FeeStrategy):
    def calculateFee(self, base_rate, total_time_in_sec: int) -> int:
        return ceil(base_rate * total_time_in_sec)    


class ParkingBuilding:
    def __init__(self, list_of_parking_slots: List[ParkingSlot], no_of_floor: int, list_of_gate: List[str],
                 fee_strategy: FeeStrategy) -> None:
        self.parkingSlots: List[ParkingSlot] = list_of_parking_slots
        self.no_of_floor: int = no_of_floor
        self.list_of_gate: List[str] = list_of_gate
        self.fee_strategy = fee_strategy
        self.groupParkingSlotByVechicleType = defaultdict(list)
        self.slotsPerVechicleType = {}

class ParkingTicket:
    def __init__(self, vechicle: Vechicle, parking_slot: ParkingSlot, user: User) -> None:
        self.vechicle = vechicle
        self.entry_time = datetime.now()
        self.parking_slot = parking_slot
        self.user = user
        self.exit_time = None
    
    def markExit(self):
        self.exit_time = datetime.now()



