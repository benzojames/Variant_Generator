condition = 'a<b'
def checker(a, b):
    return eval(condition)
 
#print(checker(1, 2))
 
conditions = ['all((a > 100, b > 100, a%10 == 0, b%10 == 0, a%100 != 0, (a + b)%100 == 0))']
def arr_checker(arr):
    for condition in conditions:
        counter = 0
        for [a, b, c] in arr:
            if eval(condition):
                counter += 1
        if counter != 3:
            return False
    return True
 
print(arr_checker([[150,150,300],[150,150,300],[150,150,300]]))