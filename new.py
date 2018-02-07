'''uniqueness issues with 2*, 5-, 6+, 6*, 8-'''
# in helpers
#from random import randint, choice, shuffle
import numpy as np
from helpers import *
 
# I dont bother doing anything if only one index is ever removed
def ADD1():
    ''' NOTE: GOOD
        Conditions:
        A + B = 10;
        A = 0 to 9
    '''
    # range functions helps ensure our variants will be diverse
    addend_left_list = range(10)
    addend_right_list = [10 - i for i in addend_left_list]
    variants = list(zip(addend_left_list, addend_right_list, [10] * 10))
    shuffle(variants)
 
    # by default either A or B is missing
    return variants, 'AB'
 
def SUB1():
    ''' NOTE: GOOD '''
    variants = []

    CZeros = 2
    for subtrahend in range(10):
        while True:
            minuend = randint(subtrahend + (0 if CZeros else 1), 10)
 
            # avoid [0, 0, 0]
            if minuend == 0:
                continue
 
            difference = minuend - subtrahend
            if difference == 0:
                CZeros -= 1
            variant = [minuend, subtrahend, difference]
 
            # avoid repitition
            if variant not in variants:
                variants.append([minuend, subtrahend, difference])
                break

    shuffle(variants)
    return variants, 'ABC'
 
def MUL1():
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
    return list(zip(factor_left_list, factor_right_list, [None] * 10)), 'C'
     
def DIV1():
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
 
    quotient_list = list(range(11))
    shuffle(quotient_list)
    quotient_list.pop()
    dividend_list = [i*j for i, j in zip(quotient_list, divisor_list)]
    return list(zip(dividend_list, divisor_list, [None] * 10)), 'C'
 
def ADD2():
    ''' NOTE: GOOD
    A in [0, 20]
    B in [0, 20]
    A + B in [11, 20]
    '''
    variants = []
    zeros = 2
    floor = 0
    ceil = 20
 
    while len(variants) != 10:
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
    return variants, 'ABC'
 
def SUB2():
    """ NOTE: GOOD
    currenly can have B=2 or B=12 not both
    """
    variants = []
    over_one = list(range(2, 10))
    shuffle(over_one)
    # these are unique so variants will be unique
    subtrahend_list = [0, 1] + over_one

    # min 4 crossovers (need subtrahend at least 2)
    while len(variants) < 4:
        subtrahend = subtrahend_list.pop()
        minuend = randint(11, 9 + subtrahend)
        difference = minuend - subtrahend
        variants.append([minuend, subtrahend, difference])
 
    CZeros = 1
    for temp_sub in subtrahend_list:
        subtrahend = temp_sub + choice((0, 10))
        minuend = randint(max(subtrahend + (0 if CZeros else 1), 11), 20)
        difference = minuend - subtrahend
        if difference == 0:
            CZeros -= 1

        variants.append([minuend, subtrahend, difference])

    shuffle(variants)
    return variants, 'ABC'
 
def MUL2():
    # while True:
    #     variants = mult_variants_from_list([0, 4, 8], minimum=3, zeros=1, keep_product=False), 'C'
    #     if check_unique(variants):
    #         return variants
     
    variants = []
    factor_right_list = repeat_shuffle_fill([0, 4, 8], 3)
    while True:
        non_zero_index = randint(0, 9)
        if factor_right_list[non_zero_index] != 0:
            break
    factor_left_list = list(range(1, 10))
    for i in range(10):
        if i == non_zero_index:
            if i != 9:
                factor_left_list.append(factor_left_list[i])
            variants.append([0, factor_right_list[i], None])
        else:
            variants.append([factor_left_list[i], factor_right_list[i], None])
    return variants, 'C'
 
def DIV2():
    variants = []
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
    return variants, 'C'
 
def ADD3():
    ''' GOOD '''
    variants = []
    zeros = 2
    floor = 0
 
    while len(variants) != 10:
        # could be (1, 9)
        addend1 = 10 * randint(2, 9)
        addend2 = choice((randint(floor, 9), 10 * randint(1, 10 - addend1 / 10)))
        summation = addend1 + addend2
 
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 20 < summation < 100:
            variants.append(possibly_commuted)
            if addend2 == 0:
                zeros -= 1
                if zeros == 0:
                    floor = 1
 
    shuffle(variants)
    return variants, 'ABC'
 
def SUB3():
    ''' NOTE: GOOD '''
    variants = []
    # subtrahend <= 80 (need difference >= 20)
    subtrahend_list = [i * choice((1, 10)) for i in range(1, 8)] + [8, 9]
    subtrahend_list += [choice((randint(1, 7) * choice((1, 10)), 8, 9))]
 
    for subtrahend in subtrahend_list:
        while True:
            minuend = 10 * randint(max(3, subtrahend / 10), 10)
            variant = [minuend, subtrahend, minuend - subtrahend]
            if variant not in variants:
                variants.append(variant)
                break
 
    shuffle(variants)
    return variants, 'ABC'
 
def MUL3():
    #variants = mult_variants_from_list([3, 6, 9], minimum=3, zeros=2, keep_product=False)
    # examples imply having 6 * 9 and 9 * 6 is ok
    factor_right_list = [3, 6, 9] * 3
    shuffle(factor_right_list)
    factor_right_list += [factor_right_list[0]]
 
    factor_left_list = list(range(10))
    shuffle(factor_left_list)
    return list(zip(factor_left_list, factor_right_list, [None] * 10)), 'C'
 
def DIV3():
    variants = []
    divisor_list = repeat_list([3, 6, 9], 3)
 
    for divisor in divisor_list:
        while True:
            variant = [divisor * randint(1, 10), divisor, None]
            if variant not in variants:
                variants.append(variant)
                break
    # want dividend = 0 once
    variants[randint(0, 9)][0] = 0
    return variants, 'C'
 
def ADD4():
    ''' NOTE: GOOD
    Charles said to trust examples over ALGO, but ALGO is quite specific
    about no b = 0 and b = 0 in one example.
 
    I said no b = 0 since the MIN for this is 0 anyway
 
    Specs:
    See any addend at most twice
    results are multiples of 10
    '''
    variants = []
    # see smallest addend at most twice
    addend1_list = list(range(1, 10))*2
    shuffle(addend1_list)
 
    while len(variants) != 10:
        addend1 = addend1_list.pop()
 
        while True:
            addend2 = 10 * randint(1, 8) + (10 - addend1)
            # unnecessary. `if comm_unique` will already cover this but Im gonna keep anyway
            if ab_count(addend2, variants) == 2:
                continue
            else:
                summation = addend1 + addend2
 
                possibly_commuted = comm_unique(addend1, addend2, summation, variants)
                if possibly_commuted and summation%10 == 0 and 20 < summation < 100:
                    variants.append(possibly_commuted)
                    break
 
    return variants, 'ABC'
 
    # zeros = 2
 
    # while len(variants) != 10:
    #     addend1 = 10 * randint(2, 9) + randint(1, 8)
    #     # b = randint(0 if zeros else 1, 9 - a%10)
    #     addend2 = randint(1, 9 - addend1%10)
    #     summation = addend1 + addend2
 
    #     possibly_commuted = comm_unique(addend1, addend2, summation, variants)
    #     if possibly_commuted:
    #         variants.append(possibly_commuted)
    #         # if b is 0:  zeros -= 1
 
    # variants = remove_indices('ABC', variants)
 
def SUB4():
    ''' NOTE: GOOD
    I ignored the condition that A >= 21 and used A >= 20 instead
    '''
    variants = []
    same_digit = 2

    # reversed means we will see 9 first which avoids crossover issues
    # range(10) ensures variants will be unique
    for subtrahend in reversed(range(10)):
        minu_digit = randint(subtrahend + (0 if same_digit else 1), 9)
        if minu_digit == subtrahend:
            same_digit -= 1

        minuend = 10 * randint(2, 9) + minu_digit
        difference = minuend - subtrahend
        variants.append([minuend, subtrahend, difference])

    shuffle(variants)
    return variants, 'ABC'
 
def MUL4():
    variants = list(zip(range(10), [7] * 10, [None] * 10))
    shuffle(variants)
    return variants, 'C'
 
def DIV4():
    divisor = 7
    dividend_list = [divisor * i for i in range(10)]
    variants = list(zip(dividend_list, [divisor] * 10, [None] * 10))
    shuffle(variants)
    return variants, 'C'
 
def ADD5():
    ''' NOTE: GOOD '''
    variants = []
    while len(variants) != 10:
        addend1 = randint(2, 9)
        addend2 = 10 * randint(1, 8) + randint(11 - addend1, 9)
        summation = addend1 + addend2
         
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 20 < summation < 100 and summation%10 != 0:
            variants.append(possibly_commuted)
     
    return variants, 'ABC'
    # while len(variants) != 10:
    #     addend1 = 10 * randint(1, 8) + randint(1, 9)
    #     addend2 = randint(10 - addend1%10, 9)
    #     summation = addend1 + addend2
 
    #     possibly_commuted = comm_unique(addend1, addend2, summation, variants)
    #     if possibly_commuted:
    #         variants.append(possibly_commuted)
 
    # shuffle(variants)
    # variants = remove_indices('ABC', variants)
 
def SUB5():
    '''NOTE: GOOD'''
    subtrahend_list = list(range(2, 10))
    minuend_list = [10 * randint(2, 9) + randint(1, sub - 1) for sub in subtrahend_list]
    difference_list = [i - j for i, j in zip(minuend_list, subtrahend_list)]
 
    variants = list(zip(minuend_list, subtrahend_list, difference_list))
    shuffle(variants)
 
    # final 2 variants
    while len(variants) != 10:
        subtrahend = randint(2, 9)
        minuend = 10 * randint(2, 9) + randint(1, subtrahend - 1)
        add_if_unique([minuend, subtrahend, minuend-subtrahend], variants)
 
    return variants, 'ABC'
 
def MUL5():
    # ''' NOTE:
    # 0*0 possible in this version
    # '''
    # # There is a zero in A or this would be 3
    # zeros = 2
    # floor = 0
    # factor_left_list = list(range(10))
 
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
            return list(zip(factor_left_list, factor_right_list, [None] * 10)), 'C'
 
def DIV5():
    '''NOTE: didn't bother with quotient list'''
    divisor_list = list(range(1, 10 + 1))
    dividend_list = [div * randint(1, 10) for div in divisor_list]
    variants = list(zip(dividend_list, divisor_list, [None] * 10))
    shuffle(variants)
    return variants, 'C'
 
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
 
def ADD6():
    ''' NOTE: GOOD '''
    variants = []
    # this time zeros are found in one-units of a 2 digit number twice
    zeros = 2
 
    while len(variants) != 10:
        addend1 = 10 * randint(1, 8) + randint(1, 9)
        addend2 = 10 * randint(1, 9 - addend1//10)
        summation = addend1 + addend2
        if not zeros:
            addend2 += randint(1, 10 - addend1%10)
 
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 20 < summation < 100:
            variants.append(possibly_commuted)
            if not addend2%10:
                zeros -= 1
 
    shuffle(variants)
    return variants, 'ABC'
 
def SUB6():
    '''NOTE: GOOD'''
    # awkward
    variants = []
    same_digit = 2
    while len(variants) != 10:
        minu_digit = randint(1, 9)
        minuend = 10 * randint(2, 9) + minu_digit

        # at least one subtrahend has a zero unit
        if len(variants) < 9:
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
 
    # shuffle in the zero subtrahend digit variant
    shuffle(variants)
    return variants, 'ABC'
 
def MUL6():
    # under_ten_ok = 2
    # for factor_left in range(10):
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
 
            # i was having uniqueness issues
            if check_unique(variants):
                return variants, 'AB'
            else:
                return MUL6()
 
def DIV6():
    '''NOTE: needs spec fix'''
    divisor_list = list(range(1, 10 + 1))
    dividend_list = [divisor * randint(1, 10) for divisor in divisor_list]
    quotient_list = [i//j for i, j in zip(dividend_list, divisor_list)]
 
    variants = list(zip(dividend_list, divisor_list, quotient_list))
    shuffle(variants)
    return variants, 'AB'
 
def ADD7():
    ''' NOTE: GOOD '''
    variants = []
    while len(variants) != 10:
        add_left_ones = randint(2, 9)
        addend_left = 10 * randint(1, 7) + add_left_ones
        addend_right = 10 * randint(1, 8 - addend_left//10) + randint(11 - add_left_ones, 9)
        summation = addend_left + addend_right
 
        variant = [addend_left, addend_right, summation]
        if comm_unique(addend_left, addend_right, summation, variants) and 30 < summation < 200:
            variants.append(variant)
 
    return variants, 'ABC'
 
def SUB7():
    ''' NOTE: GOOD
        always have X0 - Y0
        50% of the time have X1 - Y1
        :/
        have a lot of AB - XY where B is small, i could force larger tho when Y is big
    '''
    variants = []
    same_digit = 2
    # range ensures uniqueness of variants
    for sub_digit in range(10):
        subtrahend = 10 * randint(1, 8) + sub_digit
        minu_digit = randint(0, sub_digit - (0 if same_digit else 1))
        if minu_digit == sub_digit:
            same_digit -= 1

        minuend = 10 * randint(subtrahend//10 + 1, 9) + minu_digit
        variants.append([minuend, subtrahend, minuend - subtrahend])
 
    shuffle(variants)
    return variants, 'ABC'
 
def MUL7():
    ''' NOTE: 
    currently no restrictions on numbers of 100 mults, 10 mults, ...
 
    ALSO
    problem with unique variants
    '''
    variants = []
    # for last entry, a in hundreds or ones could cause uniqueness issues
    factor_left_mults = [1] * 3 + [10] * 3 + [100] * 4
    shuffle(factor_left_mults)
    factor_left_mults = factor_left_mults[:8]
    factor_left_list = [0, 1] + [choice(factor_left_mults) * i for i in range(2, 10)]
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
    return variants, 'C'
    # factor_left_mults = [1] * 4 + [10] * 3 + [100] * 4
    # shuffle(factor_left_mults)
    # factor_left_mults = factor_left_mults[:10]
    # factor_right_mults = []
 
    # for flm in factor_left_mults:
 
def DIV7():
    '''NOTE: didn't bother with quotient list
    looks completely new :( '''
    variants = []
    divisor_list = [choice((1, 10)) * i for i in range(1, 10)]
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
 
    return variants, 'C'
 
def ADD8():
    '''NOTE: GOOD
    algo specifies we can have XY0 + A00 but examples don't have this
    i"m going with examples
    '''
    variants = []
    # will satisfy in (100, 1000)
    variants.append(comm_choice(100 * randint(1, 9), randint(1, 9), None))
 
    while len(variants) < 2:
        hun_multiple = 100 * randint(1, 9)
        under_10 = randint(1, 9)

        possibly_commuted = comm_unique(hun_multiple, under_10, None, variants)
        if possibly_commuted:
            variants.append(possibly_commuted)
 
    while len(variants) != 10:
        addend1 = choice((10, 100)) * randint(1, 9)
        addend2 = choice((10, 100)) * randint(1, 9)
        if addend2 < 100:
            addend2 += randint(0, 9)
        summation = addend1 + addend2
 
        possibly_commuted = comm_unique(addend1, addend2, None, variants)
        if possibly_commuted and 100 < summation < 1000:
            variants.append(possibly_commuted)
 
    shuffle(variants)
    return variants, 'C'
 
def SUB8():
    '''NOTE: GOOD'''
    CND1 = []
    # 4 where 100|A, 10|B, B < 100
    while len(CND1) != 4:
        minuend = 100 * randint(2, 9)
        subtrahend = 10 * randint(1, 9)
        difference = minuend - subtrahend
        if 100 < difference <= 1000:
            add_if_unique([minuend, subtrahend, difference], CND1)

    hun_sub = 100 * randint(2, 9)
    CND1.append([1000, hun_sub, 1000 - hun_sub])
    shuffle(CND1)

    CND2 = []
    # 4 where 100|(A and B)
    while len(CND2) != 8:
        minu_huns = randint(2, 9)
        minuend = 100 * minu_huns
        subtrahend = 100 * randint(1, minu_huns - 1)
        if 100 < difference <= 1000:
            add_if_unique([minuend, subtrahend, difference], CND2)
 
    ten_sub = 10 * randint(1, 9)
    CND2.append([1000, ten_sub, 1000 - ten_sub])
    shuffle(CND2)


    variants = CND1[:3] + CND2[:3]
    shuffle(variants)
    # to satisfy min_before_repeat
    if choice((True, False)):
        variants = [CND1.pop(), CND2.pop()] + variants + [CND1.pop(), CND2.pop()]
    else:
        variants = [CND2.pop(), CND1.pop()] + variants + [CND2.pop(), CND1.pop()]
    return variants, 'ABC'
 
def MUL8():
    variants = []
    factor_left_list = [choice((1, 10, 100)) * i for i in range(10)]
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
    return variants, 'AB'
 
def DIV8():
    variants = []
    divisor_list = [choice((1, 10)) * i for i in range(1, 10)]
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
    return variants, 'AB'
 
def ADD9_variants_check():
    return
def ADD9variant_check(a, b, c):
    # don't add 2 multiples of 100
    if a%100 == 0 and b%100 == 0:
        return False

def ADD9type1():
    # multiples of 10 (but not 100) that add to a 100 multiple
    addend1 = 100 * randint(1, 8) + 10 * randint(1, 9)
    addend2 = 100 * randint(1, 9 - addend1//100) + (10 - addend1%10)
    return addend1, addend2, addend1 + addend2
def ADD9type2():
    # A is a hundred multiple and B is a ten multiple (not a hundred multiple)
    addend1 = 100 * randint(1, 8)
    addend2 = 100 * randint(1, 9 - addend1//100) + 10 * randint(1, 9)
    return addend1, addend2, addend1 + addend2
def ADD9type3():
    # A and B ten mult but not hun mult
    addend1 = 100 * randint(1, 8) + 10 * randint(1, 9)
    addend2 = 100 * randint(1, 9 - addend1//100) + 10 * randint(1, 9)
    summation = addend1 + addend2
    return addend1, addend2, summation
def ADD9():
    ''' NOTE: GOOD
    should b < 100 be possible?
    examples say OK
    PROBABLY NOT
    '''
    variants = []
    # three of condition 1
    while len(variants) < 3:
        addend1, addend2, summation = ADD9type1()
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and summation%100 == 0 and 200 < summation < 1000:
            variants.append(possibly_commuted)

    # three of condition 2
    while len(variants) < 6:
        addend1, addend2, summation = ADD9type2()
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 200 < summation < 1000:
            variants.append(possibly_commuted)

    # three of condition 3
    while len(variants) < 9:
        addend1, addend2, summation = ADD9type3()
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 200 < summation < 1000:
            variants.append(possibly_commuted)
    
    # to satisfy min_before_repeat condition last variant must have same condition as first
    temp = list(enumerate(variants))
    shuffle(temp)
    variants = [enm[1] for enm in temp]
    choices = [ADD9type1, ADD9type2, ADD9type3]
    selection = choices[temp[0][0]//3]
    while len(variants) < 10:
        # addend1 = 100 * randint(1, 8) + 10 * randint(1, 9)
        # addend2 = 100 * randint(1, 9 - addend1//100) + 10 * randint(1, 9)
        # summation = addend1 + addend2
        addend1, addend2, summation = selection()
        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 200 < summation < 1000:
            variants.append(possibly_commuted)
     
    return variants, 'ABC'
 
    # bothHunLeft = 2
    # while len(variants) != 10:
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
 
def SUB9type1():
    m_huns = randint(1, 10)
    m_tens = randint(1, 8)
    s_huns = 0
    s_tens = randint(m_tens + 1, 9)
    minuend = 100 * m_huns + 10 * m_tens
    subtrahend = 10 * s_tens
    return [minuend, subtrahend, minuend - subtrahend]
def SUB9type2():
    m_huns = randint(2, 10)
    m_tens = 0
    s_huns = randint(1, m_huns - 1)
    s_tens = randint(1, 9)
    minuend = 100 * m_huns
    subtrahend = 100 * s_huns + 10 * s_tens
    return [minuend, subtrahend, minuend-subtrahend]
def SUB9type3():
    m_huns = randint(1, 10)
    m_tens = randint(2, 9)
    s_huns = randint(1, m_huns)
    s_tens = randint(1, m_tens - 1)
    minuend = 100 * m_huns + 10 * m_tens
    subtrahend = 100 * s_huns + 10 * s_tens
    return [minuend, subtrahend, minuend-subtrahend]
def SUB9():
    '''NOTE: GOOD'''
    variants = []
    while len(variants) < 3:
        variant = SUB9type1()
        add_if_unique(variant, variants)
     
    while len(variants) < 6:
        variant = SUB9type2()
        add_if_unique(variant, variants)

    while len(variants) < 9:
        variant = SUB9type3()
        add_if_unique(variant, variants)
     
    shuffle(variants)

    # last variant
    while len(variants) != 10:
        var_type = choice((SUB9type1, SUB9type2, SUB9type3))
        add_if_unique(var_type(), variants)

    return variants, 'ABC'
 
def MUL9():
    # variants = mult_variants_from_list([11, 12, 15, 25], minimum=2, low=2)
    # variants = remove_indices('ABC', variants)
    variants = []
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
    return variants, 'ABC'
 
def DIV9():
    variants = []
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
 
    return variants, 'AC'
 
def ADD10():
    ''' NOTE: GOOD
        The way the specs are laid out min_before_repeat would not make sense
    '''
    #     while len(variants) != 10:
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
    variants = []
    once_hundred = 2
    h_crossovers = 2
    t_crossovers = 2
    both_crossovers = 3

    while once_hundred:
        hun_mult1 = randint(2, 9)
        ten_mult1 = randint(2, 9)
        hun_mult2 = 0
        ten_mult2 = randint(11 - ten_mult1, 9)
        addend1 = 100 * hun_mult1 + 10 * ten_mult1
        addend2 = 100 * hun_mult2 + 10 * ten_mult2
        summation = addend1 + addend2

        possibly_commuted = comm_unique(addend1, addend2, addend1 + addend2, variants)
        if possibly_commuted and 300 < summation < 2000:
            variants.append(possibly_commuted)
            once_hundred -= 1
            # dont need to track this
            # if ten_mult1 + ten_mult2 > 10:
            #     t_crossovers -= 1
     
    while both_crossovers:
        hun_mult1 = randint(2, 9)
        ten_mult1 = randint(2, 9)
        hun_mult2 = randint(11 - hun_mult1, 9)
        ten_mult2 = randint(11 - ten_mult1, 9)
        addend1 = 100 * hun_mult1 + 10 * ten_mult1
        addend2 = 100 * hun_mult2 + 10 * ten_mult2
        summation = addend1 + addend2

        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 300 < summation < 2000:
            variants.append(possibly_commuted)
            both_crossovers -= 1
 
    while h_crossovers:
        hun_mult1 = randint(2, 9)
        ten_mult1 = randint(1, 8)
        hun_mult2 = randint(11 - hun_mult1, 9)
        ten_mult2 = randint(1, 9 - ten_mult1)
        addend1 = 100 * hun_mult1 + 10 * ten_mult1
        addend2 = 100 * hun_mult2 + 10 * ten_mult2
        summation = addend1 + addend2

        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 300 < summation < 2000:
            variants.append(possibly_commuted)
            h_crossovers -= 1
 
    while t_crossovers:
        hun_mult1 = randint(1, 8)
        ten_mult1 = randint(2, 9)
        hun_mult2 = randint(1, 9 - hun_mult1)
        ten_mult2 = randint(11 - ten_mult1, 9)
        addend1 = 100 * hun_mult1 + 10 * ten_mult1
        addend2 = 100 * hun_mult2 + 10 * ten_mult2
        summation = addend1 + addend2

        possibly_commuted = comm_unique(addend1, addend2, summation, variants)
        if possibly_commuted and 300 < summation < 1000:
            variants.append([addend1, addend2, summation])
            t_crossovers -= 1
 
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

            possibly_commuted = comm_unique(addend1, addend2, summation, variants)
            if possibly_commuted and 300 < summation < 1000:
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
            if possibly_commuted and 300 < summation < 2000:
                variants.append(possibly_commuted)
 
    shuffle(variants)
    return variants, 'ABC'
 
def SUB10():
    # while len(variants) != 10:
    #     minuend = choice((100, 1000)) * randint(10, 99)
    #     subtrahend = choice((10, 100, 1000) if minuend//1000 else (10, 100)) * randint(1, 99)
 
    #     if not ((subtrahend%1000)//100 > (minuend%1000)//100) or not ((subtrahend%100)//10 > (minuend%100)//10):
    #         continue
 
    #     if [minuend, subtrahend, None] not in variants and minuend - subtrahend > 1000:
    #         variants.append([minuend, subtrahend, None])
 
    # first variant s_huns > 10
    variants = []
    m_huns = randint(12, 20)
    m_tens = randint(0, 8)
    s_huns = randint(11, min(m_huns - 1, 15))
    s_tens = randint(m_tens + 1, 9)
    minuend = 100 * m_huns + 10 * m_tens
    subtrahend = 100 * s_huns + 10 * s_tens
    variants.append([minuend, subtrahend, minuend-subtrahend])
 
    while len(variants) != 10:
        m_huns = randint(5, 20)
        m_tens = randint(0 if (m_huns >= 11) else 1, 8)
        s_huns = randint(1, min(m_huns - 1, 15))
        s_tens = randint(m_tens + 1, 9)
        minuend = 100 * m_huns + 10 * m_tens
        subtrahend = 100 * s_huns + 10 * s_tens
        variant = [minuend, subtrahend, minuend-subtrahend]
        if variant not in variants:
            variants.append(variant)
 
    shuffle(variants)
    return variants, 'ABC'
 
def MUL10():
    ''' NOTE:
    quotient is less than 1000
    '''
    variants = []
    factor1_list = [randint(2, 9) * item for item in repeat_list([10, 100, 1000], 2)]
 
    for factor1 in factor1_list:
        while True:
            factor2 = 10 * randint(2, 9)
            product = factor1 * factor2
 
            possibly_commuted = comm_unique(factor1, factor2, product, variants)
            if possibly_commuted and product < 1000000:
                variants.append(possibly_commuted)
                break
 
    return variants, 'ABC'
 
def DIV10():
    ''' NOTE:
    I added restrictions to match examples
    '''
    variants = []
    divisor_list = [randint(2, 9) * item for item in repeat_list([1, 10, 100, 1000], 2)]
 
    for divisor in divisor_list:
        while True:
            dividend = divisor * choice((1, 10, 100)) * randint(2, 9)
            quotient = dividend//divisor
 
            if [dividend, divisor, quotient] not in variants:
                if quotient <= 10000 and 100 < dividend < 1000000:
                    variants.append([dividend, divisor, dividend//divisor])
                    break
 
    return variants, 'ABC'
 
    # tps = [1, 10, 100, 1000]
    # mult10_divisor_list = [1] * 2 + [10] * 3 + [100] + 3 + [1000] * 2
    # mult10_dividend_list = tps[2:] + tps[1:] + tps[:3] + tps[:2]
    # #mult_divisor_list = [randint(1, 9)] + list(range(1, 10))
 
    # # want some randomness but cant shuffle mult lists
    # mult_index_list = list(range(10))
    # shuffle(mult_index_list)
 
    # mult_divisor_list = []
    # for mult in mult10_divisor_list:
         
 
    # while mult_index_list:
    #     index = mult10_index_list.pop()
    #     mult10_divisor = mult10_divisor_list[index]
    #     mult10_dividend = mult10_dividend_list[index]
    #     mult_divisor = mult_divisor_list.pop()
    #     # need to use all items in mult_index_list
    #     while True:
    #         divisor = mult_divisor * mult10_divisor
 
def level_maker(level, operation):
    '''operation should be a string'''
    op_str = ''
    if operation == '+':            op_str = 'ADD'
    elif operation == '-':          op_str = 'SUB'
    elif operation == '*':          op_str = 'MUL'
    elif operation in (':', '/'):   op_str = 'DIV'
    return eval(op_str + str(level) + '()')
 
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
            sep = str(level) + ' ' + operation
            output.write(sep + '\n')
 
            contents = []
 
            # generate 10 example levels
            while len(contents) < 10:
                # the 10 variants should be unique
                # how unique?
 
                lvl, missing_index = level_maker(level, operation)
 
                ## CHECK length
                if len(lvl) != 10:
                    print(sep + ' length issue!!!')
 
                ## CHECK UNIQUE VARIANTS
                if not check_unique(lvl):
                    print(sep + ' variant uniqueness issue!!!')
 
                for variant in lvl:
                    ## CHECK [0, 0, 0]
                    if variant[:2].count(0) > 1:
                        print(sep + ' too many AB zeros!!!')

                    ## CHECK negative result
                    if operation == '-' and (variant[0] - variant[1] < 0):
                        print(sep + ' negative result!!!')
 
                ## CHECK one None index
                lvl = remove_indices(missing_index, lvl)
                for variant in lvl:
                    if variant.count(None) != 1:
                        print(sep + ' number of None issue!!!')
                 
                     
                if str(lvl) not in contents:
                    if len(lvl) != 10:
                        print('Level ' + sep + ' length is ' + str(len(lvl)))
                    contents.append(str(lvl))
                    output.write(str(lvl) + '\n')
            output.write('\n')
    output.close()
 
make_output()