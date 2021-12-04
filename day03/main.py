def q1(bits, nums):
    gamma_str = ''
    for b in range(bits):
        gamma_str = gamma_str + most_common(b, nums, False)
    gamma = int(gamma_str, 2)

    epsilon = (2 ** bits - 1) ^ gamma

    print(f"Gamma rate: {gamma}")
    print(f"Epsilon rate: {epsilon}")
    print(f"Power consumption: {gamma * epsilon}")


def q2(bits, nums):
    o2 = int(calc_life_support(bits, nums, False), 2)
    co2 = int(calc_life_support(bits, nums, True), 2)
    print(f"O2 generator rating: {o2}")
    print(f"CO2 scrubber rating: {co2}")
    print(f"Life support rating: {o2 * co2}")


def calc_life_support(bits, nums, invert):
    nums = nums.copy()

    for b in range(bits):
        if len(nums) == 1:
            return nums[0]
        mc = most_common(b, nums, invert)
        nums = [num for num in nums if num[b] == mc]

    if len(nums) > 1:
        raise ValueError("Too many values left")
    return nums[0]


def most_common(bit, nums, invert):
    num_0 = 0
    num_1 = 0
    for num in nums:
        if num[bit] == '1':
            num_1 = num_1 + 1
        else:
            num_0 = num_0 + 1

    if num_1 > num_0:
        return '0' if invert else '1'
    elif num_0 > num_1:
        return '1' if invert else '0'
    else:
        return '0' if invert else '1'


if __name__ == '__main__':
    with open('input.txt') as f:
        nums = [line.strip() for line in f.readlines()]
    bits = len(nums[0])

    q1(bits, nums)
    print()
    q2(bits, nums)
