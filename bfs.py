import threading

class Rule:
    def __init__(self, target, source, script):
        self.target = target
        self.source = source
        self.script = script

        self.done = threading.event()

    def __repr__(self):
        return self.target + " : " + repr(self.source) + " : " + self.script

    def build(self):
        for i in range(1, 11):
            time.sleep(0.1)
            print("Building " + self.target + " " + str(i))

def make_rule_map(rules):
    return {rule.target: rule for rule in rules}

rules = [
    Rule("poem.txt", ["stanza1.txt", "stanza2.txt"], "cat stanza1.txt stanza2.txt > poem.txt"),
    Rule("stanza1.txt", ["verse1.txt", "chorus.txt"], "cat verse1.txt chorus.txt > stanza1.txt"),
    Rule("stanza2.txt", ["verse2.txt", "chorus.txt"], "cat verse2.txt chorus.txt > stanza1.txt")
]

rulemap = make_rule_map(rules)

class Info:
    def __init__(self, depth, target, source):
        self.depth = depth
        self.source = source
        self.target = target

def dependencies(rulemap, center):
    q = [Info(0, center, rulemap[center].source)]
    answer = []

    while q:
        info = q.pop(0)
        source = info.source
        depth = info.depth

        while len(answer) <= depth:
            answer.append(set())

        answer[depth].add(info.target)

        for t in source:
            if rulemap.has_key(t):
                q.append(Info(depth+1, t, rulemap[t].source))
            else:
                q.append(Info(depth+1, t, []))

    return answer

print dependencies(rulemap, "poem.txt")

import time

afinished = threading.Event()

threading.Thread(target=A).start()
threading.Thread(target=B).start()

