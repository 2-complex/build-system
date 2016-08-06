
import md5
import commands
import os
import json

def execute_command(line):
    status = commands.getstatusoutput(line)

def multihash(nodes):
    return md5.md5(reduce(str.__add__, map(
            lambda node: node.hash(), nodes), "")).hexdigest()

class File:
    def __init__(self, name, sources, procedure):
        self._name = name
        self._hash_on_file = ""
        self.sources = sources
        self.procedure = procedure

    def name(self):
        return self._name

    def __repr__(self):
        return self.name()

    def procedure_lines(self):
        return filter(bool, map(lambda s: s.strip(), self.procedure))

    def update(self):
        map(lambda node: node.update(), self.sources)
        if self.needs_procedure():
            map(lambda line: execute_command(line), self.procedure_lines())
            self._hash_on_file = self.hash()

    def changed(self):
        return self.hash() != self._hash_on_file;

    def contents(self):
        try:
            f = open(self._name, 'r')
            result = f.read()
            f.close()
        except:
            return ""
        return result

    def _exists(self):
        return os.path.isfile(self._name);

    def hash(self):
        return md5.md5(str(self._exists()) + self.contents()).hexdigest()

    def _source_needs_procedure(self):
        return reduce(bool.__or__, map(lambda x:x.needs_procedure(), self.sources), False)

    def _source_changed(self):
        return reduce(bool.__or__, map(lambda x:x.changed(), self.sources), False)

    def needs_procedure(self):
        return self.changed() or self._source_changed() or self._source_needs_procedure()

    def freeze(self):
        result = {}
        self._freeze_into_map(result)
        return result

    def _freeze_into_map(self, m):
        m[self.name()] = {"file":self.hash(), "sources":multihash(self.sources)}
        map(lambda x:x._freeze_into_map(m), self.sources)

    def thaw(self, m):
        self._hash_on_file = m.get(self.name(), {"file":""})["file"]
        map(lambda x:x.thaw(m), self.sources)

    def map_from_file(self, path):
        try:
            f = open(path, 'r')
            result = json.loads(f.read())
            f.close()
        except:
            return {}
        return result

    def map_to_file(self, m, path):
        f = open(path, 'w')
        f.write(json.dumps(m))
        f.close()

    def save(self, path):
        m = self.map_from_file(path)
        self._freeze_into_map(m)
        self.map_to_file(m, path)

    def restore(self, path):
        m = self.map_from_file(path)
        print "THE MAP " + str(m)
        self.thaw(m)



def get_name_to_file(map_list):
    result = {}
    for rule in map_list:
        if rule['name']:
            result[rule['name']] = File(rule['name'], rule['sources'], rule['procedure'])
    for m in map_list:
        for source in m['sources']:
            if not result.has_key(source):
                result[source] = File(source, [], [])
    return result


def resolve(map_list):
    result = []
    name_to_node = get_name_to_file(map_list)
    for name in name_to_node:
        def resolve_single(n):
            if name_to_node.has_key(n):
                return name_to_node[n]
            return n
        node = name_to_node[name]
        node.sources = map(resolve_single, node.sources)
        result.append(node)
    return {node.name() : node for node in result}


