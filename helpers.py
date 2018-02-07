from random import shuffle, choice, randint
 
def remove_indices(options, variant_list):
    """Replace some indices in a list with None.
 
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
    elif options == 'C':
        return variant_list
    else:
        # perhaps the option was invalid
        return None
    # don't have 4 in a row all missing A or all missing B
    # 30% liklihood of having 3 in a row
    missing *= max_repeats
    shuffle(missing)
    # once maximums have been satisfied, repeat
    missing += missing[:10 - len(missing)]
 
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
    until it has 10 values.
    This value takes the values in B and returns a shuffled list of length 10
    that satisfies the above repetition condition.
    '''
    lst = input_list * minimum
    shuffle(lst)
    lst += lst[:10 - len(lst)]
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
    while len(variants) != 10:
        ''' NOTE:
        reset see once all values are used
        when reset occurs, this could lead to at most 4 questions
        in a row that share a multiplicant
 
        We want to see all values in inputs minimum times before we see any of them
        more than minimum times.
        '''
        to_see = input_list * minimum
        while to_see and len(variants) != 10:
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
    '''This can help with min_before_repeat conditions.'''
    output = lst * num
    shuffle(output)
    mult = 10//len(output) + 1
    output *= mult
    return output[:10]
 
def add_if_unique(variant, variants):
    if variant not in variants:
        variants.append(variant)
 
def check_unique(variants):
    for variant in variants:
        if variants.count(variant) != 1:
            return False
    return True