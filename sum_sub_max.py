class SumSubMax:

    """Sum the maximum values in all subarrays of an integer array in O(n).

    array = [1, 3, 2]

    All subarrays of array are: [1], [1, 3], [1, 2, 3], [3], [3, 2], [2]

    1 is the maximum of one subarray: [1]

    3 is the maximum of four subarrays: [1, 3], [1, 3, 2], [3], [3, 2]

    2 is the maximum of one subarray: [2]

    1 + 3 + 3 + 3 + 3 + 2 = 15

    In order to avoid counting multiple maximums in a given subarray, find a strictly greater value to the left and
    a greater or equal value to the right. If no such value is found, use the distance to the end of the array + 1.
    The number of subarrays a value is a maximum of can be found by multiplying the distances found above.
    To calculate the sum of maximums for each index simply multiply the value by the number of subarrays in which it
    represents the maximum.


    index 0: value is 1. There are no values greater to the left, so we use the distance to the end of the
        array plus one: 0 + 1 = 1. The distance to a greater or equal value to the right is 1. So, we multiply both
        distances and our value: 1 * 1 * 1 = 1
    index 1: value is 3. There are no values greater to the left, the distance to the end of the
        array plus one: 1 + 1 = 2. No value greater or equal exists to the right, so again we use the
        distance 1 + 1 = 2. Multiply both distances and the value: 2 * 2 * 3 = 12
    index 2: value is 2. A greater value is just one space to the left. No values greater or equal exist to the right.
        Multiply as before: 1 * 1 * 2 = 2
    Add it all up: 1 + 12 + 2 = 15
    """

    def __init__(self, array: list) -> None:
        """Initialize a stack and int to track total.

        :param array: Array for which the sum of subarray maximums is required.
        """
        self.array = array
        self.size = len(array)
        self.stack = []
        self.total = 0

    def sum_subs(self) -> int:
        """Calculate and return the sum of maximum values for each subarray of self.array in O(n).

        Use a stack to keep track of indexes. If the current array value is larger than the value at the index at the
        top of the stack, pop from the stack and calculate the distance from the popped index to the current index,
        repeating until the current value is <= value at index at top of stack. Otherwise, add the current index to the
        stack and continue iterating.


        :return: Sum of subarray maximums.
        """
        for idx, num in enumerate(self.array):
            if not self.stack:
                self.stack.append(idx)
            elif num <= self.array[self.stack[-1]]:
                self.stack.append(idx)
            else:
                while self.stack and num > self.array[self.stack[-1]]:
                    index = self.stack.pop()
                    if self.stack:
                        # The next >= value is at array[stack[-1]].
                        self.total += self.array[index] * (index - self.stack[-1]) * (idx - index)
                    else:
                        # If the stack is empty array[index] is the largest value seen so far.
                        self.total += self.array[index] * (index + 1) * (idx - index)
                self.stack.append(idx)
        # The end of the array has been reached. Calculate the values remaining in the stack.
        while self.stack:
            index = self.stack.pop()
            if self.stack:
                self.total += self.array[index] * (index - self.stack[-1]) * (self.size - index)
            else:
                # the largest (or first instance of the largest) value in array.
                self.total += self.array[index] * (index + 1) * (self.size - index)
        return self.total


if __name__ == "__main__":
    pass
