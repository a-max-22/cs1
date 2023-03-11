
from BuildAst import ASTNode
from ExpressionParser import Operators
import operator

operations = { '+': operator.add, '*': operator.mul, '-': operator.sub, '/':operator.truediv}

def interpretAstInternal(node):
    if node.NodeValue in Operators.all_operators:
        op1str, op1val = interpretAstInternal(node.Children[0])
        op2str, op2val = interpretAstInternal(node.Children[1])
        node.translationResult = '(' + op1str + node.NodeValue + op2str + ')'
        node.interpretationResult = operations[node.NodeValue](op1val, op2val)
        return  node.translationResult, node.interpretationResult 
    
    if isinstance(node.NodeValue, int):
        return str(node.NodeValue), node.NodeValue 

    
def interpretAst(rootNode):
    return  interpretAstInternal(rootNode)[1]

