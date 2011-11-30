# -*- coding: utf-8 -*- 
"""
Bunch of functions that implements Reed-Muller (RM(N,1)) coding algorithm. 
"""

from math import log
from numpy import matrix

VERBOSE = False 

def encode_message(message):
    """Encodes given message using Reed–Muller code."""
    # Creating matrix (row) from message
    message_list = [int(el) for el in message]
    message_row = matrix(message_list)
    # Obtaining coding matrix for given message
    coding_matrix = _generate_coding_matrix(len(message))
    # Obtaining and returning coded string
    encoded_row = message_row * coding_matrix
    code = [str(el % 2) for el in encoded_row.tolist()[0]]
    if VERBOSE:
        print "Multiplying message and generating matrix..."
    return "".join(code) 

def _generate_coding_matrix(n):
    """Generates coding matrix for a given length of message."""
    # n value for coding matrix is actually (length of message - 1)
    n = n - 1
    # forming list of matrix columns
    result = []
    for i in range(0, 2 ** n):
        # first element of every column is 1
        line = [1]
        F = i
        for j in range(n - 1, -1, -1):
            line.insert(n - j, F / (2 ** j))
            F = F % (2 ** j)
        result.append(line)
    # creating matrix (transposing it to obtain rows from columns list)
    result_matrix = matrix(result).T
    if VERBOSE:
        print "Generating matrix:\n" + str(result_matrix)
    return result_matrix

def decode_message(code):
    """Decodes code encoded using Reed–Muller code."""
    checksums = _generate_pairs(int(log(len(code), 2)))
    return _decode(code, checksums)

def _generate_pairs(n):
    """Generates pairs for RM coding (for encoded string with length n)."""
    result = []
    for i in range(0, n):
        tmp_result = []
        for j in range(0, 2 ** (n - 1 - i)):
            for l in range(1, 2 ** i + 1):
                tmp_result.append(l + j * (2 ** (i + 1)))
                tmp_result.append(l + j * (2 ** (i + 1)) + 2 ** i)
        # generate pairs 
        result.append(zip(tmp_result[::2], tmp_result[1::2]))
    if VERBOSE:
        message_length = len(result) + 1
        for i in range(0, len(result)):
            print 'm' + str(message_length - i) + ':'
            print ''.join(['c' + str(e[0]) + ' + c' + str(e[1]) + '\n' \
                    for e in result[i]])
    return result

def _decode(code, checksums):
    """Actually decodes the code."""
    message = []
    for checksum_interval in checksums:
        # finding possible list values
        symbol_values_list = []
        for checksum in checksum_interval:
            # Adding values at given positions (chk pairs) in encoded string
            symbol_values_list.append(
                    int(
                        (int(code[checksum[0] - 1]) + 
                        int(code[checksum[1] - 1])) % 2))
        # Adding 'restored' value
        message.append(_find_most_possible_value(symbol_values_list))
    # Decoding starts from last element and goes down to second
    message.reverse()
    # Decoding first symbol in a initial message
    message.insert(0, _find_first_letter(code, message))
    return "".join([str(el) for el in message])

def _find_most_possible_value(values_list):
    """Finds value that has most entries in a list (with 2 unique elem)."""
    elems = list(set(values_list))
    if len(elems) > 2:
        raise AttributeError("to many errors in coded string")
    first_counter = 0
    for value in values_list:
        if value == elems[0]:
            first_counter += 1
    if first_counter == len(values_list) / 2:
        raise AttributeError("to many errors in coded string")
    elif first_counter < len(values_list) / 2:
        return elems[1]
    else:
        return elems[0]

def _find_first_letter(code, partial_message):
    """Finds first letter of a message."""
    if VERBOSE:
        print "\nFinding m1:\nMock message : " + '0' + ''.join(\
                str(e) for e in partial_message)
    # partially decoded message with 0 as first value
    tmp_message_row = matrix([0] + partial_message)
    # matrix (row) for code
    code_row = matrix([int(el) for el in code])
    # coding matrix for a given message length
    coding_matrix = _generate_coding_matrix(len(partial_message) + 1)
    checking_row = tmp_message_row * coding_matrix
    # obtaining matrix row with possible first element's values
    first_element_row = code_row + checking_row
    # all elements must be in a field F2
    first_element_list = [(el % 2) for el in first_element_row.tolist()[0]]
    if VERBOSE:
        print "Multiplying mock message and matrix...\nAdding the result" \
                + " to encoded word...\nPossible first element's values: " \
                + ', '.join(str(e) for e in first_element_list) + '\n'
    return _find_most_possible_value(first_element_list) 


if __name__ == '__main__':
    from sys import argv

    if len(argv) >= 4:
        if argv[3] == '-v':
            VERBOSE = True
    if len(argv) >= 3:
        mode = argv[1].lower()
        string = argv[2]
    else:
        mode = '-h'
        
    if mode == '-d':
        print decode_message(string)
    elif mode == '-e':
        print encode_message(string) 
    elif mode == '-h' or mode == '-help':
        print """Reed-Muller encoder/decoder (for binary strings).

Usage instructions:
    python rm_coding.py <key> <parameter> [-v]
        -v optional parameter that makes program print details of processing
        <key> could be -d, -e, -h:
            -d  decodes string coded using Reed-Muller code
                parameter is an encoded string
                Example python rm_coding.py -d 10001001

            -e  encodes given binary string using Reed-Muller code
                parameter is a binary string to encode
                Example python rm_coding.py -e 1011

            -h  show this help screen"""
