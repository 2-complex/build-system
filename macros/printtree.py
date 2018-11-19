
import readline

languageName = "macros"

Lexer = getattr(__import__(languageName + "Lexer"), languageName + "Lexer")
Parser = getattr(__import__(languageName + "Parser"), languageName + "Parser")
Listener = getattr(__import__(languageName + "Listener"), languageName + "Listener")

import antlr4
import sys


def printtree(expr):
    def helper(expr, indent):
        if isinstance(expr, antlr4.tree.Tree.TerminalNode):
            print indent + expr.getText()
        else:
            context_type_name = type(expr).__name__[:-7]
            print indent + expr.getText(), context_type_name

            for child in expr.getChildren():
                helper(child, '  ' + indent)
    helper(expr, '')


def main():
    while True:
        text = raw_input('> ')
        lexer = Lexer(antlr4.InputStream(text))
        stream = antlr4.CommonTokenStream(lexer)
        parser = Parser(stream)
        tree = parser.program()
        printtree(tree)
if __name__ == '__main__':
    main()

