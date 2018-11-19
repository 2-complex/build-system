grammar macros;

program
    : (
    ( buildRule
    | listexp
    | listConcatination
    | listDefinition
    | definition
    | concatination ) ';')*
    ;

buildRule : listConcatination '<' listConcatination '<' concatination;

listDefinition : word '=' listConcatination;

fileList : '[' stringlist ']' ;

listexp
    : word
    | fileList
    ;

listConcatination
    : (listexp ('+' listexp)*)
    ;

definition : prototype '{' concatination '}' ;

call : word '(' explist ')' ;

prototype
    : word '(' wordlist ')'
    ;

concatination
    : exp+
    ;

exp
    : call
    | listexp
    | string
    ;

explist
    : (exp (',' exp)* ','?)?
    ;

wordlist
    : (word (',' word)* ','?)?
    ;

stringlist
    : (string (',' string)* ','?)?
    ;

word
    : WORD
    ;

WORD
    : [a-zA-Z_] [0-9a-zA-Z_]*
    ;

string
    : STRING
    ;

STRING
    : '"' (ESC_Q | ~ ["\\])* '"'
    | '\'' (ESC_S | ~ ['\\])* '\''
    | '`' (ESC_T | ~ [`\\])* '`'
    ;

fragment ESC_Q
    : '\\' (["\\/bfnrt] | UNICODE)
    ;

fragment ESC_S
    : '\\' (['\\/bfnrt] | UNICODE)
    ;

fragment ESC_T
    : '\\' ([`\\/bfnrt] | UNICODE)
    ;

fragment UNICODE
    : 'u' HEX HEX HEX HEX
    ;

fragment HEX
    : [0-9a-fA-F]
    ;

WS
    : [ \t\n\r] + -> skip
    ;
