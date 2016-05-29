
## ABAB = 2
## AAAB = 1
## BAAA = 4
## QUESTION is located at 24572
## BOOKKEEPER = 10743
## NONINTUITIVENESS = 8222334634

def big_loop(word):
    from math import factorial as f

    original_order_list = []
    for char in word:
        original_order_list.append(char)

    set_letters = sorted(list(set(original_order_list)))
    sort_letters = sorted(original_order_list)
    L = len(sort_letters)
    location = 0

    def find_equal(location):
        a = 0
        l = (max((len(set_letters)-1),0))
        for ch in set_letters:

            for x in sort_letters:
                if set_letters == original_order_list and len(original_order_list) ==1:
                    print "only one way to arrange this"
                    location +=1

                if x != original_order_list[a]:
                    print x,"NOT equal",original_order_list[a]
                    print "adding f(l) %s to location" % f(l)
                    location = location + f(l)
                    print "location =",location
                else:
                    print x,"EQUAL to",original_order_list[a]
                    l = l - 1
                    if len(sort_letters)>0:
                        print original_order_list,"original_order_list"
                        print sort_letters,"sort_letters"
                        print set_letters,"set_letters"
                        print "removing %s from sort_letters, original_order_list" % x
                        original_order_list.pop(original_order_list.index(x))
                        sort_letters.pop(sort_letters.index(x))
                        if x in set_letters and x not in original_order_list:
                            set_letters.pop(set_letters.index(x))
                        print original_order_list,"original_order_list"
                        print sort_letters,"sorted list"
                        print set_letters,"set_letters"
                        print "location =",location
                    return sort_letters, location


    def loop_thru_word():
        for char in original_order_list:
            loc = 0
            sort_letters = []
            for a in xrange(len(word)):
                sort_letters, loc = find_equal(loc)
            print "Sequence located at index: %s of permutation" % loc
            return loc
    return loop_thru_word()


big_loop("BOOKKEEPER")
