import sys
import unittest

sys.path.append("../ip_models")

from ip_models.ipv4 import AddressException, IPv4Address, IPv4NetMask


class TestIPv4Address(unittest.TestCase):
    def test_valid_integer_address(self):
        valid_cases = (
            (IPv4Address(0), (0, "0.0.0.0")),
            (IPv4Address(1), (1, "0.0.0.1")),
            (IPv4Address(10), (10, "0.0.0.10")),
            (IPv4Address(2**32 - 1), (2**32 - 1, "255.255.255.255")),
            (IPv4Address(3487534), (3487534, "0.53.55.46")),
        )
        for case_addr_obj, case_assert in valid_cases:
            self.assertEqual(case_addr_obj.address_int, case_assert[0])
            self.assertEqual(case_addr_obj.address_str, case_assert[1])

    def test_negative_integer_address(self):
        with self.assertRaises(AddressException) as addr_exc_ctxmgr:
            IPv4Address(-1)
        self.assertTrue(
            "IPv4Address cannot be less than 0" in str(addr_exc_ctxmgr.exception)
        )

    def test_large_integer_address(self):
        with self.assertRaises(AddressException) as addr_exc_ctxmgr:
            IPv4Address(2**33)
        self.assertTrue(
            "IPv4Address cannot be greater than or equal to 2**32"
            in str(addr_exc_ctxmgr.exception)
        )

    def test_valid_octet_cast(self):
        cases = (
            (IPv4Address("0.0.0.0"), 0),
            (IPv4Address("0.0.0.1"), 1),
            (IPv4Address("0.0.0.255"), 255),
            (IPv4Address("255.255.255.255"), 2**32 - 1),
            (IPv4Address("172.17.255.23"), 2886860567),
        )
        for case_obj, case_equal in cases:
            self.assertEqual(int(case_obj), case_equal)

    def test_negative_dotted_decimal_octet_raises_exception(self):
        for addr in ("0.0.0.-1", "0.0.-1.0", "0.-1.0.0", "-1.0.0.0", "-1.-1.-1.-1"):
            with self.assertRaises(AddressException) as addr_exc_ctxmgr:
                IPv4Address(addr)
            self.assertTrue(
                "IPv4 octet cannot be less than zero" in str(addr_exc_ctxmgr.exception)
            )

    def test_dotted_decimal_octet_too_large_raises_exception(self):
        for addr in (
            "0.0.0.256",
            "0.0.256.0",
            "0.256.0.0",
            "256.0.0.0",
            "256.256.256.256",
            "987439.28743535.82568734.95438",
        ):
            with self.assertRaises(AddressException) as addr_exc_ctxmgr:
                IPv4Address(addr)
            self.assertTrue(
                "IPv4 octet cannot be greater than 255"
                in str(addr_exc_ctxmgr.exception)
            )


class TestIpv4NetMask(unittest.TestCase):
    def test_cast_from_valid_bitlength(self):
        cases = (
            (IPv4NetMask(0), (0, "0.0.0.0")),
            (IPv4NetMask(1), (1, "128.0.0.0")),
            (IPv4NetMask(32), (32, "255.255.255.255")),
        )
        for case_netmask, case_results in cases:
            self.assertEqual(case_netmask.mask_length, case_results[0])
            self.assertEqual(case_netmask.address_str, case_results[1])

    def test_cast_from_valid_mask_str(self):
        cases = (
            (IPv4NetMask("0.0.0.0"), (0, "0.0.0.0")),
            (IPv4NetMask("128.0.0.0"), (1, "128.0.0.0")),
            (IPv4NetMask("255.255.255.255"), (32, "255.255.255.255")),
        )
        for case_netmask, case_results in cases:
            self.assertEqual(case_netmask.mask_length, case_results[0])
            self.assertEqual(case_netmask.address_str, case_results[1])


if __name__ == "__main__":
    unittest.main()
