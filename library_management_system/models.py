from  datetime import datetime
from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional
import uuid



class BookStatus(Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    OVERDUE = "overdue"


class Book(ABC):
    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def author(self) -> str:
        pass

    @property
    @abstractmethod
    def subject(self) -> str:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

class LibraryBaseBook(Book):
    def __init__(self, title: str, author: str, subject: str, price: float) -> None:
        self._title = title
        self._author = author
        self._subject = subject
        self._price = price
        self.book_id = str(uuid.uuid4())

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def subject(self):
        return self._subject

    @property
    def price(self):
        return self._price

class LibraryItemBook:
    def __init__(self, book: LibraryBaseBook) -> None:
        self.status = BookStatus.AVAILABLE
        self.book: LibraryBaseBook = book # generate with UUID
        self.book_item_id = str(uuid.uuid4())
    
    def updateBookStatus(self, status: BookStatus):
        self.status = status
    

class BookingStatus:
    def __init__(self, book: LibraryBaseBook, book_item: LibraryItemBook, booking_from: datetime, booking_to: datetime, user: User):
        self.booking_id = str(uuid.uuid4())
        self.book = book
        self.book_item = book_item
        self.booking_from = booking_from
        self.booking_to = booking_to
        self.current_status = BookStatus.BOOKED
        self.user = user
    
    def updateBookStatus(self, status: BookStatus, booking_to: Optional[datetime]):
        self.current_status = status
        # extend book time
        if booking_to:
            self.booking_to = booking_to
    @property
    def total_time_in_sec(self) -> float:
        return (self.booking_to - self.booking_from).total_seconds()


class User(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

class Librarian(User):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self):
        return self._name
    
    def addBook(self, book: LibraryBaseBook):
        pass

    def removeBook(self, book: LibraryBaseBook):
        pass
    
class Reader(User):
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self):
        return self._name