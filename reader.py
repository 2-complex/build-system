
from bs import *

f = open('buildfile', 'r')
s = f.read()
f.close()

accum = {}
indicator = ' '
target = []
nodeList = []

for c in s:
    if c in '([{':
        accum[' '] = ''.join(target).strip()
        target = []
        indicator = c
    elif c == {'{':'}', '[':']', '(':')'}.get(indicator, 0):
        accum[c] = ''.join(target)
        indicator = ' '
        if c == '}':
            nodeList.append(Node(accum[' '], accum[')'], accum[']'], accum['}']))
        accum = {' ':'', ']':''}
    else:
        target.append(c)

for n in nodeList:
    print n
