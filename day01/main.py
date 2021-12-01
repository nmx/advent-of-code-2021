def q1():
    increments = 0
    oldval = None
    with open('input.txt') as f:
        line = f.readline()
        while line:
            val = int(line.strip())
            if oldval is not None and val > oldval:
                increments = increments + 1
            oldval = val
            line = f.readline()
    print(f"Q1: {increments}")


def q2():
    increments = 0
    measurements = []
    old_msum = None
    with open('input.txt') as f:
        line = f.readline()
        while line:
            val = int(line.strip())
            measurements.insert(0, val)
            if len(measurements) > 3:
                measurements.pop()
            if len(measurements) == 3:
                msum = sum(measurements)
                if old_msum is not None and msum > old_msum:
                    increments = increments + 1
                old_msum = msum
            line = f.readline()
    print(f"Q2: {increments}")


if __name__ == '__main__':
    q1()
    q2()
