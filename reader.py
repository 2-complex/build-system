
from bs import *

f = open('buildfile', 'r')
s = f.read()
f.close()

accum = {}
indicator = ' '
target = []
nodeList = []

def list_split(inString):
    return map(lambda x:x.strip(), inString.split(','))

def proc_split(inString):
    return map(lambda x:x.strip(), inString.replace(';', '\n').split('\n'))

for c in s:
    if c in '([{' and indicator == ' ':
        accum[' '] = ''.join(target).strip()
        target = []
        indicator = c
    elif c == {'{':'}', '[':']', '(':')'}.get(indicator, 0):
        accum[c] = ''.join(target)
        indicator = ' '
        target = []
        if c == '}':
            nodeList.append(Node(accum[' '], list_split(accum[')']), list_split(accum[']']), proc_split(accum['}'])))
            accum = {' ':'', ']':''}
    else:
        target.append(c)

resolve(nodeList)


