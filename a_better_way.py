"""This solution is O(n**2). See sum_sub_max for an O(n) solution."""

def distance_to_greater_value(arr: list, allow_equal: bool) -> list:
    """Creates array where each value indicates distance from arr[i] to a value in arr greater than arr[i].

    In order to avoid counting multiple maximums in a given subarray we count the distance to a strictly greater value
    in one direction and a greater or equal value in the opposite.
    For each value arr[i] we search for a value that is greater (or equal), if found we store its distance from i,
    otherwise we store the length of the array.

    :param arr: Array from which to determine sum of subarray maximums.
    :param allow_equal: Bool. If True, the index of values equal or greater than arr[i] are stored.
    :return:
    """
    next_greater_value = [0] * len(arr)
    stack = []

    for idx, num in enumerate(arr):
        if len(stack) == 0:
            stack.append(idx)
        elif num < arr[stack[-1]] or (allow_equal and num == arr[stack[-1]]):
            stack.append(idx)
        else:
            while len(stack) > 0 and ((allow_equal and num > arr[stack[-1]]) or
                                      (not allow_equal and num >= arr[stack[-1]])):
                idx2 = stack.pop()
                next_greater_value[idx2] = idx
            stack.append(idx)
    while len(stack) > 0:
        idx2 = stack.pop()
        next_greater_value[idx2] = len(arr)
    return next_greater_value


def subarray_maximum_total(arr: list) -> int:
    """Determines sum of maximum values of all subarrays of arr.
    The number of subarrays for which a given value represents the maximum can be found by multiplying the distance to
    a greater value in one direction and a greater/equal value in the opposite. We multiply this product by the original
    value to derive our total.
    Calls distance_to_greater_value().
    For each index i to_right and to_left store the distance from arr[i] to a value in arr that is greater than
    (or equal to) arr[i] to the right and left of i respectively.
    :param arr: arr whose subarray maximums we wish to total
    :return: int. total of all subarray maximums
    """
    len_arr = len(arr)

    to_right = distance_to_greater_value(arr, True)
    to_left = list(reversed([len_arr - x - 1 for x in distance_to_greater_value(list(reversed(arr)), False)]))

    total = 0
    for idx in range(len_arr):
        total += arr[idx] * (idx - to_left[idx]) * (to_right[idx] - idx)
    return total


if __name__ == "__main__":
    array = [-394, 488, 477, -588, 43, 477, 488, 488, -2, 2, 39, -588, 477, 478, 488, 2, 3, 4, 5, 4, 3, 2, 1]
    print(subarray_maximum_total(array))
