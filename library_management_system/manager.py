# Manager like LibraryManager, fee calculator, search book
# future scope - give notification to user for overdue

from abc import ABC, abstractmethod
from datetime import datetime
from math import ceil
from typing import Optional
import threading

from dataclasses import dataclass

@dataclass(frozen=True)
class RateConfig:
    hourly_rate: float
    penalty_rate: float

from library_management_system.models import BookStatus, BookingStatus, LibraryItemBook, User

class FeeStategy(ABC):
    @abstractmethod
    def calculate_fee(self, rate: float, total_time_in_sec: float) -> float:
        pass

class HourlyFeeStategy(FeeStategy):
    def calculate_fee(self, rate: float, total_time_in_sec: float) -> float:
        return ceil(max(1, (rate * total_time_in_sec / 3600)))

class BookNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class BookNotAvailable(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class PenaltyStrategy(ABC):
    @abstractmethod
    def calculate_penatly_fee(self, base_amount : float, overdue_time: float) -> float:
        pass

class FlatPenaltyStrategy(PenaltyStrategy):
    def __init__(self, flat_rate: float):
        self.flat_rate = flat_rate

    def calculate_penatly_fee(self, base_amount : float, overdue_time: float) -> float:
        if overdue_time <= 0:
            return base_amount
        return base_amount + self.flat_rate
    
class PercentagePenaltyStrategy(PenaltyStrategy):
    def __init__(self, penalty_percent: float):
        self.penalty_percent = penalty_percent

    def calculate_penatly_fee(self, base_amount : float, overdue_time: float) -> float:
        if overdue_time <= 0:
            return base_amount
        return base_amount + (base_amount * (self.penalty_percent / 100))


class DurationPenaltyStrategy(PenaltyStrategy):
    def __init__(self, rate_per_hour: float):
        self.rate_per_hour = rate_per_hour

    def calculate_penatly_fee(self, base_amount : float, overdue_time: float) -> float:
        if overdue_time <= 0:
            return base_amount
        return base_amount + (overdue_time / 3600) * self.rate_per_hour


class LibraryItemBookManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._bookings: dict(str, BookingStatus) = {}

    def searchBookBy(self, title: Optional[str], subject: Optional[str], author: Optional[str], booking_till: Optional[datetime]) -> Optional[list[LibraryItemBook]]:
        pass

    def reserveABook(self, book_obj: LibraryItemBook, user_obj: User, booking_till: datetime) -> Optional[BookingStatus]:
        with self._lock:
            if book_obj.status == BookStatus.AVAILABLE:
                booking_status = BookingStatus(book_obj.book, book_obj, datetime.now(), booking_till, user_obj)
                self._bookings[book_obj.book_item_id] = book_obj
                book_obj.updateBookStatus(BookStatus.BOOKED)
                return booking_status
            return None

    def submitAndFreeBookItem(self,  book_obj: LibraryItemBook) -> bool:
        booking_obj: Optional[LibraryItemBook] = self._bookings.pop(book_obj.book_item_id, None)
        if not booking_obj:
            return False
        booking_obj.updateBookStatus(BookStatus.AVAILABLE)
        return True

    def fetchBookingStatus(self, book_id: str) -> BookingStatus:
        pass

class LibraryManager:
    def __init__(self, library_item_book_manager: LibraryItemBookManager, feeStrategry: FeeStategy, penaltyStrategy: PenaltyStrategy, rate_map: dict):
        self.library_item_book_manager = library_item_book_manager
        self.feeStrategry = feeStrategry
        self.rate_map = rate_map
        self.penaltyStrategy = penaltyStrategy

    def findAndReserveBook(self, booking_till: datetime, user: User, title: Optional[str], subject: Optional[str], author: Optional[str]) -> Optional[LibraryItemBook]:
        book_objs = self.library_item_book_manager.searchBookBy(title, subject, author, booking_till)
        if not book_objs:
            raise BookNotFound("Try Searching by different values or options")
        # check book status
        available = [b for b in book_objs if b.status == BookStatus.AVAILABLE]
        if not available:
            raise BookNotAvailable("All copies are currently checked out")
        result_status = self.library_item_book_manager.reserveABook(available, user, booking_till)
        return available if result_status else None
    
    def returnBook(self, book_obj: LibraryItemBook):
        # check for book status
        booking_status = self.library_item_book_manager.fetchBookingStatus(book_obj.book_item_id)
        total_fee = self.feeStrategry.calculate_fee(self.rate_map.get("rate").get("hours"), booking_status.total_time_in_sec)
        over_due_time = max(0, (datetime.now() - booking_status.booking_to).total_seconds()) # avoiding earling submission
        estimated_final_fee = self.penaltyStrategy.calculate_penatly_fee(total_fee, RateConfig.penalty_rate, over_due_time)
        # raise this estimated_final_fee to the payment aggregator.
        self.library_item_book_manager.submitAndFreeBookItem(book_obj)
        