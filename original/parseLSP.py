#!/usr/bin/python
# Parse a Lightspeed Pascal source file into a human-readable text file

import sys
from tokens import *


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
        #printstr('{read %02X}' % b)
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
        elif b == TOKEN_COND_COMP:
            skip(infile, 3)
            s = readString(infile)
            printstr('{CONDITIONAL:} %s\n' % s)
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
        elif b == TOKEN_IDENTIFIER2:
            name = readString(infile)
            printstr(name)
        elif b == TOKEN_COMMA:
            n = ord(infile.read(1))
            printstr(', ' * n)
        elif b == TOKEN_CONST:
            skip(infile, 1)
            printstr('const\n')
        elif b == TOKEN_COMMENT:
            skip(infile, 3)
            comment = readString(infile)
            printstr('%s\n' % comment)
        elif b == TOKEN_CONST_DEF:
            skip(infile, 1)
            name = readString(infile)
            printstr('%s =' % name)
        elif b == TOKEN_IS:
            type_code = ord(infile.read(1))
            if type_code == 3:
                x = readInt(infile)
                printstr(' %d' % x)
            elif type_code == 5:
                skip(infile, 4)
                value = readString(infile)
                printstr(value)
            else:
                printstr('{ unknown type code %02X }' % type_code)
        elif b == TOKEN_POINTER:
            skip(infile, 1)
            value = readString(infile)
            printstr(' ^%s' % value)
        elif b == TOKEN_PACKED_A or b == TOKEN_PACKED_R:
            skip(infile, 1)
            printstr(' packed ')
        elif b == TOKEN_RECORD:
            skip(infile, 1)
            printstr(' record\n')
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
            printstr('String[%d]' % n);
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
        elif b == TOKEN_BEGIN:
            skip(infile, 9)
            printstr('\nbegin\n')
        elif b == TOKEN_WITH:
            skip(infile, 1)
            printstr('with ')
        elif b == TOKEN_IF:
            skip(infile, 1)
            printstr('\nif ')
        elif b == TOKEN_STATEMENT:
            skip(infile, 1)
            printstr('\n')
        elif b == TOKEN_ELSE:
            skip(infile, 1)
            printstr('\nelse\n')
        elif b == TOKEN_OR:
            printstr(' or ')
        elif b == TOKEN_EQUALS:
            printstr(' = ')
        elif b == TOKEN_NOT_EQUALS:
            printstr(' <> ')
        elif b == TOKEN_GETS:
            printstr(' := ')
        elif b == TOKEN_LPAREN2:
            printstr('(')
        elif b == TOKEN_RPAREN2:
            printstr(')')
        elif b == TOKEN_COMMA2 or b == TOKEN_COMMA3:
            printstr(', ')
        elif b == TOKEN_INTEGER:
            type_code = ord(infile.read(1))
            if type_code == 0x04:
                x = ord(infile.read(1)) * 256 * 256 * 256
                x += ord(infile.read(1)) * 256 * 256
                x += ord(infile.read(1)) * 256
                x += ord(infile.read(1))
                printstr('%d' % x)
            elif type_code == 0x03:
                x = ord(infile.read(1)) * 256
                x += ord(infile.read(1))
                printstr('%d' % x)
            elif type_code == 0x02:
                s = readString(infile)
                printstr('\'%s\'' % s)
            elif type_code == 0x05:
                s = readString(infile)
                printstr('"%s"' % s)
            elif type_code == 0x0A:
                skip(infile, 2)
                s = readString(infile)
                printstr(s)
            else:
                printstr('unknown number code %02X' % type_code)
        elif b == TOKEN_TIMES:
            printstr(' * ')
        elif b == TOKEN_MOD:
            printstr(' mod ')
        elif b == TOKEN_SLASH:
            printstr(' / ')
        elif b == TOKEN_DIV:
            printstr(' div ')
        elif b == TOKEN_SPACE:
            printstr(' ')
        elif b == TOKEN_LESS_EQUAL:
            printstr(' <= ')
        elif b == TOKEN_GR_EQUAL:
            printstr(' >= ')
        elif b == TOKEN_LBRACKET:
            printstr('[')
        elif b == TOKEN_RBRACKET:
            printstr(']')
        elif b == TOKEN_IN:
            printstr(' in ')
        elif b == TOKEN_RANGE:
            printstr('..')
        elif b == TOKEN_PLUS:
            printstr(' + ')
        elif b == TOKEN_MINUS:
            printstr(' - ')
        elif b == TOKEN_NULL:
            printstr('null')
        elif b == TOKEN_HYPHEN:
            printstr('-')
        elif b == TOKEN_CASE:
            skip(infile, 1)
            printstr('case ')
        elif b == TOKEN_DO:
            skip(infile, 1)
            printstr('do\n')
        elif b == TOKEN_FOR:
            skip(infile, 1)
            s = readString(infile)
            printstr('for %s := ' % s)
        elif b == TOKEN_AT:
            printstr('@')
        elif b == TOKEN_WHILE or b == TOKEN_WHILE2:
            skip(infile, 1)
            printstr('\nwhile ')
        elif b == TOKEN_DEFAULT:
            skip(infile, 1)
            printstr('default')
        elif b == TOKEN_NOT:
            printstr(' not ')
        elif b == TOKEN_AND:
            printstr(' and ')
        elif b == TOKEN_LESS_THAN:
            printstr(' < ')
        elif b == TOKEN_GREATER_THAN:
            printstr(' > ')
        elif b == TOKEN_DOT:
            printstr('.')
        elif b == TOKEN_DEREFERENCE:
            printstr('^')
        elif b == TOKEN_TO:
            printstr(' to ')
        elif b == TOKEN_DOWN_TO:
            printstr(' down to ')
        elif b == TOKEN_PERIOD:
            skip(infile, 3)
            printstr('.\n')
        else:
            printstr('{ unknown byte %02X }' % b)
            pass


if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], '<encoded Pascal source file>'
    exit(0)

infilename = sys.argv[1]
outfilename = infilename + '.p'

with open(infilename, 'rb') as infile:
    print '{ Pascal source code from', infilename, '}'
    processFile(infile)

