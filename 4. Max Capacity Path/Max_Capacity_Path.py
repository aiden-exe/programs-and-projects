class MaxHeap:
    '''Stores a MaxHeap with each element as (key, value)
        along with a pointers list storing at what index each key is'''

    def __init__(self, data = None):
        if data == None:
            self._data = []
            self._pointers = []

        else:
            self._data = list(enumerate(data))
            self._pointers = [i for i in range(len(data))]
            self.buildHeap()

    def __len__(self):
        return len(self._data)

    def isEmpty(self):
        return len(self) == 0

    def value(self, index):
        return self._data[index][1]

    def getIndex(self, key):
        return self._pointers[key]

    def swap(self, index1, index2):
        self._pointers[self._data[index1][0]], self._pointers[self._data[index2][0]] = \
        self._pointers[self._data[index2][0]], self._pointers[self._data[index1][0]]

        self._data[index1], self._data[index2] = self._data[index2], self._data[index1]

    def __HeapDown(self, index):
        if 2*index + 1 >= len(self):
            return
        
        if 2*index + 2 == len(self):
            if self.value(index) < self.value(2*index + 1):
                self.swap(index, 2*index + 1)
        
            return
        
        maxChild = 2*index + 1
        if self.value(maxChild) < self.value(2*index + 2):
            maxChild = 2*index + 2

        if self.value(index) < self.value(maxChild):
            self.swap(index, maxChild)
            self.__HeapDown(maxChild)
        
    def __HeapUp(self, index):
        if index == 0:
            return

        if self.value(index) > self.value((index-1)//2):
            self.swap(index, (index-1)//2)
            self.__HeapUp((index-1)//2)        

    def buildHeap(self):
        for i in range(len(self)//2, -1, -1):
            self.__HeapDown(i)

    def changeValue(self, key, newValue):
        index = self.getIndex(key)
        oldValue = self.value(index)

        self._data[index] = (key, newValue)

        if oldValue < newValue:
            self.__HeapUp(index)
            return
        self.__HeapDown(index)
        return

    def insert(self, data):
        self._data.append(data)
        self._pointers[data[0]] = len(self) - 1
        self.__HeapUp(len(self)-1)
        
    def extractMax(self):
        self.swap(0, len(self)-1)
        max = self._data.pop()

        self._pointers[max[0]] = None

        self.__HeapDown(0)
        return max           


class Graph:
    def __init__(self, n = 0, links = None):
        self.AdjacencyList = [list() for i in range(n)]

        for edge in links:
            self.addEdge(edge[0], edge[1], edge[2])

    def isAdjacent(self, v1, v2) -> bool:
        for i in self.AdjacencyList[v1]:
            if i[0] == v2:
                return True
        return False

    def ListNeighbours(self, v) -> list:
        return self.AdjacencyList[v]

    def addEdge(self, v1, v2, weight) -> None:
        self.AdjacencyList[v1].append((v2, weight))
        self.AdjacencyList[v2].append((v1, weight))


def findMaxCapacity(n, links, s, t):
    network = Graph(n, links)
    Capacity = [-1 for i in range(n)]   # Max capacity path to each vertex i

    # Stores the second last node in the max capacity path from s to vertex i
    Predecessor = [None for i in range(n)]  
    
    # Sets the capacity from s to s as infinite
    Capacity[s] = float("inf")

    CapacityHeap = MaxHeap(data=Capacity)

    while not CapacityHeap.isEmpty():
        # Run a modified Dijkstra's Algorithm
        currentVertex, currentMax = CapacityHeap.extractMax()

        for edge in network.AdjacencyList[currentVertex]:
            neighbour = edge[0]
            if Capacity[neighbour] < min(currentMax, edge[1]):
                # Then we have a new higher capacity path to vertex "neighbour"
                Capacity[neighbour] = min(currentMax, edge[1])
                Predecessor[neighbour] = currentVertex

                CapacityHeap.changeValue(neighbour, Capacity[neighbour])

    path = [t]

    while path[-1] != s:
        path.append(Predecessor[path[-1]])
    path.reverse()

    return (Capacity[t], path)


if __name__ == "__main__":
    print(findMaxCapacity(3,[(0,1,1),(1,2,1)],0,1))