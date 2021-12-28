from unittest import TestCase

from main import *


class Test(TestCase):
    def test_tree_to_string(self):
        tests = [
            "[[[[[9,8],1],2],3],4]",
            "[7,[6,[5,[4,[3,2]]]]]",
            "[[6,[5,[4,[3,2]]]],1]",
            "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
            "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
            "[[3,[2,[8,0]]],[10,[5,[4,[3,2]]]]]"
        ]

        for s in tests:
            self.assertEqual(tree_to_string(string_to_tree(s)), s)

    def test_explode(self):
        tests = [
            ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
            ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
            ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
            ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
            ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
        ]

        for input, output in tests:
            root = string_to_tree(input)
            explode(root)
            self.assertEqual(tree_to_string(root), output)

    def test_split(self):
        tests = [
            ("[[[[0,7],4],[15,[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"),
            ("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]", "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        ]

        for input, output in tests:
            root = string_to_tree(input)
            split(root)
            self.assertEqual(tree_to_string(root), output)

    def test_reduce(self):
        root = string_to_tree("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        reduce(root)
        self.assertEqual(tree_to_string(root), "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

    def test_add_trees(self):
        tests = [
            (["[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"], "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
            (["[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
              "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
              "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
              "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
              "[7,[5,[[3,8],[1,4]]]]",
              "[[2,[2,2]],[8,[8,1]]]",
              "[2,9]",
              "[1,[[[9,3],9],[[9,0],[0,7]]]]",
              "[[[5,[7,4]],7],1]",
              "[[[[4,2],2],6],[8,7]]"],
             "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        ]

        for input, output in tests:
            trees = strings_to_trees(input)
            self.assertEqual(tree_to_string(add_trees(trees)), output)

    def test_magnitude(self):
        tests = [
            ("[[1,2],[[3,4],5]]", 143),
            ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488)
        ]

        for input, output in tests:
            self.assertEqual(magnitude(string_to_tree(input)), output)

    def test_q1(self):
        self.assertEqual(q1('sample.txt'), 4140)

    def test_q2(self):
        self.assertEqual(q2('sample.txt'), 3993)

