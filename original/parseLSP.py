#!/usr/bin/python
# Parse a Lightspeed Pascal source file into a human-readable text file

import sys


# byte codes
TOKEN_COMMENT    = 0x00
TOKEN_COMMA      = 0x7C
TOKEN_USES       = 0x7E
TOKEN_SPACE      = 0x92
TOKEN_NEWLINE    = 0x94
TOKEN_SEMICOLON  = 0x98
TOKEN_TAB        = 0x9E
TOKEN_CONST      = 0xA2
TOKEN_PROGRAM    = 0xAE
TOKEN_UNIT       = 0xC6
TOKEN_INTERFACE  = 0xC8


def skip(f, n):
    skipped = f.read(n)
    skipped_str = ' '.join(x.encode('hex') for x in skipped)
    print '{ Skipped', n, 'bytes:', skipped_str, ' }'


def readString(f):
    n = ord(f.read(1))
    return f.read(n)


def printstr(s):
    sys.stdout.write(s)


def processFile(infile, outfile):
    x = 0
    while True:
        b = infile.read(1)
        if b == '':
            break
        b = ord(b)
        x += 1
        #print 'read', hex(b)
        if b == TOKEN_UNIT:
            skip(infile, 5)
            name = readString(infile)
            printstr('unit %s' % name)
        elif b == TOKEN_PROGRAM:
            skip(infile, 5)
            name = readString(infile)
            printstr('program %s' % name)
        elif b == TOKEN_INTERFACE:
            skip(infile, 5)
            printstr('interface')
        elif b == TOKEN_SEMICOLON:
            n = ord(infile.read(1))
            printstr(';' * n)
        elif b == TOKEN_NEWLINE:
            n = ord(infile.read(1))
            printstr('\n' * n)
        elif b == TOKEN_TAB:
            n = ord(infile.read(1))
            printstr('\t' * n)
        elif b == TOKEN_USES:
            skip(infile, 1)
            name = readString(infile)
            printstr('uses %s' % name)
        elif b == TOKEN_COMMA:
            n = ord(infile.read(1))
            printstr(',' * n)
        elif b == TOKEN_CONST:
            skip(infile, 1)
            printstr('const')
        elif b == TOKEN_SPACE:
            n = ord(infile.read(1))
            printstr(' ' * n)
        elif b == TOKEN_COMMENT:
            skip(infile, 1)
            comment = readString(infile)
            printstr(comment)
        else:
            print '{ unknown byte %02X }' % b
    print '{ read', x, 'bytes }'


if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], '<encoded Pascal source file>'
    exit(0)

infilename = sys.argv[1]
outfilename = infilename + '.p'

with open(infilename, 'rb') as infile:
    with open(outfilename + '.p', 'w') as outfile:
        print '{ Parsing', infilename, 'into', outfilename, '}'
        processFile(infile, outfile)

