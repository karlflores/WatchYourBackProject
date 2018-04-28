from heapq import heapify, heappop, heappush
import heapq

class PriorityQueue:
    def __init__(self):
        pass

    @staticmethod
    def pop_min(pq):
        if isinstance(pq,list) is False:
            return None

    @staticmethod
    def pop_max(pq):
        if isinstance(pq,list) is False:
            return None
        if len(pq) > 0:
            return heapq
    @staticmethod
    def enqueue(pq,item):
        heappush(pq,item)

    @staticmethod
    def dequeue(pq,item):
        return heappop(pq)

    @staticmethod
    def size(pq):
        return len(pq)

    @staticmethod
    def peek(pq):
        if len(pq) > 0:
            return pq[0]
        else:
            return None

    @staticmethod
    def replace(pq,old,new):
        if len(pq) > 0:
            pass

    @staticmethod
    def heapmax(pq):
        heapq._heapify_max(pq)



