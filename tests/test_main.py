import unittest
from main import check_allowed_values

class TestCheckAllowedValues(unittest.TestCase):
    def test_allowed(self):
        self.assertTrue(check_allowed_values("forward", 0))

    def test_allowed2(self):
        self.assertTrue(check_allowed_values("reverse", 0))

    def test_allowed3(self):
        self.assertTrue(check_allowed_values("forward", 100))

    def test_allowed4(self):
        self.assertTrue(check_allowed_values("reverse", 100))

    def test_fail1(self):
        self.assertFalse(check_allowed_values(0, 0))

    def test_fail2(self):
        self.assertFalse(check_allowed_values("not_allowed", 0))

    def test_fail3(self):
        self.assertFalse(check_allowed_values("forward", -1))

    def test_fail4(self):
        self.assertFalse(check_allowed_values("forward", 1.0))

    def test_fail5(self):
        self.assertFalse(check_allowed_values("not_allowed", -100))

    def test_fail6(self):
        self.assertFalse(check_allowed_values("reverse", 101))

if __name__ == "__main__":
    unittest.main()