import pytest
import requests

# Константы
BASE_URL = "https://qa-internship.avito.com"
VALID_SELLER_ID = 111111
INVALID_SELLER_ID = 100000  # вне диапазона
VALID_PRICE = 1000
INVALID_PRICE = "abc"  # некорректный тип

# Тест-кейсы для создания объявления (POST /api/1/item)
def test_create_item_success():
    """TC001: Позитивный кейс — создание объявления с корректными данными"""
    payload = {
        "sellerID": VALID_SELLER_ID,
        "name": "Тестовый товар",
        "price": VALID_PRICE,
        "statistics": {"contacts": 3, "likes": 500, "viewCount": 1523}
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 200, "Ожидался статус-код 200 OK"
    assert "status" in response.json(), "В ответе отсутствует поле 'status' (UUID объявления)"

def test_create_item_without_name():
    """TC002: Негативный кейс — отсутствие обязательного поля 'name'"""
    payload = {"sellerID": VALID_SELLER_ID, "price": VALID_PRICE}
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400, "Ожидался статус-код 400 Bad Request"

def test_create_item_with_invalid_sellerID():
    """TC003: Негативный кейс — некорректный sellerID (выход за диапазон)"""
    payload = {
        "sellerID": INVALID_SELLER_ID,
        "name": "Тестовый товар",
        "price": VALID_PRICE,
        "statistics": {"contacts": 3, "likes": 500, "viewCount": 1523}
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400, "Ожидался статус-код 400 Bad Request"

def test_create_item_with_invalid_price():
    """TC004: Негативный кейс — price не числового типа"""
    payload = {
        "sellerID": VALID_SELLER_ID,
        "name": "Тестовый товар",
        "price": INVALID_PRICE,
        "statistics": {"contacts": 3, "likes": 500, "viewCount": 1523}
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    assert response.status_code == 400, "Ожидался статус-код 400 Bad Request"

# Тест-кейсы для получения объявления по ID (GET /api/1/item/:id)
def test_get_item_by_id_success():
    """TC005: Позитивный кейс — получение существующего объявления"""
    # Предварительно создайте объявление через test_create_item_success()
    # и сохраните UUID из поля 'status' в ответе
    item_id = "ВАШ_UUID_ОБЪЯВЛЕНИЯ"  # замените на реальный UUID
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}")
    assert response.status_code == 200, "Ожидался статус-код 200 OK"
    assert response.json(), "Ответ должен содержать данные объявления"

def test_get_item_by_nonexistent_id():
    """TC006: Негативный кейс — поиск несуществующего объявления"""
    nonexistent_id = "nonexistent123"
    response = requests.get(f"{BASE_URL}/api/1/item/{nonexistent_id}")
    assert response.status_code == 404, "Ожидался статус-код 404 Not Found"
    assert "не найден" in response.json().get("message", ""), "Сообщение об ошибке не соответствует ожидаемому"

def test_get_item_with_invalid_id_format():
    """TC007: Негативный кейс — некорректный формат ID"""
    invalid_id = "abc123"
    response = requests.get(f"{BASE_URL}/api/1/item/{invalid_id}")
    assert response.status_code == 400, "Ожидался статус-код 400 Bad Request"

# Тест-кейсы для получения всех объявлений по ID продавца (GET /api/1/:sellerID/item)
def test_get_items_by_sellerID_with_items():
    """TC008: Позитивный кейс — получение объявлений для продавца с объявлениями"""
    response = requests.get(f"{BASE_URL}/api/1/{VALID_SELLER_ID}/item")
    assert response.status_code == 200, "Ожидался статус-код 200 OK"
    assert isinstance(response.json(), list), "Ответ должен быть списком объявлений"
    assert len(response.json()) >= 1, "У продавца должны быть объявления"

def test_get_items_by_sellerID_without_items():
    """TC009: Позитивный кейс — пустой список объявлений для продавца"""
    # Используйте sellerID, у которого точно нет объявлений
    empty_sellerID = 999999
    response = requests.get(f"{BASE_URL}/api/1/{empty_sellerID}/item")
    assert response.status_code == 200, "Ожидался статус-код 200 OK"
    assert response.json() == [], "Ответ должен быть пустым списком []"

def test_get_items_by_invalid_sellerID():
    """TC010: Негативный кейс — некорректный sellerID"""
    response = requests.get(f"{BASE_URL}/api/1/{INVALID_SELLER_ID}/item")
    assert response.status_code == 400, "Ожидался статус-код 400 Bad Request"

# Тест-кейсы для получения статистики по item ID (GET /api/2/statistic/:id)
def test_get_statistics_by_itemID_success():
    """TC011: Позитивный кейс — получение статистики для существующего объявления"""
    item_id = "ВАШ_UUID_ОБЪЯВЛЕНИЯ"  # замените на реальный UUID
    response = requests.get(f"{BASE_URL}/api/2/statistic/{item_id}")
    assert response.status_code == 200, "Ожидался статус-код 200 OK"
    stats = response.json()
    assert "contacts" in stats, "В статистике должен быть поле 'contacts'"
    assert "likes" in stats, "В статистике должен быть поле 'likes'"
    assert "viewCount" in stats, "В статистике должен быть поле 'viewCount'"

def test_get_statistics_by_nonexistent_itemID():
    """TC012: Негативный кейс — статистика для несуществующего объявления"""
    nonexistent_id = "nonexistent123"
    response = requests.get(f"{BASE_URL}/api/2/statistic/{nonexistent_id}")
    assert response.status_code == 404, "Ожидался статус-код 404 Not Found"
    assert "не найдена" in response.json().get("message", ""), "Сообщение об ошибке не соответствует ожидаемому"

def test_get_statistics_with_invalid_id_format():



