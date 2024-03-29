#!/usr/bin/env python3

import sys

# network calculator based on 2 inputs:
# ipv4 address and subnet mask, both in
# dotted-decimal format


# initializing the dictionary of all input and output values
NETWORK_DATA_DICT = {
    "ip_add": [0, "Host IPv4 Address"],
    "sub_mask": [0, "Subnet Mask"],
    "wildcard": [0, "Wildcard Mask"],
    "network": [0, "Network Address"],
    "bcast": [0, "Broadcast Address"],
    "hosts": [0, "Host addresses"],
}
INPUT_KEYS = ["ip_add", "sub_mask"]
OUTPUT_KEYS = ["wildcard", "network", "bcast", "hosts"]


def is_valid_ip_address(address: str):
    """
    --checks 4-item list as ipv4 address--
    input is dotted-decimal ipv4 address as string
    and returns True if it is a 'generically' valid IPv4
    address and False if not
    DOES NOT CHECK IF address IS THE NETWORK OR
    BROADCAST ADDRESS
    """
    # need to check:
    # len = 4
    # each block is <= 255 (decimal)
    if address.count(".") != 3:
        return False
    else:
        address = address.split(".")
        if len(address) < 4:
            return False
        for octet in address:
            try:
                if int(octet) > 255:
                    return False
            except ValueError:
                print("An octet in your IP address contains invalid input.")
                return False
    return True


def is_valid_subnet_mask(address: str):
    """
    checks 4-item list as ipv4 address
    and returns True if it is a valid
    address and False if not
    """
    # need to check:
    # len = 4
    # each block is <= 255
    # contiguous 1's
    if address.find(".") != 3:
        return False
    binmask = ipv4ToBin(address)
    for i in range(1, len(binmask)):
        if binmask[i] == "1":
            if binmask[i - 1] != "1":
                return False
    else:
        address = address.split(".")
        if len(address) < 4:
            return False
        for octet in address:
            try:
                if int(octet) > 255:
                    return False
            except ValueError:
                print("An octet in your subnet mask contains invalid input.")
                return False
    return True


def ipv4ToBin(address: str) -> str:
    """
    takes in dotted-decimal ipv4 address
    # takes in 4-item list as
    as a string and converts to 32-bit
    binary string
    """
    address = address.split(".")
    primary_out = ""
    for inp in address:
        output = ""
        inps = str(bin(int(inp))[2:])
        if len(inps) < 8:
            inps = ("0" * (8 - len(inps))) + inps
        for i in inps:
            output += i
        primary_out += output
    return primary_out


def binToIPv4(address: int) -> str:
    """
    takes in 32-bit unsigned integer and
    returns dotted-decimal string
    """
    output = ["", "", "", ""]
    for i in range(32):
        if i in range(8):
            output[0] += address[i]
        elif i in range(16):
            output[1] += address[i]
        elif i in range(24):
            output[2] += address[i]
        else:
            output[3] += address[i]
    for j in range(len(output)):
        output[j] = str(int(output[j], 2))
    return ".".join(output)


def get_wildcard(mask: str) -> str:
    """
    calculates wildcard mask based on subnet mask
    subnet mask input as string
    and returns subnet mask as dotted-decimal string
    """
    # flip bits in subnet mask and return
    wildmask = ""
    binmask = ipv4ToBin(mask)
    for i in range(len(binmask)):
        if binmask[i] == "1":
            wildmask += "0"
        else:
            wildmask += "1"
    return binToIPv4(wildmask)


def get_network(address, mask):
    """
    input of dotted-decimal string representations
    of a host address, return a dotted-decimal
    representation of the network address
    """
    netadd = ""
    binadd = ipv4ToBin(address)
    binmask = ipv4ToBin(mask)
    for i in range(32):
        if binmask[i] == "1":
            netadd += binadd[i]
        else:
            netadd += "0"
    return binToIPv4(netadd)


def get_broadcast(address, mask):
    """
    input of dotted-decimal string representations
    of a host address, return a dotted-decimal
    representation of the broadcast address
    """
    bcast_bin = ""
    binadd = ipv4ToBin(address)
    binmask = ipv4ToBin(mask)
    for i in range(32):
        if binmask[i] == "1":
            bcast_bin += binadd[i]
        else:
            bcast_bin += "1"
    return binToIPv4(bcast_bin)


def num_hosts(mask):
    """
    takes in dotted-decimal subnet mask
    returns number of hosts the subnet supports
    """
    power = 0
    binmask = ipv4ToBin(mask)
    for i in range(len(binmask)):
        if binmask[i] == "0":
            power += 1
    hosts = (2**power) - 2
    return hosts


def convert_mask(prefix_length):
    """
    take in integer value between 0-32, immediately return false if not

    output tuple of 2 strings: (dotted-decimal mask, binary mask string)
    """
    prefix_length = int(prefix_length)
    if prefix_length in range(33):
        # do the conversion
        # easiest first - convert to 32-char bit string
        bin_string = ""
        bin_string += "1" * prefix_length
        bin_string += "0" * (32 - prefix_length)
        return (binToIPv4(bin_string), bin_string)
    else:
        return False


def get_input() -> None:
    """
    takes in ipv4 address and subnet mask,
    checks for valid input
    returns 0 if input is invalid, else returns 2-item tuple in form:
    (ip_address, subnet_mask)
    i.e. ('10.0.0.1','255.255.255.0')
    note: ip address and subnet mask are strings at this point
    """
    # input block
    inp_msg = [
        "IPv4 dotted-decimal address:\n > ",
        "IPv4 dotted-decimal subnet mask:\n > ",
    ]
    ip_info = [input(inp_msg[a0]).strip() for a0 in range(2)]
    # check both inputs, subnet mask first and then ip address based on subnet mask
    if is_valid_subnet_mask(ip_info[1]) == False:
        print("Invalid subnet mask, please enter a valid dotted-decimal IPv4 mask.")
        # THIS RETURN STATEMENT STOPS THE PROGRAM ENTIRELY, TRACEBACK TO RETURN 0 IN MAIN
        return 0
    if is_valid_ip_address(ip_info[0]) == False:
        print("Invalid IP address, please enter a valid dotted-decimal IPv4 address.")
        # THIS RETURN STATEMENT STOPS THE PROGRAM ENTIRELY, TRACEBACK TO RETURN 0 IN MAIN
        return 0
    return (str(ip_info[0]), str(ip_info[1]))


def print_output() -> None:
    table_len = 40
    print("\n\n" + "=" * table_len)
    print("| Input Data: " + " " * (table_len - 15) + "|")
    print("| " + "-" * (table_len - 4) + " |")
    for key in INPUT_KEYS:
        data_len = len(NETWORK_DATA_DICT[key][1]) + len(NETWORK_DATA_DICT[key][0])
        print(
            "| "
            + str(NETWORK_DATA_DICT[key][1])
            + " " * (table_len - data_len - 4)
            + str(NETWORK_DATA_DICT[key][0])
            + " |"
        )
    print("=" * table_len + "\n| Output Data:" + " " * (table_len - 15) + "|")
    print("| " + "-" * (table_len - 4) + " |")
    for key in OUTPUT_KEYS:
        data_len = len(str(NETWORK_DATA_DICT[key][1])) + len(
            str(NETWORK_DATA_DICT[key][0])
        )
        print(
            "| "
            + str(NETWORK_DATA_DICT[key][1])
            + " " * (table_len - data_len - 4)
            + str(NETWORK_DATA_DICT[key][0])
            + " |"
        )
    print("=" * table_len + "\n\n")


def main():
    inp_tup = get_input()
    if inp_tup == 0:
        print("There was a problem with your input, program will now exit.")
        return 0

    net_host, net_mask = inp_tup[0], inp_tup[1]
    for key in range(len(INPUT_KEYS)):
        NETWORK_DATA_DICT[INPUT_KEYS[key]][0] = inp_tup[key]
    NETWORK_DATA_DICT["wildcard"][0] = get_wildcard(net_mask)
    NETWORK_DATA_DICT["network"][0] = get_network(net_host, net_mask)
    NETWORK_DATA_DICT["bcast"][0] = get_broadcast(net_host, net_mask)
    NETWORK_DATA_DICT["hosts"][0] = num_hosts(net_mask)

    print_output()
    return None


if __name__ == "__main__":
    main()
