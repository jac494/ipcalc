import sys
import unittest

sys.path.append("../ip_models")

from ip_models.ipv4 import AddressException, IPv4Address

class TestIPv4Address(unittest.TestCase):
    def test_valid_integer_address(self):
        valid_cases = (
            (IPv4Address(0), 0),
            (IPv4Address(1), 1),
            (IPv4Address(10), 10),
            (IPv4Address(2**32), 2**32),
            (IPv4Address(3487534), 3487534),
        )
        for case_addr_obj, case_assert in valid_cases:
            self.assertEqual(case_addr_obj.address_int, case_assert)

    def test_negative_integer_address(self):
        with self.assertRaises(AddressException) as addr_exc_ctxmgr:
            IPv4Address(-1)
        self.assertTrue("IPv4Address cannot be less than 0" in str(addr_exc_ctxmgr.exception))
    
    def test_large_integer_address(self):
        with self.assertRaises(AddressException) as addr_exc_ctxmgr:
            IPv4Address(2**33)
        self.assertTrue("IPv4Address cannot be greater than 2**32" in str(addr_exc_ctxmgr.exception))

if __name__ == "__main__":
    unittest.main()
