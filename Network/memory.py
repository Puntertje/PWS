from collections import deque
import numpy as np


class Memory:
    def __init__(self, maxSize):
        self.buffer = deque(maxlen=maxSize)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self, batchSize):
        buffer_size = len(self.buffer)
        index = np.random.choice(np.arange(buffer_size),
                                 size=batchSize,
                                 replace=False)
        return [self.buffer[i] for i in index]


class PrioritisedMemory:
    # some cheeky hyperparameters
    e = 0.01
    a = 0.06
    b = 0.04
    bIncreaseRate = 0.001
    errorsClippedAt = 1.0

    def __init__(self, capacity):
        self.sumTree = SumTree(capacity)
        self.capacity = capacity

    def store(self, experience):
        """ when an experience is first added to memory it has the highest priority
            so each experience is run through at least once
        """
        # get max priority
        maxPriority = np.max(self.sumTree.tree[self.sumTree.indexOfFirstData:])

        # if the max is 0 then this means that this is the first element
        # so might as well give it the highest priority possible
        if maxPriority == 0:
            maxPriority = self.errorsClippedAt

        self.sumTree.add(maxPriority, experience)

    def sample(self, n):
        batch = []
        batchIndexes = np.zeros([n], dtype=np.int32)
        batchISWeights = np.zeros([n, 1], dtype=np.float32)

        # so we divide the priority space up into n different priority segments
        totalPriority = self.sumTree.total_priority()
        prioritySegmentSize = totalPriority / n

        # also we need to increase b with every value to anneal it towards 1
        self.b += self.bIncreaseRate
        self.b = min(self.b, 1)

        # ok very nice now in order to normalize all the weights in order to ensure they are all within 0 and 1
        # we are going to need to get the maximum weight and divide all weights by that

        # the largest weight will have the lowest priority and thus the lowest probability of being chosen
        minPriority = np.min(np.maximum(self.sumTree.tree[self.sumTree.indexOfFirstData:], self.e))
        minProbability = minPriority / self.sumTree.total_priority()

        # formula
        maxWeight = (minProbability * n) ** (-self.b)
        for i in range(n):
            # get the upper and lower bounds of the segment
            segmentMin = prioritySegmentSize * i
            segmentMax = segmentMin + prioritySegmentSize

            value = np.random.uniform(segmentMin, segmentMax)

            treeIndex, priority, data = self.sumTree.getLeaf(value)

            samplingProbability = priority / totalPriority

            #  IS = (1/N * 1/P(i))**b /max wi == (N*P(i))**-b  /max wi

            batchISWeights[i, 0] = np.power(n * samplingProbability, -self.b) / maxWeight

            batchIndexes[i] = treeIndex
            experience = [data]
            batch.append(experience)

        return batchIndexes, batch, batchISWeights

    def batchUpdate(self, treeIndexes, absoluteErrors):
        absoluteErrors += self.e  # do this to avoid 0 values
        clippedErrors = np.minimum(absoluteErrors, self.errorsClippedAt)

        priorities = np.power(clippedErrors, self.a)
        for treeIndex, priority in zip(treeIndexes, priorities):
            self.sumTree.update(treeIndex, priority)


class SumTree:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 2 * capacity - 1
        self.tree = np.zeros(self.size)
        self.data = np.zeros(capacity, dtype=object)
        self.dataPointer = 0
        self.indexOfFirstData = capacity - 1

    """
    adds a new element to the sub tree (or overwrites an old one) and updates all effected nodes 
    """

    def add(self, priority, data):
        treeIndex = self.indexOfFirstData + self.dataPointer

        # overwrite data

        self.data[self.dataPointer] = data
        self.update(treeIndex, priority)
        self.dataPointer += 1
        self.dataPointer = self.dataPointer % self.capacity

    """
    updates the priority of the indexed leaf as well as updating the value of all effected
    elements in the sum tree
    """

    def update(self, index, priority):
        change = priority - self.tree[index]
        self.tree[index] = priority

        while index != 0:
            # set index to parent
            index = (index - 1) // 2
            self.tree[index] += change

    def getLeaf(self, value):
        parent = 0
        LChild = 1
        RChild = 2

        while LChild < self.size:
            if self.tree[LChild] >= value:
                parent = LChild
            else:
                value -= self.tree[LChild]
                parent = RChild

            LChild = 2 * parent + 1
            RChild = 2 * parent + 2

        treeIndex = parent
        dataIndex = parent - self.indexOfFirstData

        return treeIndex, self.tree[treeIndex], self.data[dataIndex]

    def total_priority(self):
        return self.tree[0]  # Returns the root node