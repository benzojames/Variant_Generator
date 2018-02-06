// where do special options belong?

type IB = number|boolean;
interface options {
    semiRandomAValues?:boolean;     // involves randint
    semiRandomBValues?:boolean;     // involves randint
    isAUnique?:boolean;             // a1 !== a2
    isABUnique?:boolean;            // (a1 or b1) !== (a2 or b2)
    isCSpecified?:boolean;          // eg A + B = 10
    isBFromA?:boolean;              // b = f(a)
    randomOnes?:boolean;            // ones digit is randint(1, 9) (maybe 0 sometimes)
    crossover11?:IB;                // a%10 + b%10 > 10
    crossover101?:IB;               // a%100 + b%100 > 100
    divisibleByN?:IB;               // a = N*randint...
    missingA?:IB;
    missingB?:IB;
    missingC?:IB;
    minC?:number;
    maxC?:number;
    maxZeros?:number;

}

let add1:options = {
    semiRandomAValues:false,
    isAUnique:true,
    //isBFromA:true,
    isCSpecified:true,
    missingA:3,
    missingB:3
}

let COUNTER = 0;
let flag1 = COUNTER;
let flag2 = 2**COUNTER++;
let flag3 = 2**COUNTER++;



/* OPTION FLAGS
 *
 * divisibleByN
 * isSpecificNumber
 * addsTo10
 * addsTo100
 * crossover11
 * crossover101
 * missingA
 * missingB
 * missingC
 * missingAB
 * missingABC
 * only_one         // A or B not BOTH have these options
 * both             // should A & B both have these options
 * 
 * 
 */

/* OTHER OPTIONS
 * min_result
 * max_result
 * min_repeats
 * 
 */ 


/* 
 * check repeat conditions
 * generate first set
 * look back to satisfy further repeats
 * check if special variants
 * if so put them in the right place
 * 
 * Eg
 * if (options & divisibleByN)
 *  a = randint(1, 9) * N
 * 
 */


class Variant {
    
}

let ten_multiple_factor = (variants:number[][]) => {
    let indices = [];
    let double_indices = []
    for (let i = 0; i < variants.length; i++) {
        if (variants[i][0] !== 0 && variants[i][0]%10 === 0) indices.push(i);
        if (variants[i][1] !== 0 && variants[i][1]%10 === 0) {
            if (indices.includes(i)) double_indices.push(i);
            else indices.push(i);
        }
    }
    return [indices, double_indices]
}

let conditions = {
    ten_multiple_factor: ten_multiple_factor;    
}