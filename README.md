<h2>Sum of subarray maximums.</h2>

<h4>An O(n) approach (sum_sub_max.py) to determine the sum of the maximum value in each subarray of an integer array and an
O(n log n) approach (sum_sub_query.py) to determine the sum of subarray maximums for a number of slices of an integer 
array.</h4>

I came about this problem on a competitive programming site where it is listed among a few "advanced" problems. 
main.py represents an attempt at this after about three months of programming experience. I returned to the problem
a few months later and came up with a_better_way which I mistakenly thought was an O(n) solution (its O(n<sup>2</sup>)).
I could imagine an O(n) solution, but couldn't quite get there at the time. After a few more moths of study I finally
got it with sum_sub_max, but was passing only about 30% of tests before timing out. I caved and checked out the 
editorial solution. :disappointed: Presented in Java, with many single letter variable names and no commenting, it
wasn't immediately helpful. I had to pick up some Java and figure this thing out for good. So, finally, 
here is a Python solution involving a sweeping line and binary indexed trees. A Java version is 
[here](https://github.com/llpk79/sumsubmax/blob/master/src/Main.java). I'm still not quite to the point where I can clearly explain how all of the 
math here works exactly, so I still have some work left!

For example:

array = [1, 3, 2]

All subarrays of array are: [1], [1, 3], [1, 2, 3], [3], [3, 2], [2]

1 is the maximum of one subarray: [1]

3 is the maximum of four subarrays: [1, 3], [1, 3, 2], [3], [3, 2]

2 is the maximum of one subarray: [2]

1 + 3 + 3 + 3 + 3 + 2 = 15

This can be done much faster by using some principals of combinatorics and the distance from one array value to one that
is greater or equal.

In order to avoid counting multiple maximums in a given subarray, find a strictly greater value to the left and
a greater or equal value to the right of each array member, count the spaces between the member and the found values 
and add 1. If no such value is found, use the distance to the end of the array plus 1. The number of subarrays the 
member is a maximum of can be found by multiplying the distances found above. To calculate the sum of maximums for each 
array member simply multiply the value of the member by the number of subarrays in which it represents the maximum.

Iterate through the array:

index 0: value is 1, total is 0. There are no values greater to the left, so we use the distance to the end of the
    array plus one: 0 + 1 = 1. The distance to a greater or equal value to the right is 0 because it is 
    adjacent: 0 + 1 = 1. So, we multiply both distances and our value: 1 * 1 * 1 = 1. Add this to the total.

index 1: value is 3, total is 1. There are no values greater to the left, the distance to the end of the
    array plus one: 1 + 1 = 2. No value greater or equal exists to the right, so again we use the
    distance 1 + 1 = 2. Multiply both distances and the value: 2 * 2 * 3 = 12

index 2: value is 2, total is 13. A greater value is adjacent to the left. No values greater or equal exist to the 
right. Multiply as before: 1 * 1 * 2 = 2

Add it all up: 13 + 2 = 15
