"""
Sometimes I ensure that variants are within specifications while making them.
In 8+, however, I let variants be whatever, but only add them if they are
within specifications. This is much easier to code, and can take on a simpler
format, but will likely run more slowly as we will have to generate more
variants before they randomly fit the specifications.
"""

import numpy as np
from random import randint, choice, shuffle

def remove_indices(options, variant_list):
    '''
    If the variants in a level can have different missing variables, then we
    want to have at most three questions with the same missing variable in a
    row.
    '''
    maxRepeats = 3
    variants = []
    if options == 'AB':         missing = [0, 1]
    elif options == 'ABC':      missing = [0, 1, 2]
    elif options == 'AC':       missing = [0, 2]
    else:
        # perhaps the option was invalid
        return None
    # don't have 4 in a row all missing A or all missing B
    # 30% liklihood of having 3 in a row
    missing *= maxRepeats
    shuffle(missing)
    # once maximums have been satisfied, repeat
    missing += missing[:10 - len(missing)]

    for index in range(len(variant_list)):
        # variant_list may be filled with zipped objects
        variant = list(variant_list[index])

        ''' NOTE:
        may ruin pattern, but only out of necessity
        '''
        if variant.count(0) > 1:
            variant[variant.index(0)] = None
        else:
            variant[missing[index]] = None
        variants.append(variant)
    return variants

def repeatList(B, minimum):
    '''
    We need to see all values in B exactly minimum times before we can repeat
    them any further. Once this condition has been satisfied repeat the list
    until it has 10 values.
    This value takes the values in B and returns a shuffled list of length 10
    that satisfies the above repetition condition.
    '''
    lst = B * minimum
    shuffle(lst)
    lst += lst[:10 - len(lst)]
    return lst

def comm_unique(a, b, c, variants):
    return all(([a, b, c] not in variants, [b, a, c] not in variants))

def mult_variants_from_list(B, minimum, low=1, high=10, zerosLeft=0, C=True):
    variants = []
    while len(variants) != 10:
        ''' NOTE:
        reset see once all values are used
        when reset occurs, this could lead to at most 4 questions
        in a row that share a multiplicant

        We want to see all values in inputs minimum times before we see any of them
        more than minimum times.
        '''
        to_see = B * minimum
        while len(to_see) != 0 and len(variants) != 10:
            b = choice(to_see)
            to_see.remove(b)

            while True:
                a = randint(0 if zerosLeft else max(low, 1), high)
                if not (a in B and a not in to_see):
                    if comm_unique(a, b, a * b, variants):
                        break

            if a == 0:      zerosLeft -= 1
            if a in to_see: to_see.remove(a)
            # is the product/sum set to None?
            variants.append([a, b, a * b if C else None])

    return variants


def lvl1(operation):
    variants = []

    if operation == '+':
        # want to loop through adding by 0 to 9 for diverse variants
        A = np.arange(10)
        variants = list(zip(A, 10 - A, [10] * 10))
        shuffle(variants)

        # by default either A or B is missing
        variants = remove_indices('AB', variants)

    elif operation == '-':
        ''' NOTE:
        0 - 0 is currently possible
        '''
        B = np.arange(10)
        A = [randint(b, 10) for b in B]
        variants=list(zip(A, B, A - B))
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        variants = mult_variants_from_list([1, 2, 5, 10], minimum=2, C=False)

    elif operation in (':', '/'):
        zerosLeft = 2
        B = repeatList([1, 2, 5, 10], 2)

        for b in B:
            while True:
                a = b * randint(0 if zerosLeft else 1, 10)
                variant = [a, b, None]

                if variant not in variants:
                    variants.append(variant)
                    if a == 0:  zerosLeft -= 1
                    break
    return variants

def lvl2(operation):
    variants = []

    if operation == '+':
        zerosLeft = 2

        while len(variants) != 10:
            ''' NOTE:
            this does not allow for same A, B, C even if different missing index
            '''
            a = randint(0, 20) if zerosLeft else randint(1, 19)
            b = randint(max(10 - a, 0 if zerosLeft else 1), 20 - a)

            if comm_unique(a, b, a + b, variants):
                variants.append([a, b, a + b])
                if 0 in (a, b): zerosLeft -= 1

        shuffle(variants)
        variants = remove_indices('ABC',variants)

    elif operation == '-':
        """ NOTE:
        currenly can have B=2 or B=12 not both
        """
        B = np.arange(10)

        for i in range(len(B)):
            B[i] += choice((0, 10))

        A = [randint(max(b, 11), 20) for b in B]
        variants = list(zip(A, B, A - B))
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        variants = mult_variants_from_list([0, 4, 8], minimum=3, C=False)

    elif operation in (':', '/'):
        B = repeatList([4, 8], 3)

        for b in B:
            while True:
                variant = [b * randint(1, 10), b, None]
                if variant not in variants:
                    variants.append(variant)
                    break

    return variants

def lvl3(operation):
    variants = []

    if operation == '+':
        zerosLeft = 2

        while len(variants) != 10:
            a = 10 * randint(2, 9)
            b = choice((randint(0 if zerosLeft else 1, 9), 10 * randint(1, 10 - a / 10)))

            if comm_unique(a, b, a + b, variants):
                variants.append(choice(([a, b, a + b], [b, a, a + b])))
                if b == 0:  zerosLeft -= 1

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        # B <= 80 (need C >= 20)
        B = np.arange(1, 8) * [choice((1, 10)) for i in range(7)]
        B = np.append(B, [8, 9])
        B = np.append(B, choice((randint(1, 7) * choice((1, 10)), 8, 9)))

        for b in B:
            while True:
                a = 10 * randint(max(3, b / 10), 10)
                if [a,b,a-b] not in variants:
                    variants.append([a, b, a - b])
                    break

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        variants = mult_variants_from_list([3, 6, 9], minimum=3, zerosLeft=2, C=False)

    elif operation in (':', '/'):
        B = repeatList([3, 6, 9], 3)

        for b in B:
            while True:
                variant = [b * randint(1, 10), b, None]
                if variant not in variants:
                    variants.append(variant)
                    break

    return variants

def lvl4(operation):
    variants = []

    if operation == '+':
        ''' NOTE:
        Charles said to trust examples over ALGO, but ALGO is quite specific
        about no b = 0 and b = 0 in one example.

        I said no b = 0 since the MIN for this is 0 anyway
        '''
        zerosLeft = 2

        while len(variants) != 10:
            a = 10 * randint(2, 9) + randint(1, 8)
            # b = randint(0 if zerosLeft else 1, 9 - a%10)
            b = randint(1, 9 - a%10)

            if comm_unique(a, b, a + b, variants):
                variants.append(choice(([a, b, a + b], [b, a, a + b])))
                # if b is 0:  zerosLeft -= 1

        variants = remove_indices('ABC', variants)

    elif operation == '-':
        ''' NOTE:
        I have currently allowed for b = 0 once
        '''
        B = np.arange(10)
        A = np.array([10 * randint(2, 9) + randint(b, 9) for b in B])
        variants = list(zip(A, B, A - B))
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        A = np.arange(10)
        variants = list(zip(A, [7] * 10, [None] * 10))
        shuffle(variants)

    elif operation in (':', '/'):
        A = 7 * np.arange(10)
        variants = list(zip(A, [7] * 10, [None] * 10))
        shuffle(variants)
    return variants

def lvl5(operation):
    variants = []

    if operation == '+':
        while len(variants) != 10:
            a = 10 * randint(1, 8) + randint(1, 9)
            b = randint(10 - a%10, 9)

            if comm_unique(a, b, a + b, variants):
                variants.append(choice(([a, b, a + b], [b, a, a + b])))

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        B = np.arange(1, 10)
        A = np.array([10 * randint(2, 9) + randint(0, b) for b in B])
        variants = list(zip(A, B, A - B))
        shuffle(variants)

        # final variant
        while True:
            b = randint(1, 9)
            a = 10 * randint(2, 9) + randint(0, b)
            variant = [a, b, a - b]

            if variant not in variants:
                variants.append(variant)
                break

        variants = remove_indices('ABC', variants)

    elif operation == '*':
        ''' NOTE:
        0*0 possible in this version
        '''
        # There is a zero in A or this would be 3
        zerosLeft = 2
        A = np.arange(10)

        for a in A:
            while True:
                b = randint(0 if zerosLeft else 1, 10)
                if comm_unique(a, b, None, variants):
                    variants.append([a, b, None])
                    if b == 0:  zerosLeft -= 1
                    break

        shuffle(variants)

    elif operation in (':', '/'):
        B = np.arange(1, 11)
        A = B * [randint(1, 10) for i in range(len(B))]
        variants = list(zip(A, B, [None] * 10))
        shuffle(variants)

    return variants

def lvl6(operation):
    variants = []

    if operation == '+':
        # this time zeros are found in one-units of a 2 digit number twice
        zerosLeft = 2

        while len(variants) != 10:
            a = 10 * randint(1, 8) + randint(1, 9)
            b = 10 * randint(1, 9 - a//10)
            if not zerosLeft:   b += randint(1, 10 - a%10)

            if comm_unique(a, b, a + b, variants):
                variants.append(choice(([a, b, a + b], [b, a, a + b])))
                if not b%10: zerosLeft -= 1

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        ''' awkward '''
        while len(variants) != 10:
            a = 10 * randint(2, 9) + randint(1, 9)
            # at least one subtrahend has a zero unit
            if len(variants) < 9:
                b = 10 * randint(1, a//10 - 1) + randint(1, a%10)
            else:
                b = 10 * randint(1, a//10 - 1)

            variant = [a, b, a - b]
            if variant not in variants:
                variants.append(variant)

        # shuffle in the zero one digit variant
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        underTenOK = 2
        A = np.arange(10)

        for a in A:
            while True:
                if a == 0:
                    b = randint(1, 10)
                elif underTenOK:
                    b = randint(0, 10)
                else:
                    b = randint(int(np.ceil(10 / a)), 10)

                if comm_unique(a, b, a * b, variants):
                    variants.append([a, b, a * b])
                    if a * b < 10:    underTenOK -= 1
                    break

        shuffle(variants)
        variants = remove_indices('AB', variants)

    elif operation in (':', '/'):
        B = np.arange(1, 11)
        A = B * [randint(1, 10) for i in range(len(B))]
        variants = list(zip(A, B, A//B))
        shuffle(variants)
        variants = remove_indices('AB', variants)

    return variants

def lvl7(operation):
    variants = []

    if operation == '+':
        while len(variants) != 10:
            a = 10 * randint(1, 7) + randint(1, 9)
            b = 10 * randint(1, 8 - a//10) + randint(10 - a%10, 9)

            if comm_unique(a, b, a + b, variants):
                variants.append([a, b, a + b])

        variants=remove_indices('ABC', variants)

    elif operation == '-':
        B = np.append(np.arange(1, 10), randint(1, 9)) + [10 * randint(1, 8) for i in range(10)]
        A = [10 * randint(b//10 + 1, 9) + randint(1, b%10) for b in B]
        variants = list(zip(A, B, A - B))
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        ''' NOTE:
        currently no restrictions on numbers of 100 mults, 10 mults, ...

        ALSO
        problem with unique variants
        '''
        # for last entry, a in hundreds or ones could cause uniqueness issues
        A = [choice((1, 10, 100)) * a for a in range(1, 10)]
        while True:
            a = choice((1, 10, 100)) * randint(1, 9)
            if a not in A:
                A.append(a)
                break

        for a in A:
            while True:
                if a < 10:
                    b = 100 * randint(1, min(10//a, 9))
                elif a < 100:
                    b = choice((1, 10)) * randint(1, 9)
                else:
                    b = randint(1, 10//(a//100))

                # this is causing issues
                # if comm_unique(a,b,None, variants) and 100 <= a*b <= 1000:
                if [a, b, None] not in variants and 100 <= a * b <= 1000:
                    variants.append([a, b, None])
                    break

        shuffle(variants)

    elif operation in (':', '/'):
        B = [choice((1, 10)) * b for b in range(1, 10)]
        while True:
            b = choice((1, 10)) * randint(1, 9)
            if b not in B:
                B.append(b)
                break

        for b in B:
            while True:
                if b < 10:
                    a = b * choice((1, 10, 100)) * randint(1, 9)
                elif b < 100:
                    a = b * choice((1, 10))*randint(1, 9)
                else:
                    a = b * randint(1, 9)

                if [a, b, None] not in variants and a <= 1000:
                    variants.append([a, b, None])
                    break

        shuffle(variants)

    return variants

def lvl8(operation):
    variants = []

    if operation == '+':
        while len(variants) != 10:
            a = 100 * randint(1, 10)
            b = choice((10, 100)) * randint(1, 9)
            if b < 100:
                b += randint(1, 9)

            if all((100 < a + b <= 1000, b < a, comm_unique(a, b, None, variants))):
                    variants.append(choice(([a, b, None], [b, a, None])))

    elif operation == '-':
        while len(variants) != 10:
            a = 100 * randint(2, 10)
            b = choice((10 * randint(1, 9), 100 * randint(1, a / 100 - 1)))

            variant = [a, b, a - b]
            if variant not in variants:
                variants.append(variant)

        variants = remove_indices('ABC', variants)

    elif operation == '*':
        A = [choice((1, 10, 100)) * i for i in np.arange(10)]
        for a in A:
            while True:
                if a == 0:
                    b = choice((1, 10, 100)) * randint(1, 9)
                elif a < 10:
                    b = 100 * randint(1, min(10//a, 9))
                elif a < 100:
                    b = choice((1, 10)) * randint(1, 9)
                else:
                    b = randint(1, 10//(a//100))

                # this is causing issues
                # if comm_unique(a,b,None, variants) and 100 <= a*b <= 1000:
                if [a, b, a * b] not in variants and (100 <= a * b <= 1000 or a == 0):
                    variants.append([a, b, a * b])
                    break

        shuffle(variants)
        variants = remove_indices('AB', variants)

    elif operation in (':', '/'):
        B = [choice((1, 10)) * b for b in range(1, 10)]
        while True:
            b = choice((1, 10)) * randint(1, 9)
            if b not in B:
                B.append(b)
                break

        for b in B:
            while True:
                if b < 10:
                    a = b * choice((1, 10, 100)) * randint(1, 9)
                elif b < 100:
                    a = b * choice((1, 10)) * randint(1, 9)
                else:
                    a = b * randint(1, 9)

                if [a, b, a//b] not in variants and a <= 1000:
                    variants.append([a, b, a//b])
                    break

        shuffle(variants)
        variants = remove_indices('AB', variants)

    return variants

def lvl9(operation):
    variants = []

    if operation == '+':
        ''' NOTE
        should b < 100 be possible?
        examples say OK
        PROBABLY NOT
        '''
        bothHunLeft = 2
        while len(variants) != 10:
            # usually X00
            a = 100 * randint(1, 8) + np.random.choice((0, 10), p=(.7, .3)) * randint(1, 9)
            # usually XY0
            b = 100 * randint(1, 9 - a//100) + np.random.choice((0, 10), p=(.3, .7))*randint(1, 9 - min((a%100)//10, 8))

            if not a%100 and not b%100 and not bothHunLeft:
                continue

            if comm_unique(a,b,a + b, variants) and 200 < a + b < 1000:
                variants.append(choice(([a, b, a + b], [b, a, a + b])))
                if not a%100 and not b%100: bothHunLeft -= 1

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        ''' NOTE:
        I've avoided B tens higher than A tens completely
        '''
        while len(variants) != 10:
            a = 100 * randint(1, 9) + 10 * randint(1, 8)
            b = 100 * randint(0, a//100 - 1) + 10 * randint((a%100)//10 + 1, 9)
            variant = [a, b, a - b]

            if variant not in variants:
                variants.append(variant)

        variants = remove_indices('ABC', variants)

    elif operation == '*':
        variants = mult_variants_from_list([11, 12, 15, 25], minimum=2, low=2)
        variants = remove_indices('ABC', variants)

    elif operation in (':', '/'):
        B = repeatList([11, 12, 15, 25], 2)

        for b in B:
            while True:
                c = randint(1, 10)
                variant = [b * c, b, c]

                if variant not in variants:
                    variants.append(variant)
                    break

        variants = remove_indices('AC', variants)

    return variants

def lvl10(operation):
    variants = []

    if operation == '+':
        while len(variants) != 10:
            a = choice((100, 1000)) * randint(10, 99)
            b = choice((10, 100, 1000)) * randint(10, 99)

            if (a//1000 + b//1000 < 10) and ((a%1000)//100 + (b%1000)//100 < 10) and ((a%100)//10 + (b%100)//10 < 10):
                continue

            if comm_unique(a, b, a + b, variants) and 1000 < a + b < 99000:
                variants.append(choice(([a, b, a + b], [b, a, a + b])))

        variants = remove_indices('ABC', variants)

    elif operation == '-':
        while len(variants) != 10:
            a = choice((100, 1000)) * randint(10, 99)
            b = choice((10, 100, 1000) if a//1000 else (10, 100)) * randint(1, 99)

            if not ((b%1000)//100 > (a%1000)//100) or not ((b%100)//10 > (a%100)//10):
                continue

            if [a, b, None] not in variants and 1000 < a - b:
                variants.append([a, b, None])

    elif operation == '*':
        ''' NOTE:
        quotient is less than 1000
        '''
        A = repeatList([10, 100, 1000], 2)
        for i in range(len(A)):
            A[i] *= randint(2, 9)

        for a in A:
            while True:
                b = 10 * randint(2, 9)
                if comm_unique(a, b, a * b, variants) and a * b < 1000000:
                    variants.append(choice(([a, b, a * b], [b, a, a * b])))
                    break

        variants = remove_indices('ABC', variants)

    elif operation in (':', '/'):
        ''' NOTE:
        I added restrictions to match examples
        '''
        B = repeatList([1, 10, 100, 1000], 2)
        for i in range(len(B)):
            B[i] *= randint(2, 9)

        for b in B:
            while True:
                a = b * choice((1, 10, 100)) * randint(2, 9)
                if [a, b, a//b] not in variants and a//b <= 10000 and 100 < a < 1000000:
                    variants.append([a, b, a//b])
                    break

        variants = remove_indices('ABC', variants)

    return variants

def level_maker(level, operation):
    '''operation should be a string'''
    functions = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9, lvl10]
    return functions[level-1](operation)

test = level_maker(8, '*')
# print(test)
# are there 10 variants?
# print(len(test))
# are there repeated values?
# print(any(test.count(x) > 1 for x in test))

def make_output(versions=10):
    f = open('output.txt', 'w')
    # completed =
    for level in range(1, 11):
        for operation in ['+', '-', '*', ':']:
            f.write(str(level) + ' ' + str(operation) + '\n')
            contents = []
            # generate 10 versions for a level
            for version in range(versions):
                # the 10 versions should be unique
                ''' how unique? '''
                while True:
                    level_string = str(level_maker(level, operation))
                    if level_string not in contents:
                        contents.append(level_string)
                        f.write(level_string + '\n')
                        break
    f.close()

make_output()
