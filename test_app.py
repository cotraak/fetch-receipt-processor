import unittest
from app import validate_receipt, validate_item, calculate_points

class TestReceiptProcessor(unittest.TestCase):

    def test_validate_receipt_valid(self):
        valid_receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
            ],
            "total": "18.74"
        }
        self.assertTrue(validate_receipt(valid_receipt))

    def test_validate_receipt_missing_field(self):
        invalid_receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6.49"}]
        }
        self.assertFalse(validate_receipt(invalid_receipt))

    def test_validate_receipt_invalid_retailer(self):
        invalid_receipt = {
            "retailer": "Invalid Retailer!@#",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [{"shortDescription": "Mountain Dew 12PK", "price": "6.49"}],
            "total": "6.49"
        }
        self.assertFalse(validate_receipt(invalid_receipt))

    def test_validate_item_valid(self):
        valid_item = {"shortDescription": "Mountain Dew 12PK", "price": "6.49"}
        self.assertTrue(validate_item(valid_item))

    def test_validate_item_missing_price(self):
        invalid_item = {"shortDescription": "Mountain Dew 12PK"}
        self.assertFalse(validate_item(invalid_item))

    def test_validate_item_missing_short_description(self):
        invalid_item = {"price": "6.4"}
        self.assertFalse(validate_item(invalid_item))

    def test_validate_item_invalid_price(self):
        invalid_item = {"shortDescription": "Mountain Dew 12PK", "price": "6.4"}
        self.assertFalse(validate_item(invalid_item))

    def test_calculate_points_basic(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"}
            ],
            "total": "18.74"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 19)

    def test_calculate_points_round_total(self):
        receipt = {
            "retailer": "Walmart",
            "purchaseDate": "2022-03-15",
            "purchaseTime": "14:30",
            "items": [{"shortDescription": "Bread", "price": "5.00"}],
            "total": "5.00"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 98)

    def test_calculate_points_item_description_with_spaces(self):
        receipt = {
            "retailer": "ShopRite",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "11:01",
            "items": [{"shortDescription": "   Klarbrunn 12-PK 12 FL OZ   ", "price": "12.00"}],
            "total": "12.00"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 85)

    def test_calculate_points_no_points(self):
        receipt = {
            "retailer": "Store",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:30",
            "items": [],
            "total": "0"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 80)


if __name__ == "__main__":
    unittest.main()
