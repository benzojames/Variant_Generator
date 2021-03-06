"""
Sometimes I ensure that variants are within specifications while making them.
In 8+, however, I let variants be whatever, but only add them if they are
within specifications. This is much easier to code, and can take on a simpler
format, but will likely run more slowly as we will have to generate more
variants before they randomly fit the specifications.
"""

from random import randint, choice, shuffle
import numpy as np

VARS_PER_LVL = 10

def remove_indices(options, variant_list):
    """Replace some indices in a list with None

    If the variants in a level can have different missing variables, then we
    want to have at most three questions with the same missing variable in a
    row.
    """
    max_repeats = 3
    variants = []
    if options == 'AB':
        missing = [0, 1]
    elif options == 'ABC':
        missing = [0, 1, 2]
    elif options == 'AC':
        missing = [0, 2]
    else:
        # perhaps the option was invalid
        return None
    # don't have 4 in a row all missing A or all missing B
    # 30% liklihood of having 3 in a row
    missing *= max_repeats
    shuffle(missing)
    # once maximums have been satisfied, repeat
    missing += missing[:VARS_PER_LVL - len(missing)]

    for i, item in enumerate(variant_list):
        # variant_list may be filled with zipped objects
        variant = list(item)

        # may ruin pattern, but only out of necessity
        if variant.count(0) > 1:
            variant[variant.index(0)] = None
        else:
            variant[missing[i]] = None
        variants.append(variant)
    return variants

def repeat_list(input_list, minimum):
    '''
    We need to see all values in B exactly minimum times before we can repeat
    them any further. Once this condition has been satisfied repeat the list
    until it has VARS_PER_LVL values.
    This value takes the values in B and returns a shuffled list of length VARS_PER_LVL
    that satisfies the above repetition condition.
    '''
    lst = input_list * minimum
    shuffle(lst)
    lst += lst[:VARS_PER_LVL - len(lst)]
    return lst

def comm_unique(left, right, result, variants):
    '''
    If the operation is commutative don't consider commuted versions to be unique.

    returns [L, R, res] or [R, L, res]
    '''
    if all(([left, right, result] not in variants, [right, left, result] not in variants)):
        return choice(([left, right, result], [right, left, result]))
    else:
        return False

def comm_choice(left, right, result):
    '''Returns L R res or R L res'''
    return choice(([left, right, result], [right, left, result]))

def mult_variants_from_list(input_list, minimum, low=1, high=10, zeros=0, keep_product=True):
    '''
    input_list is a list of numbers, we want to see each number in input_list exactly minimum times
    before we see any numbers in input_list more than minimum times
    '''
    variants = []
    while len(variants) != VARS_PER_LVL:
        ''' NOTE:
        reset see once all values are used
        when reset occurs, this could lead to at most 4 questions
        in a row that share a multiplicant

        We want to see all values in inputs minimum times before we see any of them
        more than minimum times.
        '''
        to_see = input_list * minimum
        while to_see and len(variants) != VARS_PER_LVL:
            factor_right = choice(to_see)
            to_see.remove(factor_right)

            while True:
                if factor_right == 0:
                    factor_left = randint(max(low, 1), high)
                else:
                    factor_left = randint(0 if zeros > 0 else max(low, 1), high)
                product = factor_left * factor_right
                if not (factor_left in input_list and factor_left not in to_see):
                    if comm_unique(factor_left, factor_right, product, variants):
                        break

            if factor_left == 0:
                zeros -= 1
            if factor_left in to_see:
                to_see.remove(factor_left)
            # is the product/sum set to None?
            variants.append([factor_left, factor_right, product if keep_product else None])

    return variants

def ab_count(num, variants):
    '''Check how many times we have used a left or right addend/factor... already'''
    result = 0
    for variant in variants:
        result += variant[:2].count(num)
    return result

def repeat_shuffle_fill(lst, num):
    output = lst * num
    shuffle(output)
    mult = VARS_PER_LVL//len(output) + 1
    output *= mult
    return output[:VARS_PER_LVL]

def lvl1(operation):
    variants = []

    if operation == '+':
        # range functions helps ensure our variants will be diverse
        addend_left_list = range(VARS_PER_LVL)
        addend_right_list = [10 - i for i in addend_left_list]
        variants = list(zip(addend_left_list, addend_right_list, [10] * VARS_PER_LVL))
        shuffle(variants)

        # by default either A or B is missing
        variants = remove_indices('AB', variants)

    elif operation == '-':
        ''' NOTE:
        0 - 0 is currently possible
        '''
        # subtrahend_list = list(range(VARS_PER_LVL))
        # minuend_list = [randint(subtrahend, 10) for subtrahend in subtrahend_list]
        # difference_list = [i - j for i, j in zip(minuend_list, subtrahend_list)]

        # variants = list(zip(minuend_list, subtrahend_list, difference_list))
        # shuffle(variants)
        # variants = remove_indices('ABC', variants)
        CZeros = 2
        for subtrahend in range(VARS_PER_LVL):
            # possible this will cause a repetition
            minuend = randint(subtrahend + (0 if CZeros else 1), 10)
            difference = minuend - subtrahend
            if difference == 0:
                CZeros -= 1
            variants.append([minuend, subtrahend, difference])
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        #variants = mult_variants_from_list([1, 2, 5, 10], minimum=2, keep_product=False)
        # factor_right_list = repeat_shuffle_fill([1,2,5,10], 2)
        # variants.append([0, factor_right_list.pop(), None])
        # while len(variants) != 10:
        #     factor_right = factor_right_list.pop()

        #     # every factor in factor_right_list must be used
        #     while True:
        #         factor_left = randint(1, 9)
        #         variant = [factor_left, factor_right, None]
        #         if variant not in variants:
        #             variants.append(variant)
        #             break
        factor_right_list = repeat_shuffle_fill([1,2,5,10], 2)
        factor_left_list = list(range(11))
        shuffle(factor_left_list)
        if factor_left_list[-1] != 0:
            factor_left_list.pop()
        else:
            factor_left_list.pop(0)
        variants = list(zip(factor_left_list, factor_right_list, 10*[None]))

    elif operation in (':', '/'):
        # zeros = 2
        # divisor_list = repeat_list([1, 2, 5, 10], 2)

        # for divisor in divisor_list:
        #     while True:
        #         dividend = divisor * randint(0 if zeros > 0 else 1, 10)
        #         variant = [dividend, divisor, None]

        #         if variant not in variants:
        #             variants.append(variant)
        #             if dividend == 0:
        #                 zeros -= 1
        #             break
        temp = [1,2,5,10]
        divisor_list = repeat_shuffle_fill(temp, 2)
        temp.remove(1)
        if divisor_list[-2] == 1:
            divisor_list[-2] = choice(temp)
        if divisor_list[-1] == 1:
            divisor_list[-1] = choice(temp)

        mult_list = list(range(11))
        shuffle(mult_list)
        mult_list.pop()
        dividend_list = [i*j for i, j in zip(mult_list, divisor_list)]

        variants = list(zip(dividend_list, divisor_list, 10*[None]))

    return variants

def lvl2(operation):
    variants = []

    if operation == '+':
        '''
        A in [0, 20]
        B in [0, 20]
        A + B in [11, 20]
        '''
        zeros = 2
        floor = 0
        ceil = 20

        while len(variants) != VARS_PER_LVL:
            ''' NOTE:
            this does not allow for same A, B, C even if different missing index
            '''
            addend_left = randint(floor, ceil)
            addend_right = randint(max(11 - addend_left, floor), 20 - addend_left)

            if comm_unique(addend_left, addend_right, addend_left + addend_right, variants):
                variants.append([addend_left, addend_right, addend_left + addend_right])
                if 0 in (addend_left, addend_right):
                    zeros -= 1
                    if zeros == 0:
                        floor = 1
                        ceil = 19

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        """ NOTE:
        currenly can have B=2 or B=12 not both
        """
        # subtrahend_list = [i + choice((0, 10)) for i in range(VARS_PER_LVL)]
        # minuend_list = [randint(max(subtrahend, 11), 20) for subtrahend in subtrahend_list]
        # difference_list = [i - j for i, j in zip(minuend_list, subtrahend_list)]

        # variants = list(zip(minuend_list, subtrahend_list, difference_list))
        over_one = list(range(2, 10))
        shuffle(over_one)
        subtrahend_list = [0, 1] + over_one
        # min 4 crossovers
        while len(variants) < 4:
            subtrahend = subtrahend_list.pop()
            minuend = randint(11, 9 + subtrahend)
            difference = minuend - subtrahend
            variants.append([minuend, subtrahend, difference])

        CZeros = 1
        for temp_sub in subtrahend_list:
            subtrahend = temp_sub + choice((0, 10))
            # might cause repition
            minuend = randint(max(subtrahend + (0 if CZeros else 1), 11), 20)
            difference = minuend - subtrahend
            if difference == 0:
                CZeros -= 1
            variants.append([minuend, subtrahend, difference])
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        variants = mult_variants_from_list([0, 4, 8], minimum=3, zeros=1, keep_product=False)

    elif operation in (':', '/'):
        #divisor_list = repeat_list([4, 8], 3)
        divisor_list = repeat_shuffle_fill([4, 8], 3)

        for divisor in divisor_list:
            while True:
                variant = [divisor * randint(1, 10), divisor, None]
                if variant not in variants:
                    variants.append(variant)
                    break
        # want dividend = 0 once
        variants[randint(0, 9)][0] = 0

    return variants

def lvl3(operation):
    variants = []

    if operation == '+':
        zeros = 2
        floor = 0

        while len(variants) != VARS_PER_LVL:
            addend1 = 10 * randint(2, 9)
            addend2 = choice((randint(floor, 9), 10 * randint(1, 10 - addend1 / 10)))
            summation = addend1 + addend2

            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
                if addend2 == 0:
                    zeros -= 1
                    if zeros == 0:
                        floor = 1

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        # subtrahend <= 80 (need difference >= 20)
        subtrahend_list = [i * choice((1, 10)) for i in range(1, 8)] + [8, 9]
        subtrahend_list += [choice((randint(1, 7) * choice((1, 10)), 8, 9))]

        for subtrahend in subtrahend_list:
            while True:
                minuend = 10 * randint(max(3, subtrahend / 10), 10)
                if [minuend, subtrahend, minuend - subtrahend] not in variants:
                    variants.append([minuend, subtrahend, minuend - subtrahend])
                    break

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        #variants = mult_variants_from_list([3, 6, 9], minimum=3, zeros=2, keep_product=False)
        # examples imply having 6 * 9 and 9 * 6 is ok
        factor_right_list = [3, 6, 9] * 3
        shuffle(factor_right_list)
        factor_right_list += [factor_right_list[0]]

        factor_left_list = list(range(10))
        shuffle(factor_left_list)

        variants = list(zip(factor_left_list, factor_right_list, VARS_PER_LVL * [None]))

    elif operation in (':', '/'):
        divisor_list = repeat_list([3, 6, 9], 3)

        for divisor in divisor_list:
            while True:
                variant = [divisor * randint(1, 10), divisor, None]
                if variant not in variants:
                    variants.append(variant)
                    break
        # want dividend = 0 once
        variants[randint(0, 9)][0] = 0

    return variants

def lvl4(operation):
    variants = []

    if operation == '+':
        ''' NOTE:
        Charles said to trust examples over ALGO, but ALGO is quite specific
        about no b = 0 and b = 0 in one example.

        I said no b = 0 since the MIN for this is 0 anyway

        Specs:
        See any addend at most twice
        results are multiples of 10
        '''
        # see small addend at most twice
        addend1_list = list(range(1, 10))*2
        shuffle(addend1_list)

        while len(variants) != VARS_PER_LVL:
            addend1 = addend1_list.pop()

            while True:
                addend2 = 10 * randint(1, 8) + (10 - addend1)
                # unnecessary. `if comm_unique` will already cover this but Im gonna keep anyway
                if ab_count(addend2, variants) == 2:
                    continue
                else:
                    summation = addend1 + addend2

                    possibly_commuted = comm_unique(addend1, addend2, summation, variants)
                    if possibly_commuted:
                        variants.append(possibly_commuted)
                        break

        variants = remove_indices('ABC', variants)

        # zeros = 2

        # while len(variants) != VARS_PER_LVL:
        #     addend1 = 10 * randint(2, 9) + randint(1, 8)
        #     # b = randint(0 if zeros else 1, 9 - a%10)
        #     addend2 = randint(1, 9 - addend1%10)
        #     summation = addend1 + addend2

        #     possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        #     if possibly_commuted:
        #         variants.append(possibly_commuted)
        #         # if b is 0:  zeros -= 1

        # variants = remove_indices('ABC', variants)

    elif operation == '-':
        ''' NOTE:
        I have currently allowed for b = 0 once
        '''
        # subtrahend_list = list(range(VARS_PER_LVL))
        # minuend_list = [10 * randint(2, 9) + randint(sub, 9) for sub in subtrahend_list]
        # difference_list = [i - j for i, j in zip(minuend_list, subtrahend_list)]

        # variants = list(zip(minuend_list, subtrahend_list, difference_list))
        # shuffle(variants)
        # variants = remove_indices('ABC', variants)

        same_digit = 2
        # reversed means we will see 9 first which aviods crossover issues
        for subtrahend in reversed(range(VARS_PER_LVL)):
            minu_digit = randint(subtrahend + (0 if same_digit else 1), 9)
            if minu_digit == subtrahend:
                same_digit -= 1
            minuend = 10 * randint(2, 9) + minu_digit
            difference = minuend - subtrahend
            variants.append([minuend, subtrahend, difference])
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        variants = list(zip(range(VARS_PER_LVL), [7] * VARS_PER_LVL, [None] * VARS_PER_LVL))
        shuffle(variants)

    elif operation in (':', '/'):
        divisor = 7
        dividend_list = [divisor * i for i in range(VARS_PER_LVL)]
        variants = list(zip(dividend_list, [divisor] * VARS_PER_LVL, [None] * VARS_PER_LVL))
        shuffle(variants)

    return variants

def lvl5(operation):
    variants = []

    if operation == '+':
        while len(variants) != VARS_PER_LVL:
            addend1 = randint(2, 9)
            addend2 = 10 * randint(1, 8) + randint(11 - addend1, 9)
            summation = addend1 + addend2
            
            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
        
        variants = remove_indices('ABC', variants)



        # while len(variants) != VARS_PER_LVL:
        #     addend1 = 10 * randint(1, 8) + randint(1, 9)
        #     addend2 = randint(10 - addend1%10, 9)
        #     summation = addend1 + addend2

        #     possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        #     if possibly_commuted:
        #         variants.append(possibly_commuted)

        # shuffle(variants)
        # variants = remove_indices('ABC', variants)

    elif operation == '-':
        subtrahend_list = list(range(2, VARS_PER_LVL))
        minuend_list = [10 * randint(2, 9) + randint(1, sub - 1) for sub in subtrahend_list]
        difference_list = [i - j for i, j in zip(minuend_list, subtrahend_list)]

        variants = list(zip(minuend_list, subtrahend_list, difference_list))
        shuffle(variants)

        # final 2 variants
        while len(variants) != 10:
            subtrahend = randint(2, 9)
            minuend = 10 * randint(2, 9) + randint(1, subtrahend - 1)
            variant = [minuend, subtrahend, minuend - subtrahend]

            if variant not in variants:
                variants.append(variant)

        variants = remove_indices('ABC', variants)

    elif operation == '*':
        # ''' NOTE:
        # 0*0 possible in this version
        # '''
        # # There is a zero in A or this would be 3
        # zeros = 2
        # floor = 0
        # factor_left_list = list(range(VARS_PER_LVL))

        # for factor_left in factor_left_list:
        #     while True:
        #         factor_right = randint(floor, 10)
        #         if comm_unique(factor_left, factor_right, None, variants):
        #             variants.append([factor_left, factor_right, None])
        #             if factor_right == 0:
        #                 zeros -= 1
        #                 if zeros == 0:
        #                     floor = 1
        #             break

        # shuffle(variants)

        # restart if 0 * 0 shows up
        while True:
            # seems to want to avoid three of same factor on a side
            factor_right_list = list(range(11))
            shuffle(factor_right_list)
            factor_right_list = factor_right_list[:10]
            factor_left_list = list(range(10)) + list(range(1, 10))
            shuffle(factor_left_list)
            factor_left_list = factor_left_list[:10]

            if 0 in factor_right_list:
                zero_index = factor_right_list.index(0)
                if factor_left_list[zero_index] == 0:
                    continue
            else:
                variants = list(zip(factor_left_list, factor_right_list, 10*[None]))
                break



    elif operation in (':', '/'):
        '''NOTE: needs spec fix'''
        divisor_list = list(range(1, VARS_PER_LVL + 1))
        dividend_list = [div * randint(1, 10) for div in divisor_list]
        variants = list(zip(dividend_list, divisor_list, [None] * 10))
        shuffle(variants)

        # needs discussion
        # divisor_list = list(range(1, 11))
        # for divisor in divisor_list:
        #     if divisor == 1:
        #         divident = divisor * randint(12//divisor + 1, 10)
        #         variants.append([divident, divisor, None])
        #     elif divisor == 3:
        #         dividend = 30
        #     else:
        #         dividend = divisor * randint(30//divisor, 10)
        #     variants.append([dividend, divisor, None])

    return variants

def lvl6(operation):
    variants = []

    if operation == '+':
        # this time zeros are found in one-units of a 2 digit number twice
        zeros = 2

        while len(variants) != VARS_PER_LVL:
            addend1 = 10 * randint(1, 8) + randint(1, 9)
            addend2 = 10 * randint(1, 9 - addend1//10)
            summation = addend1 + addend2
            if not zeros:
                addend2 += randint(1, 10 - addend1%10)

            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
                if not addend2%10:
                    zeros -= 1

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        # awkward
        same_digit = 2
        while len(variants) != VARS_PER_LVL:
            minu_digit = randint(1, 9)
            minuend = 10 * randint(2, 9) + minu_digit
            # at least one subtrahend has a zero unit
            if len(variants) < VARS_PER_LVL - 1:
                sub_digit = randint(1, minu_digit)
                if minu_digit == sub_digit:
                    if same_digit:
                        same_digit -= 1
                    else:
                        continue
                subtrahend = 10 * randint(1, minuend//10 - 1) + sub_digit
            else:
                subtrahend = 10 * randint(1, minuend//10 - 1)

            variant = [minuend, subtrahend, minuend - subtrahend]
            if variant not in variants:
                variants.append(variant)

        # shuffle in the zero one digit variant
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        # under_ten_ok = 2
        # for factor_left in range(VARS_PER_LVL):
        #     while True:
        #         if factor_left == 0:
        #             factor_right = randint(1, 10)
        #         elif under_ten_ok:
        #             factor_right = randint(0, 10)
        #         else:
        #             factor_right = randint(int(np.ceil(10 / factor_left)), 10)

        #         if comm_unique(factor_left, factor_right, factor_left * factor_right, variants):
        #             variants.append([factor_left, factor_right, factor_left * factor_right])
        #             if factor_left * factor_right < 10:
        #                 under_ten_ok -= 1
        #             break
        while True:
            # seems to want to avoid three of same factor on a side
            factor_right_list = list(range(11))
            shuffle(factor_right_list)
            factor_right_list = factor_right_list[:10]
            factor_left_list = list(range(10)) + list(range(1, 10))
            shuffle(factor_left_list)
            factor_left_list = factor_left_list[:10]

            if 0 in factor_right_list:
                zero_index = factor_right_list.index(0)
                if factor_left_list[zero_index] == 0:
                    continue
            else:
                product_list = (i * j for i, j in zip(factor_left_list, factor_right_list))
                variants = list(zip(factor_left_list, factor_right_list, product_list))
                variants = remove_indices('AB', variants)
                break

        shuffle(variants)
        variants = remove_indices('AB', variants)

    elif operation in (':', '/'):
        '''NOTE: needs spec fix'''
        divisor_list = list(range(1, VARS_PER_LVL + 1))
        dividend_list = [divisor * randint(1, 10) for divisor in divisor_list]
        quotient_list = [i//j for i, j in zip(dividend_list, divisor_list)]

        variants = list(zip(dividend_list, divisor_list, quotient_list))
        shuffle(variants)
        variants = remove_indices('AB', variants)

    return variants

def lvl7(operation):
    variants = []

    if operation == '+':
        while len(variants) != VARS_PER_LVL:
            addend_left = 10 * randint(1, 7) + randint(1, 9)
            addend_right = 10 * randint(1, 8 - addend_left//10) + randint(10 - addend_left%10, 9)

            if comm_unique(addend_left, addend_right, addend_left + addend_right, variants):
                variants.append([addend_left, addend_right, addend_left + addend_right])

        variants = remove_indices('ABC', variants)

    elif operation == '-':
        # temp = list(range(1, VARS_PER_LVL)) + [randint(1, 9)]
        # subtrahend_list = [10 * randint(1, 8) + i for i in temp]
        # minuend_list = [10 * randint(sub//10 + 1, 9) + randint(1, sub%10) for sub in subtrahend_list]
        # difference_list = [i - j for i, j in zip(minuend_list, subtrahend_list)]
        # variants = list(zip(minuend_list, subtrahend_list, difference_list))

        # algorithm forces appearance of X0 - Y0 ...
        # also makes X1 - Y1 50% likely (in my implementation)
        # have a lot of AB - XY where B is small, i could force larger tho when Y is big
        same_digit = 2
        for sub_digit in range(10):
            subtrahend = 10 * randint(1, 8) + sub_digit
            minu_digit = randint(0, sub_digit - (0 if same_digit else 1))
            if minu_digit == sub_digit:
                same_digit -= 1
            minuend = 10 * randint(subtrahend//10 + 1, 9) + minu_digit
            variants.append([minuend, subtrahend, minuend - subtrahend])

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        ''' NOTE:
        currently no restrictions on numbers of 100 mults, 10 mults, ...

        ALSO
        problem with unique variants
        '''
        # for last entry, a in hundreds or ones could cause uniqueness issues
        factor_left_mults = [1] * 3 + [10] * 3 + [100] * 4
        shuffle(factor_left_mults)
        factor_left_mults = factor_left_mults[:8]
        factor_left_list = [0, 1] + [choice(factor_left_mults) * i for i in range(2, VARS_PER_LVL)]
        # while True:
        #     factor_left = choice((1, 10, 100)) * randint(1, 9)
        #     if factor_left not in factor_left_list:
        #         factor_left_list.append(factor_left)
        #         break

        for factor_left in factor_left_list:
            while True:
                if factor_left == 0:
                    factor_right = choice((1, 10, 100)) * randint(1, 9)
                elif factor_left < 10:
                    factor_right = 100 * randint(1, min(10//factor_left, 9))
                elif factor_left < 100:
                    factor_right = choice((1, 10)) * randint(1, 9)
                else:
                    factor_right = randint(1, 10//(factor_left//100))
                product = factor_left * factor_right

                # this is causing issues
                # if comm_unique(a,b,None, variants) and 100 <= a*b <= 1000:
                if [factor_left, factor_right, None] not in variants and (100 <= product <= 10000 or product == 0):
                    variants.append([factor_left, factor_right, None])
                    break

        shuffle(variants)
        # factor_left_mults = [1] * 4 + [10] * 3 + [100] * 4
        # shuffle(factor_left_mults)
        # factor_left_mults = factor_left_mults[:10]
        # factor_right_mults = []

        # for flm in factor_left_mults:


    elif operation in (':', '/'):
        '''NOTE: looks completely new :( '''
        divisor_list = [choice((1, 10)) * i for i in range(1, VARS_PER_LVL)]
        while True:
            divisor = choice((1, 10)) * randint(1, 9)
            if divisor not in divisor_list:
                divisor_list.append(divisor)
                break

        same = True
        for divisor in divisor_list:
            while True:
                if divisor < 10:
                    dividend = divisor * choice((1, 10, 100)) * randint(1, 9)
                elif divisor < 100:
                    dividend = divisor * choice((1, 10)) * randint(1, 9)
                else:
                    dividend = divisor * randint(1, 9)
                
                if divisor == dividend:
                    if not same:
                        continue
                    same = False

                if not (divisor > 10 or dividend/divisor > 10):
                    continue

                if [dividend, divisor, None] not in variants and dividend <= 10000:
                    variants.append([dividend, divisor, None])
                    break

        shuffle(variants)

    return variants

def lvl8(operation):
    variants = []

    if operation == '+':
        addend1 = 100 * randint(1, 9)
        addend2 = randint(1, 9)
        variants.append(comm_choice(addend1, addend2, None))

        while True:
            addend1 = 100 * randint(1, 9)
            addend2 = randint(1, 9)
            possibly_commuted = comm_unique(addend1, addend2, None, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
                break

        while len(variants) != VARS_PER_LVL:
            addend1 = 100 * randint(1, 10)
            addend2 = choice((10, 100)) * randint(1, 9)
            if addend2 < 100:
                addend2 += randint(1, 9)
            summation = addend1 + addend2

            possibly_commuted = comm_unique(addend1, addend2, None, variants)
            if all((100 < summation <= 1000, addend2 < addend1, possibly_commuted)):
                variants.append(possibly_commuted)

        shuffle(variants)

    elif operation == '-':
        # 4 where 100|A, 10|B, B < 100
        while len(variants) != 4:
            minuend = 100 * randint(2, 9)
            subtrahend = 10 * randint(1, 9)
            variants.append([minuend, subtrahend, minuend-subtrahend])

        # 4 where 100|(A and B)
        while len(variants) != 8:
            minu_mult = randint(2, 9)
            minuend = 100 * minu_mult
            subtrahend = 100 * randint(1, minu_mult - 1)
            variants.append([minuend, subtrahend, minuend-subtrahend])

        hun_sub = 100 * randint(2, 9)
        variants.append([1000, hun_sub, 1000 - hun_sub])
        ten_sub = 10 * randint(1, 9)
        variants.append([1000, ten_sub, 1000-ten_sub])

        shuffle(variants)
        variants = remove_indices('ABC', variants)

        # while len(variants) != VARS_PER_LVL:
        #     minuend = 100 * randint(2, 10)
        #     subtrahend = choice((10 * randint(1, 9), 100 * randint(1, minuend / 100 - 1)))

        #     variant = [minuend, subtrahend, minuend - subtrahend]
        #     if variant not in variants:
        #         variants.append(variant)

        # variants = remove_indices('ABC', variants)


    elif operation == '*':
        factor_left_list = [choice((1, 10, 100)) * i for i in range(VARS_PER_LVL)]
        for factor_left in factor_left_list:
            while True:
                if factor_left == 0:
                    factor_right = choice((1, 10, 100)) * randint(1, 9)
                elif factor_left < 10:
                    factor_right = 100 * randint(1, min(10//factor_left, 9))
                elif factor_left < 100:
                    factor_right = choice((1, 10)) * randint(1, 9)
                else:
                    factor_right = randint(1, 10//(factor_left//100))
                product = factor_left * factor_right

                # this is causing issues
                # if comm_unique(a,b,None, variants) and 100 <= a*b <= 1000:
                if [factor_left, factor_right, product] not in variants:
                    if 100 <= product <= 1000 or factor_left == 0:
                        variants.append([factor_left, factor_right, product])
                        break

        shuffle(variants)
        variants = remove_indices('AB', variants)

    elif operation in (':', '/'):
        divisor_list = [choice((1, 10)) * i for i in range(1, VARS_PER_LVL)]
        while True:
            divisor = choice((1, 10)) * randint(1, 9)
            if divisor not in divisor_list:
                divisor_list.append(divisor)
                break

        for divisor in divisor_list:
            while True:
                if divisor < 10:
                    dividend = divisor * choice((1, 10, 100)) * randint(1, 9)
                elif divisor < 100:
                    dividend = divisor * choice((1, 10)) * randint(1, 9)
                else:
                    dividend = divisor * randint(1, 9)

                if [dividend, divisor, dividend//divisor] not in variants and dividend <= 1000:
                    variants.append([dividend, divisor, dividend//divisor])
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
        # three multiples of 10 (but not 100) that add to a 100 multiple
        while len(variants) != 3:
            addend1 = 100 * randint(1, 8) + 10 * randint(1, 9)
            addend2 = 100 * randint(1, 9 - addend1//100) + (10 - addend1%10)
            summation = addend1 + addend2
            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted and 200 < summation < 1000:
                variants.append(possibly_commuted)
        # another 3 where A is a hundred multiple and b is a ten multiple (not a hundred multiple)
        while len(variants) != 6:
            addend1 = 100 * randint(1, 8)
            addend2 = 100 * randint(1, 9 - addend1//100) + 10 * randint(1, 9)
            summation = addend1 + addend2

            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted and 200 < summation < 1000:
                variants.append(possibly_commuted)

        # the rest can be a mixture
        while len(variants) != 10:
            addend1 = 100 * randint(1, 8) + 10 * randint(1, 9)
            addend2 = 100 * randint(1, 9 - addend1//100) + 10 * randint(1, 9)
            summation = addend1 + addend2

            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted and 200 < summation < 1000:
                variants.append(possibly_commuted)
        
        shuffle(variants)
        variants = remove_indices('ABC', variants)

        # bothHunLeft = 2
        # while len(variants) != VARS_PER_LVL:
        #     # usually X00
        #     addend1 = 100 * randint(1, 8) + np.random.choice((0, 10), p=(.7, .3)) * randint(1, 9)
        #     # usually XY0
        #     addend2 = 100 * randint(1, 9 - addend1//100) + np.random.choice((0, 10), p=(.3, .7))*randint(1, 9 - min((addend1%100)//10, 8))

        #     if not addend1%100 and not addend2%100 and not bothHunLeft:
        #         continue

        #     summation = addend1 + addend2

        #     possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        #     if possibly_commuted and 200 < summation < 1000:
        #         variants.append(possibly_commuted)
        #         if not addend1%100 and not addend2%100:
        #             bothHunLeft -= 1

        # shuffle(variants)
        # variants = remove_indices('ABC', variants)

    elif operation == '-':
        # ''' NOTE:
        # I've avoided B tens higher than A tens completely
        # '''
        # while len(variants) != VARS_PER_LVL:
        #     minuend = 100 * randint(1, 9) + 10 * randint(1, 8)
        #     subtrahend = 100 * randint(0, minuend//100 - 1) + 10 * randint((minuend%100)//10 + 1, 9)
        #     variant = [minuend, subtrahend, minuend - subtrahend]

        #     if variant not in variants:
        #         variants.append(variant)

        # variants = remove_indices('ABC', variants)

        # Extra condition 1 for now because I liked that best
        while len(variants) < 4:
            m_huns = randint(1, 10)
            m_tens = randint(1, 8)
            s_huns = 0
            s_tens = randint(m_tens + 1, 9)
            minuend = 100 * m_huns + 10 * m_tens
            subtrahend = 10 * s_tens
            variant = [minuend, subtrahend, minuend - subtrahend]
            if variant not in variants:
                variants.append(variant)
        
        while len(variants) < 7:
            m_huns = randint(2, 10)
            m_tens = 0
            s_huns = randint(1, m_huns - 1)
            s_tens = randint(1, 9)
            minuend = 100 * m_huns
            subtrahend = 100 * s_huns + 10 * s_tens
            variant = [minuend, subtrahend, minuend-subtrahend]
            if variant not in variants:
                variants.append(variant)

        while len(variants) < 10:
            m_huns = randint(1, 10)
            m_tens = randint(2, 9)
            s_huns = randint(1, m_huns)
            s_tens = randint(1, m_tens - 1)
            minuend = 100 * m_huns + 10 * m_tens
            subtrahend = 100 * s_huns + 10 * s_tens
            variant = [minuend, subtrahend, minuend-subtrahend]
            if variant not in variants:
                variants.append(variant)
        
        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '*':
        # variants = mult_variants_from_list([11, 12, 15, 25], minimum=2, low=2)
        # variants = remove_indices('ABC', variants)
        temp = [11, 12, 15, 25]
        shuffle(temp)
        factor_right_list = temp * 2 + temp[:2]
        for factor_right in factor_right_list:
            while True:
                factor_left = randint(2, 10)
                variant = [factor_left, factor_right, factor_left*factor_right]
                if variant not in variants:
                    variants.append(variant)
                    break
        variants = remove_indices('ABC', variants)


    elif operation in (':', '/'):
        divisor_list = repeat_shuffle_fill([11, 12, 15, 25], 2) #repeat_list([11, 12, 15, 25], 2)
        same = True
        for divisor in divisor_list:
            while True:
                if same:
                    quotient = randint(1, 10)
                else:
                    quotient = randint(2, 10)
                if quotient == 1:
                    same = False
                variant = [divisor * quotient, divisor, quotient]

                if variant not in variants:
                    variants.append(variant)
                    break

        variants = remove_indices('AC', variants)

    return variants

def lvl10(operation):
    variants = []

    if operation == '+':
        #     while len(variants) != VARS_PER_LVL:
        #         addend1 = choice((100, 1000)) * randint(10, 99)
        #         addend2 = choice((10, 100, 1000)) * randint(10, 99)

        #         if (addend1//1000 + addend2//1000 < 10) and ((addend1%1000)//100 + (addend2%1000)//100 < 10) and ((addend1%100)//10 + (addend2%100)//10 < 10):
        #             continue
        #         summation = addend1 + addend2

        #         possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        #         if possibly_commuted and 1000 < summation < 99000:
        #             variants.append(possibly_commuted)

        #     variants = remove_indices('ABC', variants)

        # not currently spacing variants
        no_hundreds = 0
        h_crossovers = 0
        t_crossovers = 0
        both_crossovers = 0
        while no_hundreds != 2:
            hun_mult1 = randint(2, 9)
            ten_mult1 = randint(1, 9)
            hun_mult2 = 0
            ten_mult2 = randint(1, 9)
            addend1 = 100 * hun_mult1 + 10 * ten_mult1
            addend2 = 100 * hun_mult2 + 10 * ten_mult2
            summation = addend1 + addend2
            if summation <= 300:
                continue
            possibly_commuted = comm_unique(addend1, addend2, addend1 + addend2, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
                no_hundreds += 1
                if ten_mult1 + ten_mult2 > 10:
                    t_crossovers += 1
        
        while both_crossovers < 3:
            hun_mult1 = randint(2, 9)
            ten_mult1 = randint(2, 9)
            hun_mult2 = randint(11 - hun_mult1, 9)
            ten_mult2 = randint(11 - ten_mult1, 9)
            addend1 = 100 * hun_mult1 + 10 * ten_mult1
            addend2 = 100 * hun_mult2 + 10 * ten_mult2
            summation = addend1 + addend2
            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
                both_crossovers += 1

        while h_crossovers < 2:
            hun_mult1 = randint(2, 9)
            ten_mult1 = randint(1, 8)
            hun_mult2 = randint(11 - hun_mult1, 9)
            ten_mult2 = randint(1, 9 - ten_mult1)
            addend1 = 100 * hun_mult1 + 10 * ten_mult1
            addend2 = 100 * hun_mult2 + 10 * ten_mult2
            summation = addend1 + addend2
            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted:
                variants.append(possibly_commuted)
                h_crossovers += 1

        while t_crossovers < 2:
            hun_mult1 = randint(1, 8)
            ten_mult1 = randint(2, 9)
            hun_mult2 = randint(1, 9 - hun_mult1)
            ten_mult2 = randint(11 - ten_mult1, 9)
            addend1 = 100 * hun_mult1 + 10 * ten_mult1
            addend2 = 100 * hun_mult2 + 10 * ten_mult2
            summation = addend1 + addend2
            if 300 < summation and summation < 1000:
                possibly_commuted = comm_unique(addend1, addend2, summation, variants)
                if possibly_commuted:
                    variants.append([addend1, addend2, summation])
                    t_crossovers += 1

        while len(variants) != 10:
            if choice((True, False)):
                # 10 crossover
                hun_mult1 = randint(1, 8)
                ten_mult1 = randint(2, 9)
                hun_mult2 = randint(1, 9 - hun_mult1)
                ten_mult2 = randint(11 - ten_mult1, 9)
                addend1 = 100 * hun_mult1 + 10 * ten_mult1
                addend2 = 100 * hun_mult2 + 10 * ten_mult2
                summation = addend1 + addend2
                if 300 < summation and summation < 1000:
                    possibly_commuted = comm_unique(addend1, addend2, summation, variants)
                    if possibly_commuted:
                        variants.append(possibly_commuted)

            else:
                # 100 crossover
                hun_mult1 = randint(2, 9)
                ten_mult1 = randint(1, 8)
                hun_mult2 = randint(11 - hun_mult1, 9)
                ten_mult2 = randint(1, 9 - ten_mult1)
                addend1 = 100 * hun_mult1 + 10 * ten_mult1
                addend2 = 100 * hun_mult2 + 10 * ten_mult2
                summation = addend1 + addend2
                possibly_commuted = comm_unique(addend1, addend2, summation, variants)
                if possibly_commuted:
                    variants.append(possibly_commuted)

        shuffle(variants)
        variants = remove_indices('ABC', variants)

    elif operation == '-':
        # while len(variants) != VARS_PER_LVL:
        #     minuend = choice((100, 1000)) * randint(10, 99)
        #     subtrahend = choice((10, 100, 1000) if minuend//1000 else (10, 100)) * randint(1, 99)

        #     if not ((subtrahend%1000)//100 > (minuend%1000)//100) or not ((subtrahend%100)//10 > (minuend%100)//10):
        #         continue

        #     if [minuend, subtrahend, None] not in variants and minuend - subtrahend > 1000:
        #         variants.append([minuend, subtrahend, None])

        # first variant s_huns > 10
        m_huns = randint(12, 20)
        m_tens = randint(0, 8)
        s_huns = randint(11, min(m_huns - 1, 15))
        s_tens = randint(m_tens + 1, 9)
        minuend = 100 * m_huns + 10 * m_tens
        subtrahend = 100 * s_huns + 10 * s_tens
        variants.append([minuend, subtrahend, minuend-subtrahend])

        while len(variants) != 10:
            m_huns = randint(5, 20)
            m_tens = randint(0 if m_huns >= 11 else 1, 8)
            s_huns = randint(1, min(m_huns - 1, 15))
            s_tens = randint(m_tens + 1, 9)
            minuend = 100 * m_huns + 10 * m_tens
            subtrahend = 100 * s_huns + 10 * s_tens
            variant = [minuend, subtrahend, minuend-subtrahend]
            if variant not in variants:
                variants.append(variant)

        shuffle(variants)
        variants = remove_indices('ABC', variants)


    elif operation == '*':
        ''' NOTE:
        quotient is less than 1000
        '''
        factor1_list = [randint(2, 9) * item for item in repeat_list([10, 100, 1000], 2)]

        for factor1 in factor1_list:
            while True:
                factor2 = 10 * randint(2, 9)
                product = factor1 * factor2

                possibly_commuted = comm_unique(factor1, factor2, product, variants)
                if possibly_commuted and product < 1000000:
                    variants.append(possibly_commuted)
                    break

        variants = remove_indices('ABC', variants)

    elif operation in (':', '/'):
        ''' NOTE:
        I added restrictions to match examples
        '''
        divisor_list = [randint(2, 9) * item for item in repeat_list([1, 10, 100, 1000], 2)]

        for divisor in divisor_list:
            while True:
                dividend = divisor * choice((1, 10, 100)) * randint(2, 9)
                quotient = dividend//divisor

                if [dividend, divisor, quotient] not in variants:
                    if quotient <= 10000 and 100 < dividend < 1000000:
                        variants.append([dividend, divisor, dividend//divisor])
                        break

        variants = remove_indices('ABC', variants)

        tps = [1, 10, 100, 1000]
        mult10_divisor_list = [1] * 2 + [10] * 3 + [100] + 3 + [1000] * 2
        mult10_dividend_list = tps[2:] + tps[1:] + tps[:3] + tps[:2]
        #mult_divisor_list = [randint(1, 9)] + list(range(1, 10))

        # want some randomness but cant shuffle mult lists
        mult_index_list = list(range(10))
        shuffle(mult_index_list)

        mult_divisor_list = []
        for mult in mult10_divisor_list:
            

        while mult_index_list:
            index = mult10_index_list.pop()
            mult10_divisor = mult10_divisor_list[index]
            mult10_dividend = mult10_dividend_list[index]
            mult_divisor = mult_divisor_list.pop()
            # need to use all items in mult_index_list
            while True:
                divisor = mult_divisor * mult10_divisor




    return variants

def level_maker(level, operation):
    '''operation should be a string'''
    functions = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9, lvl10]
    return functions[level - 1](operation)

# test = level_maker(8, '*')
# print(test)
# are there 10 variants?
# print(len(test))
# are there repeated values?
# print(any(test.count(x) > 1 for x in test))

def make_output():
    output = open('output.txt', 'w')
    # completed =
    for level in range(1, 11):
        for operation in ['+', '-', '*', ':']:
            output.write(str(level) + ' ' + str(operation) + '\n')
            contents = []
            # generate VARS_PER_LVL variants for a level
            for dummy_variant in range(VARS_PER_LVL):
                # the VARS_PER_LVL variants should be unique
                # how unique?
                while True:
                    lvl = level_maker(level, operation)
                    if str(lvl) not in contents:
                        if len(lvl) != 10:
                            print('Level ' + str(level) + ' ' + operation + ' not full')
                        contents.append(str(lvl))
                        output.write(str(lvl) + '\n')
                        break
    output.close()

make_output()
