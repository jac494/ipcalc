#!/bin/python3
import sys
# network calculator based on 2 inputs: 
# ipv4 address and subnet mask, both in
# dotted-decimal format


# initializing the dictionary of all input and output values
ip_dict = {
    'ip_add': [0, 'Host IPv4 Address'],
    'sub_mask': [0, 'Subnet Mask'],
    'wildcard': [0, 'Wildcard Mask'],
    'network': [0, 'Network Address'],
    'bcast': [0, 'Broadcast Address'],
    'hosts': [0, 'Host addresses']
}
inp_keys = ['ip_add', 'sub_mask']
outp_keys = ['wildcard', 'network', 'bcast', 'hosts']



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# BEGIN HELPER FUNCTIONS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def checkIP(address):
    # function definition incomplete
    '''
    --checks 4-item list as ipv4 address--
    input is dotted-decimal ipv4 address as string
    and returns True if it is a valid
    address and False if not
    DOES NOT CHECK IF address IS THE NETWORK OR
    BROADCAST ADDRESS
    '''
    # need to check:
    # len = 4
    # each block is <= 255
    if address.count('.') != 3:
        return False
    else:
        address = address.split('.')
        if len(address) < 4:
            return False
        for octet in address:
            try:
                if int(octet) > 255:
                    return False
            except ValueError:
                print('An octet in your IP address contains invalid input.')
                return False
    return True
        
def checkSubMask(address):
    # function definition incomplete
    '''
    checks 4-item list as ipv4 address
    and returns True if it is a valid
    address and False if not
    '''
    # need to check:
    # len = 4
    # each block is <= 255
    # contiguous 1's
    if address.find('.') != 3:
        return False
    binmask = ipv4ToBin(address)
    for i in range(1,len(binmask)):
        if binmask[i] == '1':
            if binmask[i-1] != '1':
                return False
    else:
        address = address.split('.')
        if len(address) < 4:
            return False
        for octet in address:
            try:
                if int(octet) > 255:
                    return False
            except ValueError:
                print('An octet in your subnet mask contains invalid input.')
                return False
    return True
        


def ipv4ToBin(address):
    # function definition complete
    '''
    takes in dotted-decimal ipv4 address 
    # takes in 4-item list as
    as a string and converts to 32-bit
    binary string
    '''
    address = address.split('.')
    primary_out = ''
    for inp in address:
        output = ''
        inps = str(bin(int(inp))[2:])
        if len(inps) < 8: inps = ('0'*(8-len(inps))) + inps
        for i in inps:
            output += i
        primary_out += output
    return primary_out



def binToIPv4(address):
    # function definition incomplete
    '''
    takes in 32-bit unsigned integer and
    returns dotted-decimal string
    '''
    output = ['', '', '', '']
    for i in range(32):
        if i in range(8): output[0] += address[i]
        elif i in range(16): output[1] += address[i]
        elif i in range(24): output[2] += address[i]
        else: output[3] += address[i]
    for j in range(len(output)):
        output[j] = str(int(output[j], 2))
    return '.'.join(output)



def get_wildcard(mask):
    # function definition incomplete
    '''
    calculates wildcard mask based on subnet mask
    subnet mask input as string
    and returns subnet mask as dotted-decimal string
    '''
    # flip bits in subnet mask and return
    wildmask = ''
    binmask = ipv4ToBin(mask)
    for i in range(len(binmask)):
        if binmask[i] == '1': wildmask += '0'
        else: wildmask += '1'
    return binToIPv4(wildmask)



def get_network(address, mask):
    # function definition complete
    '''
    input of dotted-decimal string representations
    of a host address, return a dotted-decimal
    representation of the network address
    '''
    netadd = ''
    binadd = ipv4ToBin(address)
    binmask = ipv4ToBin(mask)
    for i in range(32):
        if binmask[i] == '1':
            netadd += binadd[i]
        else: netadd += '0'
    return binToIPv4(netadd)



def get_broadcast(address, mask):
    # function definition complete
    '''
    input of dotted-decimal string representations
    of a host address, return a dotted-decimal
    representation of the broadcast address
    '''
    bcast_bin = ''
    binadd = ipv4ToBin(address)
    binmask = ipv4ToBin(mask)
    for i in range(32):
        if binmask[i] == '1':
            bcast_bin += binadd[i]
        else: bcast_bin += '1'
    return binToIPv4(bcast_bin)



def num_hosts(mask):
    # function definition complete
    '''
    takes in dotted-decimal subnet mask
    returns number of hosts the subnet supports
    '''
    power = 0
    binmask = ipv4ToBin(mask)
    for i in range(len(binmask)):
        if binmask[i] == '0': power += 1
    hosts = (2**power) - 2
    return hosts



def convert_mask(prefix_length):
    #function definition incomplete
    #take in integer value between 0-32, immediately return false if not
    #output tuple of 2 strings: (dotted-decimal mask, binary mask string)
    prefix_length = int(prefix_length)
    if prefix_length in range(33):
        #do the conversion
        # easiest first - convert to 32-char bit string
        bin_string = ''
        bin_string += '1'*prefix_length
        bin_string += '0'*(32 - prefix_length)
        return (binToIPv4(bin_string),bin_string)
    else:
        return False



def get_input():
    #function definition complete
    '''
    takes in ipv4 address and subnet mask,
    checks for valid input
    returns 0 if input is invalid, else returns 2-item tuple in form:
    (ip_address, subnet_mask)
    i.e. ('10.0.0.1','255.255.255.0')
    note: ip address and subnet mask are strings at this point
    '''
    # input block
    inp_msg = ['IPv4 dotted-decimal address:\n > ', 'IPv4 dotted-decimal subnet mask:\n > ']
    ip_info = [input(inp_msg[a0]).strip() for a0 in range(2)]
    # check both inputs, subnet mask first and then ip address based on subnet mask
    if checkSubMask(ip_info[1]) == False:
        print('Invalid subnet mask, please enter a valid dotted-decimal IPv4 mask.')
        # THIS RETURN STATEMENT STOPS THE PROGRAM ENTIRELY, TRACEBACK TO RETURN 0 IN MAIN
        return 0
    if checkIP(ip_info[0]) == False:
        print('Invalid IP address, please enter a valid dotted-decimal IPv4 address.')
        # THIS RETURN STATEMENT STOPS THE PROGRAM ENTIRELY, TRACEBACK TO RETURN 0 IN MAIN
        return 0
    return (str(ip_info[0]), str(ip_info[1]))



def print_output():
    table_len = 40
    print("\n\n" + "="*table_len)
    print("| Input Data: " + ' '*(table_len-15) + '|')
    print('| ' + '-'*(table_len-4) + ' |')
    for key in inp_keys:
        data_len = len(ip_dict[key][1]) + len(ip_dict[key][0])
        print('| ' + str(ip_dict[key][1]) + ' '*(table_len-data_len-4) + str(ip_dict[key][0]) + ' |')
    print('='*table_len + '\n| Output Data:' + ' '*(table_len-15) +  '|')
    print('| ' + '-'*(table_len-4) + ' |')
    for key in outp_keys:
        data_len = len(str(ip_dict[key][1])) + len(str(ip_dict[key][0]))
        print('| ' + str(ip_dict[key][1]) + ' '*(table_len-data_len-4) + str(ip_dict[key][0]) + ' |')
    print('='*table_len + '\n\n')



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# END HELPER FUNCTIONS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-




# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# begin main()
def main():
    # GET USER INPUT
    # get_input returns 2-item tuple of (address, mask)
    inp_tup = get_input()
    if inp_tup == 0:
        print('There was a problem with your input, program will now exit.')
        return 0
        
    net_host, net_mask = inp_tup[0], inp_tup[1]
    # add inputs to dictionary
    for key in range(len(inp_keys)):
        ip_dict[inp_keys[key]][0] = inp_tup[key]
        # ip_dict[inp_keys[key]][1] = ipv4ToBin(ip_dict[inp_keys[key]][0])

    # use inputs to add output data to dictionary
    # ref: outp_keys = ['wildcard', 'network', 'bcast', 'hosts']
    ip_dict['wildcard'][0] = get_wildcard(net_mask)
    ip_dict['network'][0] = get_network(net_host, net_mask)
    ip_dict['bcast'][0] = get_broadcast(net_host, net_mask)
    ip_dict['hosts'][0] = num_hosts(net_mask)

    # temp output to see all values in ip_dict
    # print("\n\n" + "#"*40)
    # for key in ip_dict.keys():
    #   print(str(ip_dict[key][1]) + ': ' + str(ip_dict[key][0]))


    # final: print dictionary and dotted-decimal repr of addresses/masks
    print_output()
    return None
# end main()
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

main()
