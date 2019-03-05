"""
#   Using bytearray to goaround the issues of immutable string
#   Using whitelisting filter
#   Improve the seperation/reponsibility between functions
"""
import sys
import os
import codecs
from collections import Counter
from multiprocessing import Queue, Process, Lock

#Filters
default_filter = set([48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122])
def generate_default_whitelist():
    uppercase = set(x for x in xrange(65, 90 + 1))
    lowercase = set(x for x in xrange(97, 122 + 1))
    digit = set(x for x in xrange(48, 57 + 1))
    uppercase.update(lowercase)
    uppercase.update(digit)
    return uppercase

def wl_tokenize(raw_str, whitelist=default_filter, start_pos=0, end_pos=None):
    output = []
    if end_pos == None:
        end_pos = len(raw_str)

    if (end_pos - start_pos) > 0:
        tok = []
        tok_start = start_pos
        itr = start_pos

        for char in raw_str:
            if int(ord(char)) in whitelist:
                tok.append(raw_str[itr])
            else:
                if itr > tok_start:
                    output.append(''.join(tok))#tok = raw_str[tok_start:itr]
                    tok = []
                    tok_start = itr + 1
                elif itr == tok_start:
                    tok_start = itr + 1
                else:
                    print("Error from wl_tokenize: iterator misposition")
            itr += 1 #increment iterator
        if itr > tok_start:
            output.append(''.join(tok))#tok = raw_str[tok_start:itr]

    return output

def tok_counting(tok_ls):
    return Counter(tok_ls)

def chunk_read_tokenize(file_obj, output, chunk_size=10000):
    """
    Open input file
    Read in a chunk from the file, each chunk is 10Kb as default
    Retain the last word and determine if it is a standalone word according to the next chunk
    Call on tokenizer() to properly remove all illegal characters

    Complexity: Worst Case would be O(n), where n = 1 byte
    """
    #with codecs.open(file_name, encoding='UTF-8', mode='r', errors='ignore') as input_file:
    buf = u''
    start_index = 0
    last_ws_index = 0

    for chunk in iter(lambda:file_obj.read(chunk_size), u''):
        chunk = buf + chunk #   Combining reminder & empty previous buf
        buf = u''           #   put the last whitespace seperated string of characters to the buffer ...
                            #   ... to make sure it is a complete word
        last_ws_index = find_last_ws(chunk)
        if last_ws_index >= 0: #    pass the chunk with complete whitespace seperated words to the tokenizer
            buf = chunk[last_ws_index:]
            wl_tokenizer(chunk, tok_filter, start_pos=0, end_pos=last_ws_index)
        else: # chunk is a continous string with no whitespace, but may require the next chunk to form a complete word
            buf = chunk
    if not len(buf) == 0: # meaning the reminder chunk is a complete word with no whitespace
            #tokenizer(buf, last_ws_index, len(buf),tok_filter, dic)
            wl_tokenizer(buf, tok_filter, start_pos=last_ws_index)

def add_to_queue(item, q, l):
    l.acquire()
    if not q.full():
        q.put(item)
        #print('tokenizer: put into queue', item)
        #print(item)
    l.release()

if __name__ == '__main__':
    filter = generate_default_whitelist()
    str1 = 'hello'
    str2 = 'hello world\n testing testing'
    print(wl_tokenize(str2))
    ls = wl_tokenize(str2)
    print(tok_counting(ls))
