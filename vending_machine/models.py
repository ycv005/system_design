from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid

class Coin(Enum):
    ONE = 1
    TWO = 2
    FIVE = 5
    TEN = 10
    TWENTY = 20

class FoodBase:
    def __init__(self, title, description, size_type, size_value) -> None:
        self.title = title
        self.description = description
        self.size_type = size_type
        self.size_value = size_value
        # more fields that are

class FoodBaseItem:
    def __init__(self, food_base: FoodBase, price: float, batch_no: str, last_use_date: datetime) -> None:
        self.id = str(uuid.uuid4())
        self.food_base = food_base
        self.batch_no = batch_no
        self.last_use_date = last_use_date
        self.price = price

class VendingMachine:
    def __init__(self, stock_mapping: dict(str, int), stocks):
        self.current_state = IdleVendingState(self)
        self.current_coins: list[Coin] = []
        self.stock_mapping_quantity: dict(str, int) = stock_mapping
        self.inventory_mapping: dict(str, FoodBaseItem) = stocks
        self.processing_inventory: list[FoodBaseItem] = []
    
    def update_stock(self, stocks: list[FoodBaseItem]):
        for stock in stocks:
            if stock.batch_no not in self.stock_mapping_quantity:
                self.stock_mapping_quantity[stock.batch_no] = 0
            self.stock_mapping_quantity[stock.batch_no] += 1

            self.inventory_mapping[stock.id] = stock

    def total_coin_value(self) -> float:
        total_value = 0
        for coin in self.current_coins:
            total_value += coin.value
        return total_value
    
    def update_state(self, state: 'VendingState'):
        self.current_state = state


class VendingState(ABC):
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine

    @abstractmethod
    def insert_coin(self, coin: Coin):
        pass

    @abstractmethod
    def dispense(self):
        pass

    @abstractmethod
    def select_items(self, item_codes: str):
        pass

    @abstractmethod
    def refund_amount(self, amount: int):
        pass


class IdleVendingState(VendingState):
    def insert_coin(self, coin):
        self.vending_machine.current_coins.append(coin)

    def dispense(self):
        print("Please insert coin first")

    def select_items(self, item_codes: str):
        print("Please select Item first")

    def refund_amount(self, amount: int):
        print("Please insert coin first")

class DispenseVendingState(VendingState):
    def __init__(self, vending_machine: VendingMachine):
        self.dispense()

    def insert_coin(self, coin):
        print("Please wait while Item are dispensing")

    def dispense(self):
        for each_inv in self.vending_machine.processing_inventory:
            self.vending_machine.stock_mapping_quantity[each_inv.batch_no] -= 1
            self.vending_machine.inventory_mapping.pop(each_inv.id, None)
            print(f"You got {each_inv.food_base.title} in tray.")

    def select_items(self, item_codes: str):
        print("Please select Item first")

    def refund_amount(self, amount: int):
        print("Please wait while Item are dispensing")


class SelectItemVendingState(VendingState):
    def insert_coin(self, coin):
        self.vending_machine.current_coins.append(coin)

    def dispense(self):
        print("Please select Item first")

    def select_items(self, item_codes: str):
        total_item_price: float = 0
        new_processing_items = []
        for item_code in item_codes:
            item_obj: FoodBaseItem = self.vending_machine.inventory_mapping[item_code]
            total_item_price += item_obj.price
            new_processing_items.append(item_obj)
        
        total_value = self.vending_machine.total_coin_value()
        if total_item_price > total_value:
            print(f"Please insert more coins equal to {total_item_price - total_value}")
        else:
            self.refund_amount(total_item_price - total_value)
            self.vending_machine.processing_inventory = new_processing_items
            self.vending_machine.update_state(DispenseVendingState(self.vending_machine))

    def refund_amount(self, amount: int):
        print(f"Please collect money {amount} below")


class GotMoneyVendingState(VendingState):
    def insert_coin(self, coin):
        self.vending_machine.current_coins.append(coin)

    def dispense(self):
        print("Please select items")

    def select_items(self, item_codes: str):
        self.vending_machine.update_state(SelectItemVendingState(self.vending_machine))
    
    def refund_amount(self, amount: float):
        print(f"Please collect money {amount} below")

