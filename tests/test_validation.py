import unittest
from src.utils.validation import require_text, non_negative_integer, positive_id, iso_date

class ValidationTests(unittest.TestCase):
    def test_required_text(self):
        self.assertEqual(require_text("  Book  ","Title"),"Book")
        with self.assertRaises(ValueError):
            require_text(" ","Title")

    def test_non_negative_integer(self):
        self.assertEqual(non_negative_integer(0,"Quantity"),0)
        with self.assertRaises(ValueError):
            non_negative_integer(-1,"Quantity")
        with self.assertRaises(ValueError):
            non_negative_integer("x","Quantity")

    def test_positive_id(self):
        self.assertEqual(positive_id(4,"Book ID"),4)
        with self.assertRaises(ValueError):
            positive_id(0,"Book ID")

    def test_iso_date(self):
        self.assertEqual(iso_date("2026-08-21"),"2026-08-21")
        with self.assertRaises(ValueError):
            iso_date("21-08-2026")

if __name__=="__main__":
    unittest.main()
