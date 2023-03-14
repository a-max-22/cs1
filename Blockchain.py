
import hashlib
import time 

class Block:
    def __init__(self, hash1, index, time,  data) -> None:
        self.prevHash = hash1
        self.blockHash = ''
        self.index = index
        self.time = time
        self.data = data
        self.nonce = 0


class BlockChain:
    def __init__(self, numTrailingZeroes = 1) -> None:
        assert numTrailingZeroes < 32, "Too much trailing zeroes"
        self.numTrailingZeroes = numTrailingZeroes
        self.initialHash = "00000"
        initialBlock = Block(self.initialHash, index = 0, time = str(time.perf_counter()), data = '0' )
        self.computeBlockHash(initialBlock)
        self.blocks = [initialBlock]


    def hashFunc(self, block, nonce = None):
        hashStr = block.prevHash +  str(block.index) + block.time + block.data
        if nonce is None:
            hashStr += str(block.nonce)
        else:
            hashStr += str(nonce)

        hash_object = hashlib.md5(hashStr.encode('ascii'))
        return hash_object.hexdigest()

    def computeBlockHash(self, block):
        nonce = 0
        currentHash = ''
        while (True):
            currentHash = self.hashFunc(block, nonce)
            if currentHash[-1:-self.numTrailingZeroes] == '0'*self.numTrailingZeroes:
                block.nonce = nonce
                return currentHash
            nonce += 1

    def addNewBlock(self, data):
        lastBlock = self.blocks[-1]
        index = lastBlock.index + 1
        time = str(time.perf_counter())
        prevHash = lastBlock.blockHash
        
        newBlock = Block(prevHash, index, time, data)
        hash = self.computeBlockHash(newBlock)
        newBlock.blockHash = hash
        self.blocks.append(newBlock)


    def findBlockByHash(self, hashToFind):
        for block in self.blocks:
            if block.blockHash == hashToFind: return block
        return None

    
    def validateAllBlocks(self):
        prevHash = self.initialHash
        for block in self.blocks:
            blockHash = self.computeBlockHash(block)
            if blockHash != block.blockHash: return False
            if block.prevHash != prevHash: return False
        return True