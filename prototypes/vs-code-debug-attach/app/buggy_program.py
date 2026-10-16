"""A deliberately buggy exercise for the Debugging Gym prototype.

The bug is an off-by-one in the loop bound: the last element of the list is
never added to the total, so the average is wrong. It is a real, discoverable
defect that a learner finds by stepping through the code and inspecting the
loop variable.
"""


def average(nums):
    """Return the average of a list of numbers.

    Expected: average([1, 2, 3]) == 2.0
    """
    if not nums:
        return 0.0

    total = 0.0
    # BUG: off-by-one -- range(len(nums) - 1) skips the last element.
    for i in range(len(nums) - 1):
        total += nums[i]
    return total / len(nums)