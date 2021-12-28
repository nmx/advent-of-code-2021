from __future__ import annotations

from typing import List, Optional
import math


class Node(object):
    def __init__(self, parent: Optional[Pair], isright: bool):
        self.parent = parent
        self.isright = isright


class Pair(Node):
    def __init__(self, parent: Optional[Pair], isright: bool):
        super(Pair, self).__init__(parent, isright)
        self.left = None
        self.right = None


class RegNum(Node):
    def __init__(self, parent: Optional[Pair], isright: bool, val: int):
        super(RegNum, self).__init__(parent, isright)
        self.val = val


def q1(filename: str) -> int:
    with open(filename) as f:
        trees = strings_to_trees([s.strip() for s in f.readlines()])
        return magnitude(add_trees(trees))


def q2(filename: str) -> int:
    with open(filename) as f:
        strings = [s.strip() for s in f.readlines()]
        max_mag = 0

        for i in range(len(strings)):
            for j in range(len(strings)):
                if i == j:
                    continue
                mag = magnitude(add_trees([string_to_tree(strings[i]), string_to_tree(strings[j])]))
                max_mag = max(mag, max_mag)

        return max_mag


def string_to_tree(string: str) -> Pair:
    stack = []
    last_popped = None
    i = 0
    while i < len(string):
        c = string[i]
        parent = stack[-1] if stack else None
        isright = parent.left if parent else False
        if c == '[':
            stack.append(Pair(parent, isright))
        elif c.isnumeric():
            num = ""
            while string[i].isnumeric():
                num += string[i]
                i += 1
            i -= 1
            node = RegNum(parent, isright, int(num))
            if not stack[-1].left:
                stack[-1].left = node
            else:
                stack[-1].right = node
        elif c == ',':
            pass
        elif c == ']':
            last_popped = stack.pop()
            if stack:
                parent = stack[-1]
                if not parent.left:
                    parent.left = last_popped
                else:
                    parent.right = last_popped
        i += 1
    return last_popped  # root


def tree_to_string(node: Node) -> str:
    if isinstance(node, RegNum):
        return str(node.val)
    elif isinstance(node, Pair):
        return f"[{tree_to_string(node.left)},{tree_to_string(node.right)}]"
    raise ValueError(f"unhandled type {type(node)}")


def reduce(node: Node) -> None:
    while True:
        did_explode = explode(node)
        if not did_explode:
            did_split = split(node)
            if not did_split:
                return


def explode(node: Node, depth: int = 0) -> bool:
    if isinstance(node, RegNum):
        return False
    elif isinstance(node, Pair):
        if depth > 4:
            raise ValueError("max depth is 4")
        if depth == 4:
            assert isinstance(node.left, RegNum) and isinstance(node.right, RegNum)
            exploded = RegNum(node.parent, node.isright, 0)
            if node.isright:
                node.parent.right = exploded
            else:
                node.parent.left = exploded
            explode_left(node)
            explode_right(node)
            return True

        child_exploded = explode(node.left, depth + 1)
        if not child_exploded:
            child_exploded = explode(node.right, depth + 1)
        return child_exploded
    else:
        raise ValueError(f"unhandled type {type(node)}")


def explode_left(node: Pair) -> None:
    # go up until we find a left branch, then follow it to its rightmost descendant
    n = node
    while n:
        if n.parent and n.isright:
            n = n.parent.left
            while True:
                if isinstance(n, Pair):
                    n = n.right
                else:
                    n.val += node.left.val
                    return
        n = n.parent


def explode_right(node: Pair) -> None:
    # go up until we find a right branch, then follow it to its leftmost descendant
    n = node
    while n:
        if n.parent and not n.isright:
            n = n.parent.right
            while True:
                if isinstance(n, Pair):
                    n = n.left
                else:
                    n.val += node.right.val
                    return
        n = n.parent


def split(node: Node) -> bool:
    if isinstance(node, RegNum):
        if node.val >= 10:
            split_pair = Pair(node.parent, node.isright)
            split_pair.left = RegNum(split_pair, False, math.floor(node.val / 2))
            split_pair.right = RegNum(split_pair, True, math.ceil(node.val / 2))
            if node.isright:
                node.parent.right = split_pair
            else:
                node.parent.left = split_pair
            return True
        else:
            return False
    elif isinstance(node, Pair):
        child_split = split(node.left)
        if not child_split:
            child_split = split(node.right)
        return child_split
    else:
        raise ValueError(f"unhandled type {type(node)}")


def strings_to_trees(strings: List[str]) -> List[Pair]:
    return [string_to_tree(s) for s in strings]


def add_trees(trees: List[Pair]) -> Pair:
    result = None
    for tree in trees:
        result = merge_trees(result, tree)
        reduce(result)
    return result


def merge_trees(root_a: Pair, root_b: Pair) -> Pair:
    if not root_a:
        return root_b
    new_root = Pair(None, False)
    root_a.parent = new_root
    root_b.parent = new_root
    root_b.isright = True
    new_root.left = root_a
    new_root.right = root_b
    return new_root


def magnitude(node: Node) -> int:
    if isinstance(node, RegNum):
        return node.val
    elif isinstance(node, Pair):
        return 3 * magnitude(node.left) + 2 * magnitude(node.right)
    raise ValueError(f"unhandled type {type(node)}")


if __name__ == '__main__':
    print(f"Q1: {q1('input.txt')}")
    print(f"Q2: {q2('input.txt')}")