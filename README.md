# Sum-of-maximum-values-for-all-subarrays.

An approach, using stacks, to determine the number of subarrays in which a member of an integer array is the maximum value of that subarray. 

The frequency of subarrays in which an array member is the maximum can be determined by multiplying the number of spaces to the left and right of the member that are less than or equal to its value, plus one. 

For example:
In the array a = [1, 2, 4, 3]

The number of spaces to the left of each member + 1 are:
lefts = {1:1, 2:2, 4:3, 3:1}

To the right:
rights = {1:1, 2:1, 4:2, 3:1}

Multiplied together:
frequency = {1:1, 2:2, 4:6, 3:1}

To get our total we sum the products of key:value pairs:
Total = (1 * 1) + (2 * 2) + (4 * 6) + (3 * 1) = 32

If muliple members have the same value with no larger value between them we must account for subarrays in which both appear as the maximum. To do this we start as before, multiplying left and right values for each member. We then store the sum of these products. Then, we multiply the left value of the first duplicate member by the right of the second. If a third equal value is pressent, we multilply the second left by the third right and sum the total of products. We repeat this pattern for all multiple members of the same value as long as no array member with a higher value is encountered. 

For example:
In the array b = [2, 5, 4, 5, 1, 4, 5]

Considering only the values repeated without a higher value between, the number of spaces left + 1 are:
lefts = {5:(2, 4, 7)}

And to the right:
rights = {5:(6, 4, 1)}

Summing the products of right:left pairs:
frequency = (2 * 6) + (4 * 4) + (7 * 1) = 35

Accounting for shared subarrays:
frequeny -= ((2 * 4) + (4 * 1)) = 23

Now we can add 5 * 23 = 115 to our total.

So thats the logic behind the algorythm. I'm open to any and all suggestions for improvement!
