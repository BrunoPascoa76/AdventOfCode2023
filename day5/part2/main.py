from parse import parse
from bisect import bisect_left
from time import perf_counter_ns

class Range:
    def __init__(self,start,end,diff):
        self.start=start
        self.end=end
        self.diff=diff
    
    def contains(self,value):
        return self.start<=value<=self.end
    
    def convert(self,start,end):
        if start>end:
            return [],[]
        elif self.start<=start and end<=self.end:
            return [(start+self.diff,end+self.diff)],[]
        elif start<=self.start and self.end<=end:

            return [(self.start+self.diff,self.end+self.diff)],[(start,self.start-1),(self.end+1,end)]
        elif start<=self.start and end<=self.end:
            return [(self.start+self.diff,end+self.diff)],[(start,self.start-1)]
        elif self.start<=start and self.end<=end:
            return [(start+self.diff,self.end+self.diff)],[(self.end+1,end)]
        else:
            return [],[]


class ConversionNode:
    def __init__(self):
        self.next=None
        self.ranges=[]

    def add_next(self, node):
        if self.next is None:
            self.next=node
        else:
            self.next.add_next(node)
    
    def add_range(self,fromStart,toStart,length):
        fromEnd=fromStart+length-1
        diff=toStart-fromStart
        self.ranges+=[Range(fromStart,fromEnd,diff)]

    def order_all(self):
        self.ranges.sort(key=lambda x: x.start)
        if self.next is not None:
            self.next.order_all()
        
    def convert(self,start,end):
        converted=[]
        toConvert=[(start,end)]
        while toConvert!=[]:
            s,e=toConvert.pop(0)
            indStart=bisect_left(self.ranges,s,key=lambda x:x.end)
            if indStart>=len(self.ranges):
                converted+=[(s+0,e+0)]
            else:
                r=self.ranges[indStart]
                if r.contains(s):
                    convDone,convTodo=r.convert(s,e)
                elif r.contains(e):
                    convDone=[(s+0,r.start-1+0)]
                    convTodo=[(r.start,e)]
                else:
                    convDone=[(s+0,e+0)]
                    convTodo=[]
                converted+=convDone
                toConvert+=convTodo
        return converted




class Almanac:
    def __init__(self,initialSeeds):
        self.initialSeeds=initialSeeds
        self.head=None

    def add_conversion(self,conversion):
        if self.head is None:
            self.head=conversion
        else:
            self.head.add_next(conversion)

    def convert(self):
        curr=self.head
        values=self.initialSeeds
        while True:
            if curr is None:
                break
            valuesCopy=values[:]
            values=[]
            for seedStart,seedEnd in valuesCopy:
                values+=curr.convert(seedStart,seedEnd)
            curr=curr.next
        return values
    
    def order_all(self):
        self.head.order_all()

start=perf_counter_ns()
file=open("../input.txt")
input=file.read()
file.close()
almanac=None
conversion=None

for line in input.splitlines():
    if line=="":
        continue
    if almanac is None:
        seedInfo=line.split(":")[1]
        seedInfoList=[int(seed) for seed in seedInfo.lstrip(" ").split(" ")]
        initialSeeds=[]
        for i in range(0,len(seedInfoList),2):
            initialSeeds+=[(seedInfoList[i],seedInfoList[i]+seedInfoList[i+1]-1)]
        almanac=Almanac(initialSeeds)
        continue

    if line.endswith(":"):
        if conversion is not None:
            almanac.add_conversion(conversion)
        conversion=ConversionNode()
    else:
        dstStart,srcStart,length=parse("{} {} {}",line)
        dstStart=int(dstStart)
        srcStart=int(srcStart)
        length=int(length)
        conversion.add_range(srcStart,dstStart,length)
    
almanac.add_conversion(conversion)
middle=perf_counter_ns()
almanac.order_all()

fields=almanac.convert()
minField=min([f[0] for f in fields])
end=perf_counter_ns()
print(minField)
print("total time: ",end-start)
print("importing time: ",middle-start)
print("converting time (no read input): ",end-middle)