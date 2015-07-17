
stanza1.int(stanza1.txt, refrain.txt)
{
    cat stanza1.txt refrain.txt > stanza1.int
}

stanza2.int(stanza2.txt, refrain.txt)
{
    cat stanza2.txt refrain.txt > stanza2.int
}

poem(stanza1.int, stanza2.int)
{
    cat stanza1.int stanza2.int > poem
}


