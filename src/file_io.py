#!/usr/bin/env python3

in_file  = None
out_file = None

def read_raw(length):
    global in_file
    return in_file.read(length)

def read_int(length):
    global in_file
    return int.from_bytes(in_file.read(length), 'little')
    
def read_str(length):
    global in_file
    return in_file.read(length).decode('utf-8')
    
def write_raw(b):
    global out_file
    out_file.write(b)
    
def write_int(i, length):
    global out_file
    out_file.write(i.to_bytes(length, 'little'))
    
def write_str(s):
    global out_file
    out_file.write(s.encode())
    
def seek(l):
    global in_file
    in_file.seek(l, 1)

def peek(l):
    global in_file
    data = read_raw(l)

    s = "\n"
    i = 1
    for b in data:
        n = str(b)
        s += ("  " if i < 10 else " ") + str(i) + ": "
        s += ' ' * (3-len(n))  + n + ' '
        s += format(int(n), '#010b').removeprefix('0b')
        s += '\n'
        i += 1

    print(s)
    in_file.seek(-l, 1)
