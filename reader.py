
from bs import *
import re

def list_split(s):
    return map(lambda x:x.strip(), s.split(','))

def proc_split(s):
    return map(lambda x:x.strip(),
        re.sub("\\\\\s*", " ", s).replace(';', '\n').split('\n'))

def read_buildfile(path):
    f = open(path, 'r')
    s = f.read()
    f.close()

    accum = {}
    indicator = ' '
    target = []
    map_list = []

    for c in s:
        if c in '([{' and indicator == ' ':
            if c == '(':
                accum[' '] = ''.join(target).strip()
            target = []
            indicator = c
        elif c == {'{':'}', '[':']', '(':')'}.get(indicator, 0):
            accum[c] = ''.join(target)
            indicator = ' '
            target = []
            if c == '}':
                map_list.append({
                        "name":accum[' '],
                        "sources":list_split(accum[')']),
                        "procedure":proc_split(accum['}'])})
                accum = {' ':'', ']':''}
        else:
            target.append(c)

    return map_list

