const VARS_PER_LVL:number = 10;

/** Fisher-Yates
 * Shuffles array in place. ES6 version
 * @param {Array} arr items An array containing the items.
 */
let shuffle = (arr:any[]) => {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

/**
 * Check an array to see how many times a value appears in it.
 * Sub-arrays are not checked.
 * @param arr Array to be looped through.
 * @param value Value to be counted.
 */
let count = (arr:any[], value:any) => {
    let counter = 0;
    arr.forEach((elem) => { if (elem === value) counter++; });
    return counter;
}

/**
 * Just like Python's zip.
 * @param arrs Arrays of equal length to be zipped.
 */
let zip = (...arrs: number[][]) => {
    let zipped:number[][] = [];
    let arr_length = arrs[0].length;

    // first lets check if the arguments were valid
    for (let i = 0; i < arrs.length; i++) {
        if (arrs[i].length !== arr_length) {
            console.log("Arrays must be of same length.");
            return null;
        }        
    }

    for (let i = 0; i < arr_length; i++) {
        let zipped_entry:number[] = [];
        arrs.forEach((arr) => zipped_entry.push(arr[i]));
        zipped.push(zipped_entry);
    }
    return zipped;
}

/**
 * Just like Python's random.randint.
 * @param low Lowest possible return value.
 * @param high Highest possible return value.
 */
let randint = (low:number, high:number) => Math.floor(low + Math.random() * high);

/**
 * Check whether two arrays (with no sub arrays) are equal.
 * @param arr1 
 * @param arr2 
 */
let arrays_equal = (arr1:any[], arr2:any[]) => {
    if (arr1 === arr2) return true;
    if (arr1 == null || arr2 == null) return false;
    if (arr1.length !== arr2.length) return false;

    for (let i = 0; i < arr1.length; i++) {
        if (arr1[i] !== arr2[i]) return false;
    }
    return true;
};

/**
 * Check whether inner is contained in outer.
 * @param outer array that might contain inner
 * @param inner array with no sub arrays
 */
let array_in = (outer:any[], inner:any[]) => {
    outer.forEach((arr) => { if (arrays_equal(arr, inner)) return true; });
    return false;
}

/**
 * Concatenates a list to itself a specified number of times.
 * @param arr array to be repeated
 * @param times number of times to repeat the array
 */
let repeat_list = (arr:any[], times:number) => {
    let repeated:any[] = []
    for (let i = 0; i < times; i++) {
        repeated = repeated.concat(arr);
    }
    return repeated;
}

// /**
//  * Outdated by min_repeats & flags
//  * @param variant_list 
//  * @param missing_index_options 
//  * @param max_repeats 
//  */
// let remove_indices = (variant_list:number[][], missing_index_options:number[], max_repeats:number = 3) => {
//     /** Replace an index in a variant with null.
//      * 
//      * Only replace the same index at most 3 times before the other indices have been replaced three times.
//      */
//     let variants:(number|null)[][] = [];
//     let missing_index_list = repeat_list(missing_index_options, max_repeats);
//     shuffle(missing_index_list);
//     missing_index_list = missing_index_list.concat(missing_index_list.slice(0, VARS_PER_LVL - missing_index_list.length));

//     for (let i = 0; i < variant_list.length; i++) {
//         let variant:(number|null)[] = variant_list[i];
//         if (count(variant, 0) > 1) variant[variant.indexOf(0)] = null;
//         else variant[missing_index_list[i]] = null;
//         variants.push(variant);
//     }
//     return variants;
// }

let comm_choice = (left:number, right:number, result:number) => (Math.random() < 0.5) ? [left, right, result] : [right, left, result];

/**
 * 
 * @param min number of times to see each option before seeing any more
 * @param option_mask_arr Array of bit masks that specifies which conditions will be met at which indices.
 */
let min_repeats = (min:number, option_mask_arr:number[]) => {
    let output = repeat_list(option_mask_arr, min);
    shuffle(output);
    while (output.length < VARS_PER_LVL) output = repeat_list(output, 2);
    return output.slice(0, VARS_PER_LVL);
}

// /**Outdated by min_repeats
//  * Not great.. XYYXXY could be followed by XXX
//  * would be better to attach indices to condition satisfying variants
//  * 
//  * @param k the number of indices to check for condition in variants starting at the end
//  * @param condition 
//  * @param variants 
//  */
// let check_last_k_variants = (k:number, condition:string[], variants:number[][]) => {
//     // if (variants.length === 0) return 0;
//     // if (variants.length > k) k = variants.length;
//     // let last_k = 0;
//     // for (let i = variants.length - 1; i >= variants.length - k; i--) {
//     //     //if (condition satisfied at variants[i]) last_k++;
//     //     //else return last_k;
//     // }
//     //== new ==\\
    
// }


// // this will be unholy
// let generate_from = (operation:string, output_range:number[], operand1_list:number[], operand2_list:number[]|null=null, method:()=>number[]=()=>[], factor1:number[]|null=null, factor2:number[]|null=null) => {
//     let variant:number[];
//     let variants:number[][] = [];
//     let floor = output_range[0];
//     let ceil = output_range[1];
//     while (variants.length !== 10) {
//         if (operation === '+') {
//             if (floor === ceil) {
//                 operand1_list
//             }
//         }
//     }
// }

let make_variant = (operation:string, method:()=>number[]) => {}

