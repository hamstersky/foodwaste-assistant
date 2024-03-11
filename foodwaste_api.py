from dataclasses import dataclass
import requests


@dataclass
class Store:
    id: str
    name: str
    address: str


@dataclass
class Offer:
    discount: int
    percentDiscount: float
    new_price: float
    original_price: float
    categories: str
    description: str


class FoodwasteAPI:
    BASE_URL = "https://api.sallinggroup.com"
    FOODWASTE_RESOURCE = "v1/food-waste"
    STORES_RESOURCE = "v2/stores"

    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_stores(self, zip: str):
        endpoint = f"{self.BASE_URL}/{self.STORES_RESOURCE}"
        self.session.get(endpoint, params={"zip": zip}).json()
        store_data = self.session.get(endpoint, params={"zip": zip}).json()

        stores = [
            Store(store["id"], store["name"], store["address"]["street"])
            for store in store_data
        ]

        return stores

    def get_offers(self, store_id: str):
        endpoint = f"{self.BASE_URL}/{self.FOODWASTE_RESOURCE}/{store_id}"
        offer_data = self.session.get(endpoint).json()

        offers = [
            Offer(
                offer["offer"]["discount"],
                offer["offer"]["percentDiscount"],
                offer["offer"]["newPrice"],
                offer["offer"]["originalPrice"],
                offer["product"].get("categories", {}).get("en", ""),
                offer["product"]["description"],
            )
            for offer in offer_data["clearances"]
        ]

        return offers
