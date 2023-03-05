import unittest

from ExpressionParser import PlaceParenthesesInExpressionString, getOperandInParenthesis, getNumOperand


class TestOperandsExtraction(unittest.TestCase):
    def testParenthesisedOperandExtraction(self):
        expr = '(0 + (11 + 12))'
        expected = '0 + (11 + 12)'
        res, pos = getOperandInParenthesis(expr)
        self.assertEqual(res, expected)
        self.assertEqual(pos, len(expr)-1)


    def testParenthesisedOperandExtraction2(self):
        expr = '(0 + (11 + 12)) + 11'
        expected = '0 + (11 + 12)'
        res, pos = getOperandInParenthesis(expr)
        self.assertEqual(expected, res)
        self.assertEqual(pos, 14)

    def testNumOperand(self):
        expr = '111111 + 1'
        expected = '111111'
        res, pos = getNumOperand(expr)
        self.assertEqual(expected, res)
        self.assertEqual(pos, 5)


class TestPlaceParenthesesInExpressionString(unittest.TestCase):    
        
    def testSimpleOperation(self):
        expr = '1+2'
        expected = '(1+2)'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)
    
    def testSingleNumber(self):
        expr = '111'
        expected = '111'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)
    

        
    def testOperationsWithEqualPrecedence(self):
        expr = '11  + 22+  33 '
        expected = '(11+(22+33))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)
    
    def testOperationsWithNonEqualPrecedence(self):
        expr = '3 + 11 * 22 * 44  +  33'
        expected = '(3+((11*(22*44))+33))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)

    def testOperationsWithNonEqualPrecedence2(self):
        expr = '3 + 11 * 22 * 44  +  33 * 2 * 4'
        expected = '(3+((11*(22*44))+(33*(2*4))))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)

    def testOperationsWithNonEqualPrecedence4(self):
        expr = '3 + 11 * 22'
        expected = '(3+(11*22))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)

    
    def testSubExpressions2(self):
        expr = '(11+22)*(1+2)'
        expected = '((11+22)*(1+2))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)

    
    def testSubExpressions(self):
        expr = '(11+22+33)'
        expected = '(11+(22+33))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)

    def testSubExpressions3(self):
        expr = '(11+22)*(1+2+3)'
        expected = '((11+22)*(1+(2+3)))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)

    def testSubExpressions4(self):
        expr = '(11+22)*(1+2+3)*(5-4)'
        expected = '((11+22)*((1+(2+3))*(5-4)))'
        result, tokens = PlaceParenthesesInExpressionString(expr)
        self.assertEqual(result, expected)
