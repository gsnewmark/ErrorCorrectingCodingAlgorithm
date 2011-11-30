# -*- coding: utf-8 -*- 
"""
Bunch of functions that implements Hamming coding algorithm. 
"""

from numpy import matrix

VERBOSE = False 

def encode_message(r, message):
    """Encodes given message using Hamming code."""
    return ''.join([str(v) for v in _find_coded_message(r, message)])

def decode_message(r, code):
    """Decodes code encoded using Hamming code."""
    return ''.join(str(v) for v in _find_initial_message(r, code))

def _generate_checking_matrix(r):
    """Generates checking matrix for a given r parameter of algorithm."""
    # number of rows in checking matrix
    n = 2 ** r - 1
    # forming list of matrix rows
    result = []
    for i in range(1, n + 1):
        result.append(bin(i))
    # padding all strings to make their lengthes equal 
    result = [s[2:].rjust(r, '0') for s in result]
    # transforming result to list of lists
    result = [[int(c) for c in s] for s in result]
    # creating matrix
    result_matrix = matrix(result)
    if VERBOSE:
        print "Checking matrix:\n" + str(result_matrix)
    return result_matrix

def _get_checksums_indices(r):
    """Returns indeces of checksums in a coded phrase."""
    return [(2 ** a) - 1 for a in range(0, r)]

def _find_coded_message(r, message):
    """Find cheksums for a given message."""
    # generates coded message template
    coded_message = _find_coded_message_template(r, message)
    if VERBOSE:
        print "Coded message template " + str(coded_message)
    # gets a list of columns which corresponds to checksums when multiplying
    # matrices
    columns_for_checksums = _generate_checking_matrix(r).getT().tolist()
    if VERBOSE:
            print "\nFinding checksums: "
    # fill in the 'blanks' in a coded message
    for column in columns_for_checksums:
        current_checksum_index = -1
        current_checksum_value = 0
        for i in range(0, len(column)):
            if column[i] == 1 and str(coded_message[i]).startswith('k'): 
                # found index of checksum for given column
                current_checksum_index = i
                if VERBOSE:
                    print "Checksum index in coded message = " + str(i)
            elif column[i] == 1:
                if VERBOSE:
                    print "Adding template element from position " + str(i)
                # simulating multiplication of matrix column and vector
                current_checksum_value += coded_message[i]
        # value of checksum in a field of 2
        coded_message[current_checksum_index] = current_checksum_value % 2
        if VERBOSE:
            print "Checksum's value is " + \
                    str(coded_message[current_checksum_index]) + '\n'
    return coded_message

def _find_coded_message_template(r, message):
    """Generates coded message with 'k' instead of checksum values."""
    # indices of checksums in coded word   
    checksums_indices = _get_checksums_indices(r)
    if VERBOSE:
        print "Indices of checksums " + str(checksums_indices)
    # indeces of initial word's symbols
    message_indeces = [a for a in range(0, len(message))]
    # forming coded message (with 'k' instead of actual cheksum's values)
    coded_message = []
    chk_index = 0
    for i in range (0, 2 ** r - 1):
        if i in checksums_indices:
            coded_message.append('k' + str(chk_index))
            chk_index += 1
        else:
            coded_message.append(int(message[message_indeces.pop(0)]))
    return coded_message

def _find_initial_message(r, code):
    """Restores initial message from a code. """
    # list representation of a coded string
    code_list = [int(s) for s in code]
    # obtain index of error in a code
    error_index = _find_error_index(r, code_list)
    # correct the error
    if error_index > -1:
        code_list[error_index] = (code_list[error_index] + 1) % 2
    if VERBOSE:
        print "\nCorrected coded message: " + ''.join([str(e) for e in \
            code_list])
    # get indeces of checksums in a coded word   
    checksums_indices = _get_checksums_indices(r)
    if VERBOSE:
        print "Indices of checksums " + str(checksums_indices) + '\n'
    # restore initial message (remove checksums)
    initial_message = [code_list[i] for i in range(0, len(code_list)) if \
            i not in checksums_indices]
    return initial_message 

def _find_error_index(r, code_list):
    """Finds index of element in coded word that is incorrect."""
    # generate checking matrix
    checking_matrix = _generate_checking_matrix(r)
    # transform code string to vector
    code_vector = matrix(code_list)
    # get error index
    error_index = int(''.join([str(e % 2) for e in (code_vector * \
            checking_matrix).tolist()[0]]), 2) - 1
    if VERBOSE:
        if error_index != -1:
            print "\nError at position " + str(error_index)
        else:
            print "\nCoded message is error-free"
    return error_index
    

if __name__ == '__main__':
    from sys import argv

    if len(argv) >= 5:
        if argv[4] == '-v':
            VERBOSE = True
    if len(argv) >= 4:
        mode = argv[1].lower()
        r = argv[2]
        string = argv[3]
    else:
        mode = '-h'
        
    if mode == '-d':
        print decode_message(int(r), string)
    elif mode == '-e':
        print encode_message(int(r), string) 
    elif mode == '-h' or mode == '-help':
        print """Hamming encoder/decoder (for binary strings).

Usage instructions:
    python hamming_coding.py <key> <r> <parameter> [-v]
        -v optional parameter that makes program print details of processing
        <r> is an r parameter of algorithm (k = 2^r - r - 1, n = 2^r - 1)
        <key> could be -d, -e, -h:
            -d  decodes string coded using Hamming code
                parameter is an encoded string
                Example python rm_coding.py -d 3 1101001

            -e  encodes given binary string using Hamming code
                parameter is a binary string to encode
                Example python rm_coding.py -e 3 0001

            -h  show this help screen"""

