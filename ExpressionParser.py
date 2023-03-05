
from enum import Enum

class TokenType(Enum):
    Parenthesis = 0
    Operation   = 1
    Number      = 2


class ANode:
    def __init__(self, tokenType:TokenType, tokenValue):
        self.tokenType = tokenType
        self.tokenValue = tokenValue


def getOperandInParenthesis(inStr):
    score = 0
    for i in range(len(inStr)):
        c = inStr[i]
        if c == '(': 
            score += 1
        if c == ')':
            score -= 1
        if score < 0: raise ValueError("incorrect exression")
        if score == 0: return inStr[1 : i], i


def getNumOperand(inStr):
    for i in range(len(inStr)):
        if inStr[i].isdigit(): continue
        if i != 0: return inStr[0 : i], i-1
        return None, None

    return inStr, len(inStr) - 1


def extractOperand(inputStr):
    if len(inputStr) == 0:
        return ''
    
    if inputStr[0] == '(':
        firstOperand, pos = getOperandInParenthesis(inputStr)
        return firstOperand, pos

    if inputStr[0].isdigit():
        firstOperand, pos = getNumOperand(inputStr)
        return  firstOperand, pos

    return None, None


class Operators: 
    add_operators = frozenset(['+', '-'])
    mul_operators = frozenset(['*', '/'])
    all_operators = frozenset(['+', '-', '*', '/']) 


def getOperandsOfHigherPrecedence(exprList):
    prevItem = None
    result = []
    pos = -1
    for item in exprList:
        pos =+ 1
        if item not in Operators.all_operators:
            prevItem = item
        if item in Operators.mul_operators and prevItem is not None:
            result.append(prevItem)
        else:
            break
    return result, pos


def processExpressionsList(exprList):
    if exprList == []: return []

    item = exprList[0]

    isHighPriorityItem = (isinstance(item, list) and not isinstance(item, str))
    if isHighPriorityItem and len(exprList[1:]) > 0:
        return ['('] + processExpressionsList(item) + [')'] + processExpressionsList(exprList[1:]) 
    
    if isHighPriorityItem and len(exprList[1:]) == 0:
        return processExpressionsList(item)

    if item.isdigit():
        return [item] + processExpressionsList(exprList[1:])
    
    if item in Operators.all_operators:
        processResult = processExpressionsList(exprList[1:])
        if len(processResult) == 1:
            return [item] + processResult
        else:
            return [item] + ['('] + processResult + [')'] 
    
    return [item] + processExpressionsList(exprList[1:])



def groupHighPriorityOperands(exprList):
    if len(exprList) <= 1: return exprList

    prevOperand = None
    currentGroup = []
    result = []

    for item in exprList:        
        if item not in  Operators.all_operators:
            prevOperand = item
            continue
        op = item
        if op in Operators.mul_operators:
            currentGroup.append(prevOperand)
            currentGroup.append(op)
            continue

        if currentGroup != []:
           currentGroup.append(prevOperand)
           result.append(currentGroup)
           currentGroup = []
        else:
            result.append(prevOperand)
        
        result.append(op)

    if currentGroup != []:
        currentGroup.append(prevOperand)
        result.append(currentGroup)
    else:    
        result.append(prevOperand)
    
    return result


def makeNodesArray(resultExprArray):
    nodesArray = []
    for item in resultExprArray:
        if item.isdigit(): 
            nodesArray.append(ANode(tokenType=TokenType.Number, tokenValue=int(item)))
            continue
        if item in Operators.all_operators:
            nodesArray.append(ANode(tokenType=TokenType.Operation, tokenValue=item))
            continue
        if item == '(' or item == ')': 
            nodesArray.append(ANode(tokenType=TokenType.Parenthesis, tokenValue=item))
            continue

        resultSubExprArray, isSubExpressionCorrect = processExpression(item)
        if not isSubExpressionCorrect:
            return None, False
        if isSubExpressionCorrect and len(resultExprArray) > 1:
            nodesArray += [ANode(tokenType=TokenType.Parenthesis, tokenValue='(')] + resultSubExprArray +\
                          [ANode(tokenType=TokenType.Parenthesis, tokenValue=')')]
        if isSubExpressionCorrect and len(resultExprArray) == 1:
            nodesArray += resultSubExprArray
    
    return nodesArray, True


def processExpression(inStr):
    inputStrIsFinished = False
    currentStr = inStr

    isExpressionCorrect = True
    exprList = []
    
    while not inputStrIsFinished:
        operand, operandLastChar = extractOperand(currentStr)
        if operand is None:
            isExpressionCorrect = False
            return None, isExpressionCorrect

        exprList.append(operand)

        currCharIndex = operandLastChar + 1
        if (currCharIndex  >= len(currentStr)): break
        
        operation = currentStr[currCharIndex]
        if operation not in Operators.all_operators:
            return None, False
        
        currCharIndex += 1 
        if (currCharIndex  >= len(currentStr)): 
            return None, False

        exprList.append(operation)
        currentStr = currentStr[currCharIndex:]
    
    groupedExprItems = groupHighPriorityOperands(exprList)
    resultExprArray =  processExpressionsList(groupedExprItems)


    nodesArray, isExpressionCorrect =  makeNodesArray(resultExprArray)
    return nodesArray, isExpressionCorrect



def PlaceParenthesesInExpressionString(exprString):
    inputStr = exprString.replace(' ', '')
    tokens, isExprCorrect = processExpression(inputStr)
    if not isExprCorrect:
        return None
    
    if not (len(tokens) == 1 and tokens[0].tokenType == TokenType.Number):
        tokens = [ANode(tokenType=TokenType.Parenthesis, tokenValue='(')] + tokens + \
                 [ANode(tokenType=TokenType.Parenthesis, tokenValue=')')] 
    
    resultStr = ''
    for token in tokens: resultStr += str(token.tokenValue)

    return  resultStr, tokens
