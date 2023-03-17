


def make_2_dimesional_array(N, M):
    arr = []
    for i in range(N):
        arr.append([])
        for j in range(M):
            arr[i].append(0)
    return arr

def readWeigthsFromLine(line,lineNum):
    weights = []
    for i in line:
        assert i.isdigit(), ("wrong symbol %s in line %d") % (i, lineNum)
        weights.append(int(i))

    return weights

def readValuesFromFile(fileName, height, width):
    weights = []
    with open(fileName, 'r') as file:
        lineNum = 0            
        for line in file:
            assert len(line) == width, ("symbols count in line %d doesn't correspond to width") % lineNum 
            weightsLine = readWeigthsFromLine(line, lineNum)
            weights.append(weightsLine)
        lineNum += 1
        assert lineNum == height,  ("symbols count in file %s doesn't correspond to width") % fileName

    return weights




class Perceptron:
    def __init__(self, N, M, threshold = 35) -> None:
        self.height = N
        self.width  = M
        self.weights = make_2_dimesional_array(N,M)
        self.threshold = threshold
    
    
    def evaluateActivationFunc(self, fileName):
        values = readValuesFromFile(fileName, self.height, self.width)
        sum = 0
        for i in range(self.height):
            for j in range(self.width):
                sum += self.weights[i][j] * values[i][j]

        return sum > self.threshold

