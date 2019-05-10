#Class of available objects
class BinaryHeap_available(object):
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def isEmpty(self):
        if self.currentSize == 0:
            return 1
        else:
            return 0

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapList[i].times[2] > self.heapList[i // 2].times[2]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2

    def insert(self, newItem):
        self.heapList.append(newItem)
        self.currentSize += 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.maxChild(i)
            if self.heapList[i].times[2] < self.heapList[mc].times[2]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def maxChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2].times[2] > self.heapList[i*2+1].times[2]:
                return i * 2
            else:
                return i * 2 + 1

    def delMax(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize += -1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while (i > 0):
            self.percDown(i)
            i += -1
