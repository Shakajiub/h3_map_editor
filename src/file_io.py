#!/usr/bin/env python3

in_file  = None
out_file = None

def read_raw(length: int) -> bytes:
    global in_file
    return in_file.read(length)

def read_int(length: int) -> int:
    global in_file
    return int.from_bytes(in_file.read(length), 'little')

def read_str(length: int) -> str:
    global in_file
    return in_file.read(length).decode('utf-8')

def read_bits(length: int) -> list:
    temp_bits = []
    raw_data  = read_raw(length)

    for c in raw_data:
        bits = format(int(c), '#010b').removeprefix('0b')[::-1]
        for b in bits:
            temp_bits.append(1 if b == '1' else 0)
    
    return temp_bits

def write_raw(data: bytes):
    global out_file
    out_file.write(data)

def write_int(data: int, length: int) -> None:
    global out_file
    out_file.write(data.to_bytes(length, 'little'))

def write_str(data: str) -> None:
    global out_file
    out_file.write(data.encode())

def write_bits(data: list) -> None:
    for i in range(0, len(data), 8):
        s = ""
        for b in range(8):
            s += '1' if data[i + b] else '0'
        write_int(int(s[::-1], 2), 1)

def seek(length: int) -> None:
    global in_file
    in_file.seek(length, 1)

def peek(length: int) -> None:
    global in_file
    data = read_raw(length)

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
    in_file.seek(-length, 1)
