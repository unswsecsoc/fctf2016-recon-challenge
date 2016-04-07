# testing for now
# written for upcoming CTF

import random
MAX = 100
TRIES = 50

numbers = [0] * 500


for count in xrange(0, TRIES):
    for i in xrange(0, MAX):
        rand = int(random.gauss(MAX, i))
        numbers[rand] += 1

for i in numbers:
    for x in xrange(0, i):
        print "#",
    print


