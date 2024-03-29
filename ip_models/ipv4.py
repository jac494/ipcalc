import logging


class AddressException(Exception):
    pass


class IPv4Address(object):
    def __init__(self, address_repr):
        self.address_int = None
        self.address_str = None
        logging.debug(
            f"Building IPv4Address object from {address_repr=} of type={type(address_repr)}"
        )
        if isinstance(address_repr, int):
            invalid_range_exception_str = "IPv4Address must be able to be represented by a positive integer within the range (0, 2**32) inclusive"
            if address_repr < 0:
                raise AddressException(
                    f"IPv4Address cannot be less than 0; {invalid_range_exception_str}"
                )
            elif address_repr >= 2**32:
                raise AddressException(
                    f"IPv4Address cannot be greater than or equal to 2**32; {invalid_range_exception_str}"
                )
            else:
                self.address_int = address_repr
                self.address_str = self._dotted_decimal_str_from_int()
        elif isinstance(address_repr, str):
            self.address_int = self._int_from_dotted_decimal_octet_str(address_repr)
            self.address_str = address_repr

    def __str__(self):
        return self.address_str

    def __repr__(self):
        return self.address_str

    def __int__(self):
        return self.address_int

    def __eq__(self, other):
        if isinstance(other, int):
            return self.address_int == other
        if isinstance(other, IPv4Address):
            return self.address_int == other.address_int
        if isinstance(other, str):
            return self.__str__() == other

    def _dotted_decimal_str_from_int(self):
        # slicing off the first two characters of the resulting string
        # since bin() returns something that looks like
        # '0b1000'
        temp_bin_str = bin(self.address_int)[2:]
        temp_pad_32_bits_str = temp_bin_str.zfill(32)
        octets_str_list = [
            str(int(temp_pad_32_bits_str[:8], 2)),
            str(int(temp_pad_32_bits_str[8:16], 2)),
            str(int(temp_pad_32_bits_str[16:24], 2)),
            str(int(temp_pad_32_bits_str[24:], 2)),
        ]
        return ".".join(octets_str_list)

    def _int_from_dotted_decimal_octet_str(self, dotted_decimal_octet_str):
        octet_str_list = dotted_decimal_octet_str.split(".")
        octet_count = len(octet_str_list)
        if octet_count != 4:
            raise AddressException(
                f"{dotted_decimal_octet_str} is not a valid dotted-decimal IPv4 address"
            )
        for octet in octet_str_list:
            if int(octet) < 0:
                raise AddressException(
                    f"Invalid IPv4 address {dotted_decimal_octet_str} IPv4 octet cannot be less than zero"
                )
            elif int(octet) > 255:
                raise AddressException(
                    f"Invalid IPv4 address {dotted_decimal_octet_str} IPv4 octet cannot be greater than 255"
                )
        octet_bin_list = [bin(int(octet))[2:].zfill(8) for octet in octet_str_list]
        return int("".join(octet_bin_list), 2)


class IPv4NetMask(IPv4Address):
    valid_subnet_masks = [
        IPv4Address(int("1" * mask_length + "0" * (32 - mask_length), 2))
        for mask_length in range(33)
    ]

    def __init__(self, mask_repr):
        self.mask_length = None
        if isinstance(mask_repr, int):
            if mask_repr not in range(33):
                raise AddressException(
                    "Subnet mask bit length must be a positive integer between 0 and 32, inclusive"
                )
            mask_bits_as_str = "1" * mask_repr + "0" * (32 - mask_repr)
            mask_32bit_int = int(mask_bits_as_str, 2)
            self.mask_length = mask_repr
            super().__init__(mask_32bit_int)
        if isinstance(mask_repr, str):
            super().__init__(address_repr=mask_repr)
            if self not in self.valid_subnet_masks:
                raise AddressException(f"{mask_repr} is not a valid subnet mask")
            self.mask_length = self._calculate_mask_length()

    def _calculate_mask_length(self):
        return bin(self.address_int).count("1")


class IPv4Network(object):
    pass
