
## ABAB = 2
## AAAB = 1
## BAAA = 4
## QUESTION is located at 24572
## BOOKKEEPER = 10743
## NONINTUITIVENESS = 8222334634


def find_in_permutation(word):
    from math import factorial

    letters = []
    for char in word:
        letters.append(char)
    abc_letters = sorted(letters)
    set_letters = list(set(letters))
    sorted_set = sorted(set_letters)

    print letters
    print set_letters

    def dom():
        dom = 1
        for ch in set_letters:
            if word.count(ch)>1:
                dom *= factorial(word.count(ch))
        return dom

    def top():
        return factorial(l)

    location = 1
    for ch in letters:
        l = max(1,len(abc_letters)-1)
        print abc_letters
        print "l =    ",l
        print "top() =",top()
        print "dom() =",dom()
        f = top()/dom()
        a = abc_letters.index(ch)
        print "top()/dom() =",f
        print "* abc_letters.index(ch)",f*a
        abc_letters.pop(abc_letters.index(ch))
        location += f*a
        print "location= ",location
        if ch in set_letters:
            set_letters.pop(set_letters.index(ch))
        else:
            continue
    return location
find_in_permutation("BOOKKEEPER")
