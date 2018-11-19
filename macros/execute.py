import readline

languageName = "macros"

Lexer = getattr(__import__(languageName + "Lexer"), languageName + "Lexer")
Parser = getattr(__import__(languageName + "Parser"), languageName + "Parser")
Listener = getattr(__import__(languageName + "Listener"), languageName + "Listener")

import antlr4
import sys


class Rule:
    def __init__(self, target, source, script):
        self.target = target
        self.source = source
        self.script = script

    def __repr__(self):
        return str(self.target) + " < " + str(self.source) + " < " + self.script

class Macro:
    def __init__(self, prototype, body):
        i = 0
        self.arguments = []
        self.body = body

        for arg in prototype.getChild(2).getChildren():
            if i%2 == 0:
                self.arguments.append(arg.getText())
            i+=1

    def __repr__(self):
        return "(" + ",".join(self.arguments) + ") " + self.body.getText()


class FileList:
    def __init__(self, files):
        i = 0
        self.files = files

    def __add__(self, other):
        return FileList(self.files + other.files)

    def __str__(self):
        return " ".join(self.files)

    def __repr__(self):
        return "[" + ",".join(self.files) + "]"


def evalString(literal):
    return eval(literal)


class Environment:
    def __init__(self):
        self.macros = {}
        self.filelists = {}
        self.rules = []
        self.stack = []

    def get(self, word):
        for m in self.stack:
            if m.has_key(word):
                return m[word]
        if self.filelists.has_key(word):
            return self.filelists[word]

        return "<UNDEFINED>"

    def evaluate(self, expr):
        def helper(expr):
            if isinstance(expr, antlr4.tree.Tree.TerminalNode):
                print("terminal, whatever that means")
            else:
                context_type_name = type(expr).__name__[:-7]

                if context_type_name == "Program":
                    i = 0
                    for c in expr.getChildren():
                        if i%2==0:
                            helper(c)
                        i+=1
                    return

                if context_type_name == "ListDefinition":
                    varname = expr.getChild(0).getText()
                    l = helper(expr.getChild(2))
                    self.filelists[varname] = l
                    return "List defined: " + varname + " = " + repr(l)

                if context_type_name == "Definition":
                    prototype = expr.getChild(0)
                    body = expr.getChild(2)
                    macro = Macro(prototype, body)
                    self.macros[prototype.getChild(0).getText()] = macro
                    return "Macro defined: " + repr(macro)

                if context_type_name == "FileList":
                    i = 0
                    files = []
                    for child in expr.getChild(1).getChildren():
                        if i%2==0:
                            files.append(evalString(child.getText()))
                        i+=1
                    return FileList(files)

                if context_type_name == "ListConcatination":
                    i = 0
                    accum = FileList([])
                    for child in expr.getChildren():
                        if i%2==0:
                            accum += helper(child)
                        i+=1
                    return accum

                if context_type_name == "String":
                    return evalString(expr.getText())

                if context_type_name == "Word":
                    return self.get(expr.getText())

                if context_type_name == "Call":
                    macroName = expr.getChild(0).getText()
                    if not self.macros.has_key(macroName):
                        return "<MACRO NOT FOUND>"

                    macro = self.macros[macroName]

                    values = []
                    i = 0
                    for c in expr.getChild(2).getChildren():
                        if i%2==0:
                            values.append(str(helper(c)))
                        i+=1

                    n = len(values)
                    if len(values) != len(macro.arguments):
                        return "<ARGUMENTS DID NOT MATCH>"

                    stackFrame = {}
                    for i in range(0, n):
                        stackFrame[macro.arguments[i]] = values[i]

                    self.stack.append(stackFrame)
                    result = helper(macro.body)
                    self.stack.pop()
                    return result

                if context_type_name == "Concatination":
                    return reduce(str.__add__, map(helper, expr.getChildren()))

                if context_type_name == "BuildRule":
                    rule = Rule(
                        helper(expr.getChild(0)),
                        helper(expr.getChild(2)),
                        helper(expr.getChild(4)) )
                    self.rules.append(rule)
                    return "rule: " + repr(rule)

                return helper(expr.getChild(0))

        return helper(expr)


def readInFile(name):
    with open(name) as f:
        return f.read()


def textToTree(text):
    lexer = Lexer(antlr4.InputStream(text))
    stream = antlr4.CommonTokenStream(lexer)
    parser = Parser(stream)
    return parser.program()


def main():
    import sys

    env = Environment()

    if len(sys.argv) > 1:
        env.evaluate(textToTree(readInFile(sys.argv[1])))

    for r in env.rules:
        print r

    while True:
        text = raw_input('> ')
        if text == "":
            continue

        print( env.evaluate(textToTree(text)) )


if __name__ == '__main__':
    main()

