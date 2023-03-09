
from enum import Enum

from ExpressionParser import TokenType, ANode
from ExpressionParser import Operators


class ASTNode:
    def __init__(self, val, parent):
        self.NodeValue = val 
        self.Parent = parent 
        self.Children = []
        self.Level = None
        self.NodesCountInSubtree = 0


def BuildAST(tokensList):    
    rootNode = ASTNode(val = None, parent=None)
    currentNode = rootNode
    for token in tokensList:        
        if token.tokenType == TokenType.Parenthesis and token.tokenValue == '(':
            newNode = ASTNode(val = None, parent = currentNode)
            currentNode.Children.append(newNode)
            currentNode = newNode
            continue
        
        if token.tokenType == TokenType.Parenthesis and token.tokenValue == ')':
            currentNode = currentNode.Parent
            continue
        
        if token.tokenType == TokenType.Operation:
            currentNode.NodeValue = token.tokenValue
            newNode = ASTNode(val = None, parent = currentNode)
            currentNode.Children.append(newNode)
            currentNode = newNode
            continue
        
        if token.tokenType == TokenType.Number:
            currentNode.NodeValue = token.tokenValue
            currentNode = currentNode.Parent
            continue

    return rootNode


def printTree(currentNode):
    if isinstance(currentNode.NodeValue, int):
        return str(currentNode.NodeValue)
    if currentNode.NodeValue in Operators.all_operators:
        return '(' + printTree(currentNode.Children[0]) + currentNode.NodeValue + printTree(currentNode.Children[1]) + ')'