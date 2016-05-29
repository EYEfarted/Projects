## ABAB = 2
## AAAB = 1
## BAAA = 4
## QUESTION is located at 24572
## BOOKKEEPER = 10743
## NONINTUITIVENESS = 8222334634

word = "BOOKKEEPER"
original_order_list = []
for char in word:
    original_order_list.append(char)

my_sorted_list = sorted(original_order_list)

set_letters = list(set(original_order_list))
print set_letters

r = len(set_letters)
n = len(my_sorted_list)


def factorial(num):
    x = 0
    f = 1
    for x in xrange(num):
        f = ((x+1)*f)
    return f


def count_index():

    for target_letter in original_order_list:
        if len(my_sorted_list)>1:
            target_index = my_sorted_list.index(target_letter)
            y = 1

            x = 0

            if my_sorted_list[0] == my_sorted_list[y]:
                y +=1

                index_sorted_letters = my_sorted_list.index(target_letter)

                print "target letter index", index_sorted_letters
                print "number of duplicate letters in sorted", y+1


                counted_index = target_index-my_sorted_list.count(my_sorted_list[0])
                print "returning this",target_index-my_sorted_list.count(my_sorted_list[0])

                print "Y = ", y
                return counted_index

            else:
                print "First 2 in sorted sequence not alike", target_index
                return target_index

        elif len(my_sorted_list)==1:
            return 0
        else:
            continue
        print "returning", max(0, counted_index)
        return max(0, counted_index)
# print count_index()

def add_up_location(insert_list):
    # start at position 1 cause there is no position 0
    location = 1

    for ch in word:
        i = original_order_list[0]
        print i, "Is what we are gonna be removing"

        combinations = factorial(len(insert_list)-1)
        adjusted_index = count_index()

## there is MATH here
        loc = combinations*adjusted_index
        print loc,"combinations until target"
        location += loc
        print "location", location


        my_sorted_list.remove(i)
        print "Removing",i,"from Sorted list"
        print "Sorted list", my_sorted_list

        original_order_list.pop(0)
        print "Removing",i,"from Original sequence"
        print "Original sequence",original_order_list



print add_up_location(my_sorted_list)
