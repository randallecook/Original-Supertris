#!/usr/bin/python
# Parse a Lightspeed Pascal source file into a human-readable text file

import sys


# byte codes
#TOKEN_COMMENT    = 0x00
TOKEN_PACKED_A   = 0x60
TOKEN_OF         = 0x64
TOKEN_PACKED_R   = 0x68
TOKEN_POINTER    = 0x6A
TOKEN_RECORD     = 0x6C
TOKEN_STRING     = 0x70
TOKEN_ARRAY      = 0x74
TOKEN_EQUALS     = 0x7A
TOKEN_COMMA      = 0x7C
TOKEN_IDENTIFIER = 0x7E
TOKEN_COMMENT    = 0x92
TOKEN_NEWLINE    = 0x94
TOKEN_SEMICOLON  = 0x98
TOKEN_END        = 0x9A
TOKEN_USES       = 0x9E
TOKEN_TYPE       = 0xA4
TOKEN_CONST      = 0xA2
TOKEN_COLON      = 0xA6
TOKEN_LPAREN     = 0xA8
TOKEN_RPAREN     = 0xAA
TOKEN_PROGRAM    = 0xAE
TOKEN_PROCEDURE  = 0xB0
TOKEN_FUNCTION   = 0xB2
TOKEN_VAR        = 0xBA
TOKEN_UNIT       = 0xC6
TOKEN_INTERFACE  = 0xC8
TOKEN_IMPLEMENTATION = 0xCA
TOKEN_CONST_DEF  = 0xCC


def skip(f, n):
    skipped = f.read(n)
    skipped_str = ' '.join(x.encode('hex') for x in skipped)
    #sys.stdout.write('{ Skipped %d bytes: %s }' % (n, skipped_str))


def readString(f):
    n = ord(f.read(1))
    return f.read(n)


def readInt(f):
    n = ord(f.read(1))
    x = 0
    sign = 1
    for i in xrange(n):
        b = ord(f.read(1))
        if b == 4 and i == 0:
            sign = -1
        else:
            x = x * 256 + b
    if sign == -1:
        x -= 65536
    return x


def readArrayRange(f):
    b = ord(f.read(1))
    if b == 0:
        f.read(1)
        return readString(f)
    elif b == 3:
        sign_code = ord(f.read(1))
        x = ord(f.read(1)) * 256
        x += ord(f.read(1))
        if sign_code == 4:
            x -= 65536
        return x
    else:
        printstr('{ unknown array range %02X }' % b)
        return '?'


def printstr(s):
    sys.stdout.write(s)


def processFile(infile):
    while True:
        b = infile.read(1)
        if b == '':
            break
        b = ord(b)
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
        elif b == TOKEN_IMPLEMENTATION:
            skip(infile, 5)
            printstr('implementation')
        elif b == TOKEN_SEMICOLON:
            n = ord(infile.read(1))
            printstr(';\n' * n)
        elif b == TOKEN_NEWLINE:
            n = ord(infile.read(1))
            printstr('\n' * n)
        elif b == TOKEN_USES:
            skip(infile, 1)
            printstr('uses ')
        elif b == TOKEN_IDENTIFIER:
            skip(infile, 1)
            name = readString(infile)
            printstr(name)
        elif b == TOKEN_COMMA:
            n = ord(infile.read(1))
            printstr(', ' * n)
        elif b == TOKEN_CONST:
            skip(infile, 1)
            printstr('const')
        elif b == TOKEN_COMMENT:
            skip(infile, 3)
            comment = readString(infile)
            printstr(comment)
        elif b == TOKEN_CONST_DEF:
            skip(infile, 1)
            name = readString(infile)
            printstr(name)
        elif b == 0x78:
            skip(infile, 11)
        elif b == TOKEN_EQUALS:
            skip(infile, 1)
            x = readInt(infile)
            printstr(' = %d' % x)
        elif b == TOKEN_POINTER:
            skip(infile, 1)
            value = readString(infile)
            printstr(' = ^%s' % value)
        elif b == TOKEN_PACKED_A or b == TOKEN_PACKED_R:
            skip(infile, 1)
            printstr(' = packed ')
        elif b == TOKEN_RECORD:
            skip(infile, 1)
            printstr(' = record\n')
        elif b == TOKEN_TYPE:
            skip(infile, 1)
            printstr('type')
        elif b == TOKEN_ARRAY:
            skip(infile, 1)
            first = readArrayRange(infile)
            last = readArrayRange(infile)
            printstr('array [%s..%s]' % (first, last))
        elif b == TOKEN_OF:
            skip(infile, 1)
            printstr(' of ')
        elif b == TOKEN_COLON:
            n = ord(infile.read(1))
            printstr(': ' * n)
        elif b == TOKEN_END:
            skip(infile, 1)
            printstr('end')
        elif b == TOKEN_STRING:
            skip(infile, 1)
            n = readInt(infile)
            printstr(': String[%d]' % n);
        elif b == TOKEN_VAR:
            skip(infile, 1)
            printstr('var\n')
        elif b == TOKEN_FUNCTION:
            skip(infile, 5)
            name = readString(infile)
            printstr('function %s' % name)
        elif b == TOKEN_LPAREN:
            skip(infile, 1);
            printstr('(')
        elif b == TOKEN_RPAREN:
            skip(infile, 1)
            printstr(')')
        elif b == TOKEN_PROCEDURE:
            skip(infile, 5)
            name = readString(infile)
            printstr('procedure %s' % name)
        else:
            #printstr('{ unknown byte %02X }' % b)
            pass


if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], '<encoded Pascal source file>'
    exit(0)

infilename = sys.argv[1]
outfilename = infilename + '.p'

with open(infilename, 'rb') as infile:
    print '{ Pascal source code from', infilename, '}'
    processFile(infile)

