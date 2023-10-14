import logging

class AddressException(Exception):
    pass

class IPv4Address(object):
    def __init__(self, address_repr):
        logging.debug(f"Building IPv4Address object from {address_repr=} of type={type(address_repr)}")
        if isinstance(address_repr, int):
            invalid_range_exception_str = "IPv4Address must be able to be represented by a positive integer within the range (0, 2**32) inclusive"
            if address_repr < 0:
                raise AddressException(f"IPv4Address cannot be less than 0; {invalid_range_exception_str}")
            elif address_repr > 2**32:
                raise AddressException(f"IPv4Address cannot be greater than 2**32; {invalid_range_exception_str}")
            else:
                self.address_int = address_repr