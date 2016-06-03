
## ABAB = 2
## AAAB = 1
## BAAA = 4
## QUESTION is located at 24572
## BOOKKEEPER = 10743
## NONINTUITIVENESS = 8222334634
def find_in_permutation(word):
    from math import factorial
    import time
    start_time = time.time()

    letters = []
    for char in word:
        letters.append(char)
    abc_letters = sorted(letters)
    set_letters = list(set(letters))
    sorted_set = sorted(set_letters)

    def dom():
        dom = 1
        for ch in set_letters:
            if abc_letters.count(ch)>1:
            #    print ch,abc_letters.count(ch)
                dom *= factorial(abc_letters.count(ch))
        return dom


    def top():
        return factorial(l)

    location = 1
    for ch in letters:
        d = dom()

        l = max(1,len(abc_letters)-1)

        f = top()/dom()
        a = abc_letters.index(ch)

        abc_letters.pop(abc_letters.index(ch))
        location += f*a

        if ch in set_letters and ch not in abc_letters:
            set_letters.pop(set_letters.index(ch))
        else:
            continue
    print time.time() - start_time,"seconds"
    return location

find_in_permutation("NONINTUITIVENESS")
