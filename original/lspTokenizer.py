#!/usr/bin/python
# Parse a Lightspeed Pascal source file into a human-readable text file

import json
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


def errorstr(s):
    sys.stderr.write('ERROR: ' + s + '\n')


def emit(token, name, value):
    sys.stdout.write(json.dumps([int(token), name, value]) + '\n')


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
            emit(b, 'unit', name)
        elif b == TOKEN_PROGRAM:
            skip(infile, 5)
            name = readString(infile)
            emit(b, 'program', name)
        elif b == TOKEN_INTERFACE:
            skip(infile, 5)
            emit(b, 'interface', None)
        elif b == TOKEN_IMPLEMENTATION:
            skip(infile, 5)
            emit(b, 'implementation', None)
        elif b == TOKEN_COND_COMP:
            skip(infile, 3)
            s = readString(infile)
            emit(b, 'CONDITIONAL', s)
        elif b == TOKEN_SEMICOLON:
            n = ord(infile.read(1))
            emit(b, ';', n)
        elif b == TOKEN_NEWLINE:
            n = ord(infile.read(1))
            emit(b, 'NEWLINE', n)
        elif b == TOKEN_USES:
            skip(infile, 1)
            emit(b, 'uses', None)
        elif b == TOKEN_IDENTIFIER:
            skip(infile, 1)
            name = readString(infile)
            emit(b, 'IDENTIFIER_1', name)
        elif b == TOKEN_IDENTIFIER2:
            name = readString(infile)
            emit(b, 'IDENTIFIER_2', name)
        elif b == TOKEN_COMMA:
            n = ord(infile.read(1))
            emit(b, ',', n)
        elif b == TOKEN_CONST:
            skip(infile, 1)
            emit(b, 'const', None)
        elif b == TOKEN_COMMENT:
            skip(infile, 3)
            comment = readString(infile)
            emit(b, 'COMMENT', comment)
        elif b == TOKEN_CONST_DEF:
            skip(infile, 1)
            name = readString(infile)
            emit(b, 'CONST_DEF', name)
        elif b == TOKEN_IS:
            type_code = ord(infile.read(1))
            if type_code == 3:
                x = readInt(infile)
                emit(b, 'IS', x)
            elif type_code == 5:
                skip(infile, 4)
                value = readString(infile)
                emit(b, 'IS', value)
            else:
                errorstr('unknown type code %02X' % type_code)
        elif b == TOKEN_POINTER:
            skip(infile, 1)
            value = readString(infile)
            emit(b, '^', value)
        elif b == TOKEN_PACKED_A:
            skip(infile, 1)
            emit(b, 'packedA', None)
        elif b == TOKEN_PACKED_R:
            skip(infile, 1)
            emit(b, 'packedR', None)
        elif b == TOKEN_RECORD:
            skip(infile, 1)
            emit(b, 'record', None)
        elif b == TOKEN_TYPE:
            skip(infile, 1)
            emit(b, 'type', None)
        elif b == TOKEN_ARRAY:
            skip(infile, 1)
            first = readArrayRange(infile)
            last = readArrayRange(infile)
            emit(b, 'array', (first, last))
        elif b == TOKEN_OF:
            skip(infile, 1)
            emit(b, 'of', None)
        elif b == TOKEN_COLON:
            n = ord(infile.read(1))
            emit(b, ':', n)
        elif b == TOKEN_END:
            skip(infile, 1)
            emit(b, 'end', None)
        elif b == TOKEN_STRING:
            skip(infile, 1)
            n = readInt(infile)
            emit(b, 'String', n);
        elif b == TOKEN_VAR:
            skip(infile, 1)
            emit(b, 'var', None)
        elif b == TOKEN_FUNCTION:
            skip(infile, 5)
            name = readString(infile)
            emit(b, 'function', name)
        elif b == TOKEN_LPAREN:
            skip(infile, 1);
            emit(b, '(1', None)
        elif b == TOKEN_RPAREN:
            skip(infile, 1)
            emit(b, ')1', None)
        elif b == TOKEN_PROCEDURE:
            skip(infile, 5)
            name = readString(infile)
            emit(b, 'procedure', name)
        elif b == TOKEN_BEGIN:
            skip(infile, 9)
            emit(b, 'begin', None)
        elif b == TOKEN_WITH:
            skip(infile, 1)
            emit(b, 'with', None)
        elif b == TOKEN_IF:
            skip(infile, 1)
            emit(b, 'if', None)
        elif b == TOKEN_STATEMENT:
            skip(infile, 1)
            emit(b, 'STATEMENT', None)
        elif b == TOKEN_ELSE:
            skip(infile, 1)
            emit(b, 'else', None)
        elif b == TOKEN_OR:
            emit(b, 'or', None)
        elif b == TOKEN_EQUALS:
            emit(b, '=', None)
        elif b == TOKEN_NOT_EQUALS:
            emit(b, '<>', None)
        elif b == TOKEN_GETS:
            emit(b, ':=', None)
        elif b == TOKEN_LPAREN2:
            emit(b, '(2', None)
        elif b == TOKEN_RPAREN2:
            emit(b, ')2', None)
        elif b == TOKEN_COMMA2 or b == TOKEN_COMMA3:
            emit(b, ',', None)
        elif b == TOKEN_INTEGER:
            type_code = ord(infile.read(1))
            if type_code == 0x04:
                x = ord(infile.read(1)) * 256 * 256 * 256
                x += ord(infile.read(1)) * 256 * 256
                x += ord(infile.read(1)) * 256
                x += ord(infile.read(1))
                emit(b, 'INTEGER', x)
            elif type_code == 0x03:
                x = ord(infile.read(1)) * 256
                x += ord(infile.read(1))
                emit(b, 'INTEGER', x)
            elif type_code == 0x02:
                s = readString(infile)
                sh = ''.join(c.encode('hex') for c in s)
                printstr('trouble: %s --> %s' % (s, sh))
                emit(b, 'INTEGER', sh)
            elif type_code == 0x05:
                s = readString(infile)
                emit(b, 'INTEGER', s)
            elif type_code == 0x0A:
                skip(infile, 2)
                s = readString(infile)
                emit(b, 'INTEGER', s)
            else:
                errorstr('unknown number code %02X' % type_code)
        elif b == TOKEN_TIMES:
            emit(b, '*', None)
        elif b == TOKEN_MOD:
            emit(b, 'mod', None)
        elif b == TOKEN_SLASH:
            emit(b, '/', None)
        elif b == TOKEN_DIV:
            emit(b, 'div', None)
        elif b == TOKEN_SPACE:
            emit(b, 'SPACE', None)
        elif b == TOKEN_LESS_EQUAL:
            emit(b, '<=', None)
        elif b == TOKEN_GR_EQUAL:
            emit(b, '>=', None)
        elif b == TOKEN_LBRACKET:
            emit(b, '[', None)
        elif b == TOKEN_RBRACKET:
            emit(b, ']', None)
        elif b == TOKEN_IN:
            emit(b, 'in', None)
        elif b == TOKEN_RANGE:
            emit(b, '..', None)
        elif b == TOKEN_PLUS:
            emit(b, '+', None)
        elif b == TOKEN_MINUS:
            emit(b, '-', None)
        elif b == TOKEN_NULL:
            emit(b, 'null', None)
        elif b == TOKEN_HYPHEN:
            emit(b, '-', None)
        elif b == TOKEN_CASE:
            skip(infile, 1)
            emit(b, 'case', None)
        elif b == TOKEN_DO:
            skip(infile, 1)
            emit(b, 'do', None)
        elif b == TOKEN_FOR:
            skip(infile, 1)
            s = readString(infile)
            emit(b, 'for', s)
        elif b == TOKEN_AT:
            emit(b, '@', None)
        elif b == TOKEN_WHILE:
            skip(infile, 1)
            emit(b, 'while_1', None)
        elif b == TOKEN_WHILE2:
            skip(infile, 1)
            emit(b, 'while_2', None)
        elif b == TOKEN_DEFAULT:
            skip(infile, 1)
            emit(b, 'default', None)
        elif b == TOKEN_NOT:
            emit(b, 'not', None)
        elif b == TOKEN_AND:
            emit(b, 'and', None)
        elif b == TOKEN_LESS_THAN:
            emit(b, '<', None)
        elif b == TOKEN_GREATER_THAN:
            emit(b, '>', None)
        elif b == TOKEN_DOT:
            emit(b, '.', None)
        elif b == TOKEN_DEREFERENCE:
            emit(b, '^', None)
        elif b == TOKEN_TO:
            emit(b, 'to', None)
        elif b == TOKEN_DOWN_TO:
            emit(b, 'down to', None)
        elif b == TOKEN_PERIOD:
            skip(infile, 3)
            emit(b, '.', None)
        else:
            errorstr('unknown byte %02X' % b)
            pass


if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], '<encoded Pascal source file>'
    exit(0)

infilename = sys.argv[1]
outfilename = infilename + '.p'

with open(infilename, 'rb') as infile:
    processFile(infile)

