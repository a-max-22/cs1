import unittest

from InterpretAst import interpretAst
from BuildAst import BuildAST
from ExpressionParser import PlaceParenthesesInExpressionString

class TestBuildASt(unittest.TestCase):
    def testInterpretAst(self):
        expr = '(7 + (11 + 12))'
        expected = 7+11+12
        resultStr, tokens = PlaceParenthesesInExpressionString(expr)
        resultASt = BuildAST(tokens)
        value = interpretAst(resultASt)
        self.assertEqual(expected, value)