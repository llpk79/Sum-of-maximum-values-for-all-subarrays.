class SumSubMaxQuery:

    """Calculate a number of range queries on an array to determine the sum of the maximum values of each subarray
    in the queried range in O(n log n).

    Instantiate with the array to query and an array of query range tuples. Use 1 indexing.
        array = [1, 3, 2]

        queries = [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

        sum_subs = SumSubMax(array, queries)

    Print by calling print_query_answers().

        sum_subs.print_query_answers

        1
        7
        15
        3
        8
        2
    """

    def __init__(self, array: list, queries: list) -> None:
        """Create class variables.

        :param array: An integer array.
        :param queries: List of tuples of query ranges.
        """
        self.array = array
        self.size = len(array)
        self.queries = queries
        self.event_list = []
        self.to_left = [0] * self.size
        self.to_right = [0] * self.size
        len_queries = len(queries)
        self.final_LR = [0] * len_queries
        self.final_L = [0] * len_queries
        self.final_R = [0] * len_queries
        self.final_C = [0] * len_queries
        self.save_array_info()

    def distance_to_greater_value(self) -> tuple:
        """Creates two arrays to_left and to_right where each value indicates the index of a value in array greater than
        (or equal to) array[i].

        In order to avoid counting multiple maximums in a given subarray we find a strictly greater value to_left and
        a greater or equal value to_right.
        For each value self.array[i] we search for a value that is greater (or equal), if found we store its index,
        otherwise we store -1 at to_left[i] or the len(array) at to_right[i].

        :return: (to_left, to_right)
        """
        stack = []
        for idx, num in enumerate(self.array):
            if not stack:
                stack.append(idx)
            elif num <= self.array[stack[-1]]:
                stack.append(idx)
            else:
                while stack and num > self.array[stack[-1]]:
                    index = stack.pop()
                    if stack:
                        self.to_left[index] = index - (index - stack[-1])
                        self.to_right[index] = self.size + (idx - self.size)
                    else:
                        self.to_left[index] = index - (index + 1)
                        self.to_right[index] = self.size + (idx - self.size)
                stack.append(idx)
        while stack:
            index = stack.pop()
            if stack:
                self.to_left[index] = index - (index - stack[-1])
                self.to_right[index] = self.size
            else:
                self.to_left[index] = -1
                self.to_right[index] = self.size
        return self.to_left, self.to_right

    def add_quadrant(self, start_start, end_start, start_end, end_end, qlr, ql, qr, qc):
        """Ensure quadrant values are valid, add start/end indexes and quadrant information to events.

        :param start_start: start of left edge of quadrant.
        :param end_start: end of left edge of quadrant.
        :param start_end: start of right edge of quadrant.
        :param end_end: end of right edge of quadrant.
        :param qlr: left-right quadrant.
        :param ql: left quadrant.
        :param qr: right quadrant.
        :param qc: center quadrant.
        :return:
        """
        if start_start > end_start or start_end > end_end:
            return

        self.event_list.append(Event.add_quad_start(start_start, start_end, end_end, qlr, ql, qr, qc))
        self.event_list.append(Event.add_quad_end(end_start, start_end, end_end, qlr, ql, qr, qc))

    def add_events(self):
        """Find boundaries of the range of subarray quadrants array[i] is a maximum of."""
        to_left, to_right = self.distance_to_greater_value()
        for i in range(self.size):
            next_to_left = to_left[i] + 1
            next_to_right = to_right[i] - 1
            self.add_quadrant(0, next_to_left - 1, next_to_right + 1, self.size - 1,
                              0, 0, 0,
                              (i - next_to_left + 1) * (next_to_right - i + 1) * self.array[i])
            self.add_quadrant(next_to_left, i, next_to_right + 1, self.size - 1,
                              0, (i - next_to_right - 1) * self.array[i], 0,
                              (i + 1) * (next_to_right - i + 1) * self.array[i])
            self.add_quadrant(0, next_to_left - 1, i, next_to_right,
                              0, 0, (i - next_to_left + 1) * self.array[i],
                              (1 - i) * (i - next_to_left + 1) * self.array[i])
            self.add_quadrant(next_to_left, i, i, next_to_right,
                              -self.array[i], (i - 1) * self.array[i], (i + 1) * self.array[i],
                              ((-1 * i * i) + 1) * self.array[i])
        for i in range(len(self.queries)):
            self.event_list.append(Event.add_query_point(self.queries[i][0], i))

    # noinspection PyShadowingNames
    def calc_quad_prefix_sums(self):
        """Calculate prefix sums for quadrant ranges for each event and save in an array..

        """
        events = sorted(self.event_list, key=lambda event: (event.index, event.event))
        qlr, ql, qr, qc = Fenwick(self.size), Fenwick(self.size), Fenwick(self.size), Fenwick(self.size)
        for event in events:
            if event.event == -1 or event.event == 1:
                qlr.add(event.left, event.right, event.qlr * -event.event)
                ql.add(event.left, event.right, event.ql * -event.event)
                qr.add(event.left, event.right, event.qr * -event.event)
                qc.add(event.left, event.right, event.qc * -event.event)
            if event.event == 0:
                right_of_slice = self.queries[event.query_number][1]
                self.final_LR[event.query_number] = qlr.get_total(right_of_slice)
                self.final_L[event.query_number] = ql.get_total(right_of_slice)
                self.final_R[event.query_number] = qr.get_total(right_of_slice)
                self.final_C[event.query_number] = qc.get_total(right_of_slice)

    def save_array_info(self):
        """Helper function calling add_events and calc_quad_prefix_sums."""
        self.add_events()
        self.calc_quad_prefix_sums()

    def print_query_answers(self):
        """Iterate through queries and print results."""
        for i in range(len(self.queries)):
            left, right = self.queries[i]
            print(self.final_LR[i] * left * right + self.final_L[i] * left + self.final_R[i] * right + self.final_C[i])


class Fenwick:

    """A binary index tree."""

    def __init__(self, length):
        self.size = length
        self.array = [0] * self.size

    def get_total(self, index):
        total = 0
        while index >= 0:
            total += self.array[index]
            index = (index & (index + 1)) - 1
        return total

    def add(self, left, right, value):
        if left > right:
            return
        self._add(right + 1, -value)
        self._add(left, value)

    def _add(self, index, value):
        while index < self.size:
            self.array[index] += value
            index = (index | (index + 1))


class Event:

    """Stores information about quadrant range and value."""

    def __init__(self, index, event, left, right, qlr, ql, qr, qc, query_number):
        """

        :param index: Index of event start or end.
        :param event: Type of event. start = -1, end = 1, query start = 0.
        :param left: The left edge of the right side of the quadrant.
        :param right: The right edge of the right side of the quadrant.
        :param qlr: left-right quadrant.
        :param ql: left quadrant.
        :param qr: right quadrant.
        :param qc: center quadrant.
        :param query_number: query number.
        """
        self.index = index
        self.event = event
        self.left = left
        self.right = right
        self.qlr = qlr
        self.ql = ql
        self.qr = qr
        self.qc = qc
        self.query_number = query_number

    @staticmethod
    def add_quad_start(index, left, right, qlr, ql, qr, qc):
        """Create an event at start of quadrant."""
        return Event(index, -1, left, right, qlr, ql, qr, qc, -1)

    @staticmethod
    def add_quad_end(index, left, right, qlr, ql, qr, qc):
        """Create an event at end of quadrant."""
        return Event(index, 1, left, right, qlr, ql, qr, qc, -1)

    @staticmethod
    def add_query_point(start, query_number):
        """Create a query point event."""
        return Event(start, 0, -1, -1, -1, -1, -1, -1, query_number)


if __name__ == "__main__":
    pass
