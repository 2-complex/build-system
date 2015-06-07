
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
	return "name: " + repr(self.name) + "sources: " + repr(self.sources) + "targets: " + repr(self.targets) + "procedure: " + repr(self.procedure)


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

    def update(self):
        pass

    def contents(self):
        f = open(self.name, 'r')
        result = f.read()
        f.close()
        return result

    def hash(self):
        return md5.md5(self.contents()).hexdigest()


buildline = "c++ test.cpp -I/usr/local/Cellar/sdl/1.2.15/include/SDL /usr/local/Cellar/sdl/1.2.15/lib/libSDL.a /usr/local/Cellar/sdl/1.2.15/lib/libSDLmain.a -framework Cocoa -framework OpenGL -framework AudioUnit -framework IOKit -framework Carbon -o test"
testnode = Node( "test", [File("test.cpp")], [File("test")], buildline )

testnode.update()

