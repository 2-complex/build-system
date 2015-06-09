
import md5
import commands


class Node:
    def __init__(self, name, sources, targets, procedure):
        self.name = name
        self.sources = sources
        self.targets = targets
        self.procedure = procedure

        self.built_with = ""
    
    def __repr__(self):
	return "name: " + repr(self.name) + "  sources: " + repr(self.sources) + "  targets: " + repr(self.targets) + "  procedure: " + repr(self.procedure)


    def multihash(self, nodes):
        return reduce(str.__add__, map(lambda node: node.hash(), nodes))

    def hash(self):
        return multihash(self.targets)

    def source_hash(self):
        return multihash(self.sources)

    def procedure_lines(self):
        return map(lambda s: s.strip(), self.procedure.split('\n'))

    def update(self):
        map(lambda node: node.update(), self.sources)
        map(lambda line: commands.getstatusoutput(line), self.procedure_lines())


class File:
    def __init__(self, name):
        self.name = name
        self.sources = []
        self.targets = []
        self.procedure = ""

    def __repr__(self):
	return "file: " + repr(self.name)

    def update(self):
        pass

    def contents(self):
        f = open(self.name, 'r')
        result = f.read()
        f.close()
        return result

    def hash(self):
        return md5.md5(self.contents()).hexdigest()


def resolve(nodeList):
    fileNameToFileObj = {}
    for node in nodeList:
        for s in node.sources:
            if not fileNameToFileObj.has_key(s):
            	fileNameToFileObj[s] = File(s)
    for node in nodeList:
        node.sources = map(lambda s:fileNameToFileObj[s], node.sources)

    for n in nodeList:
        print n


testnode.update()


