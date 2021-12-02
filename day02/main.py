class Sub(object):
    def __init__(self):
        self._depth = 0
        self._hpos = 0

    @property
    def depth(self):
        return self._depth

    @property
    def hpos(self):
        return self._hpos

    def follow_course(self, filename):
        with open(filename) as f:
            line = f.readline()
            while line:
                cmd, count = line.strip().split(' ')
                count = int(count)
                if cmd == 'forward':
                    self.forward(count)
                elif cmd == 'up':
                    self.up(count)
                elif cmd == 'down':
                    self.down(count)
                else:
                    raise ValueError(f"unknown command {cmd}")
                print(f"{cmd} {count} depth={self._depth} hpos={self._hpos}")
                line = f.readline()


class Sub1(Sub):
    def forward(self, count):
        self._hpos += count

    def down(self, count):
        self._depth += count

    def up(self, count):
        self._depth -= count


class Sub2(Sub):
    def __init__(self):
        super().__init__()
        self._aim = 0

    @property
    def aim(self):
        return self._aim

    def forward(self, count):
        self._hpos += count
        self._depth += self._aim * count

    def down(self, count):
        self._aim += count

    def up(self, count):
        self._aim -= count


def q(sub):
    sub.follow_course('input.txt')
    res = sub.depth * sub.hpos
    print(f"depth={sub.depth} hpos={sub.hpos} res={res}")


def q2():
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    q(Sub1())
    q(Sub2())

