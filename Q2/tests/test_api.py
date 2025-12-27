import pytest
import requests

BASE_URL = "https://qa-internship.avito.com"

# Тесты для создания объявления (TC001–TC004)
def test_create_item_success():
    payload = {
        "sellerID": 111111,
        "name": "Тестовый товар",
        "price": 1000,
        "statistics": {"contacts": 3, "likes": 500, "viewCount": 1523}
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 200
    assert "status" in response.json()

def test_create_item_without_name():
    payload = {"sellerID": 111111, "price": 1000}
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400


