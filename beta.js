var VARS_PER_LVL = 10;
/** Fisher-Yates
 * Shuffles array in place. ES6 version
 * @param {Array} arr items An array containing the items.
 */
var shuffle = function (arr) {
    for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        _a = [arr[j], arr[i]], arr[i] = _a[0], arr[j] = _a[1];
    }
    return arr;
    var _a;
};
var count = function (arr, value) {
    var counter = 0;
    arr.forEach(function (elem) {
        if (elem === value)
            counter++;
    });
    return counter;
};
var zip = function () {
    var arrs = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        arrs[_i] = arguments[_i];
    }
    var zipped = [];
    var arr_length = arrs[0].length;
    // first lets check if the arguments were vaild
    for (var i = 0; i < arrs.length; i++) {
        if (arrs[i].length !== arr_length) {
            console.log("Arrays must be of same length.");
            return null;
        }
    }
    var _loop_1 = function (i) {
        var zipped_entry = [];
        arrs.forEach(function (arr) { return zipped_entry.push(arr[i]); });
        zipped.push(zipped_entry);
    };
    for (var i = 0; i < arr_length; i++) {
        _loop_1(i);
    }
    return zipped;
};
/**
 * Just like Python's random.randint
 *
 * @param low lowest possible number that can be returned
 * @param high highest possible number that can be returned
 */
var randint = function (low, high) { return Math.floor(low + Math.random() * high); };
var repeat_list = function (lst, times) {
    var repeated = [];
    for (var i = 0; i < times; i++) {
        repeated = repeated.concat(lst);
    }
    return repeated;
};
var remove_first_zero = function (variant) {
    /** Replace the fisrt occurence of 0 in an array with null. */
    if (variant.includes(0))
        variant[variant.indexOf(0)] = null;
    for (var i = 0; i < variant.length; i++) {
        if (variant[i] === 0) {
            variant[i] = null;
            break;
        }
    }
};
var remove_indices = function (variant_list, missing_index_options, max_repeats) {
    if (max_repeats === void 0) { max_repeats = 3; }
    /** Replace an index in a variant with null.
     *
     * Only replace the same index at most 3 times before the other indices have been replaced three times.
     */
    var variants = [];
    var missing_index_list = repeat_list(missing_index_options, max_repeats);
    shuffle(missing_index_list);
    missing_index_list = missing_index_list.concat(missing_index_list.slice(0, VARS_PER_LVL - missing_index_list.length));
    for (var i = 0; i < variant_list.length; i++) {
        var variant = variant_list[i];
        if (count(variant, 0) > 1)
            remove_first_zero(variant);
        else
            variant[missing_index_list[i]] = null;
        variants.push(variant);
    }
    return variants;
};
