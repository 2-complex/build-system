
import reader
import bs

m = reader.read_buildfile('buildfile')
l = bs.resolve(m)

def display():
    for name in l:
        i = l[name]
        print i.name(), i._hash_on_file, i.hash(), i.changed(), i.needs_procedure()


l['poem'].restore("history.json")

print "before update"
display()
l['poem'].update()
print "after update"
display()

l['poem'].save("history.json")
