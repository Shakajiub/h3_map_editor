#!/usr/bin/env python3

map_file = None
out_file = None

def read_raw(length):
    global map_file
    return map_file.read(length)

def read_int(length):
    global map_file
    return int.from_bytes(map_file.read(length), 'little')
    
def read_str(length):
    global map_file
    return map_file.read(length).decode('utf-8')
    
def write_raw(b):
    global out_file
    out_file.write(b)
    
def write_int(i, length):
    global out_file
    out_file.write(i.to_bytes(length, 'little'))
    
def write_str(s):
    global out_file
    out_file.write(s.encode())
