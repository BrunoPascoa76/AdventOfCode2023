from parse import parse

class ConversionMap:
    def __init__(self,src,dst):
        self.src=src
        self.dst=dst
        self.ranges=dict()

    def addRange(self,line):
        dstStart,srcStart,length=parse("{} {} {}",line)
        dstStart=int(dstStart)
        srcStart=int(srcStart)
        length=int(length)

        self.ranges[srcStart,srcStart+length-1]=dstStart

    def convert(self,value):
        for (srcStart,srcEnd),dstStart in self.ranges.items():
            if srcStart<=value<=srcEnd:
                return dstStart+(value-srcStart)
        return value
    
    def get_ranges(self,src1,src2): #maps a src range into a dst range (for flattening)
        if src1>src2:
            return dict()
        elif src1==src2:
            return {(src1,src1):(src1,src1)}
            
        src1End=[end for start,end in self.ranges if start<=src1<=end]
        if src1End==[]: #src1 is mapped so get the first range that is
            in_between=[start for start,end in self.ranges if src1<start and end<src2]
            if in_between==[]: #there's nothing in between
                return {(src1,src2):(src1,src2)}
            else:
                src1End=min(in_between)-1 #the range of unmapped
        else:
            src1End=min((src1End[0],src2))

        return {(src1,src1End):(self.convert(src1),self.convert(src1End))}.update(self.get_ranges(src1End+1,src2))





class Almanac:
    def __init__(self,initialSeeds):
        self.conversions=dict()
        self.initialSeeds=initialSeeds

    def addConversion(self,conversion):
        src=conversion.src
        dst=conversion.dst
        if src not in self.conversions:
            self.conversions[src]=dict()
        self.conversions[src][dst]=conversion

    def convert(self,srcValue,srcType,dstType):
        if srcType not in self.conversions:
            return None
        localConversions=self.conversions[srcType]

        if dstType in localConversions:
            return localConversions[dstType].convert(srcValue)

        for t,c in localConversions.items(): #basically recursive DFS
            result=self.convert(c.convert(srcValue),t,dstType)
            if result is not None:
                return result
        return None 

    def getSmallestDst(self):
        ranges=[]
        srcConverter="seed"
        dstConverter="soil"
        for seedStart,seedEnd in self.initialSeeds:



           

            

file=open("../input.txt")
input=file.read()
file.close()
almanac=None
conversionMap=None

for line in input.splitlines():
    if line=="":
        continue
    if almanac is None:
        seedInfo=line.split(":")[1]
        seedInfo=seedInfo.lstrip(" ").split(" ")
        initialSeeds=[]
        for i in range(0,len(seedInfo),2):
            seedStart=int(seedInfo[i])
            seedEnd=seedStart+int(seedInfo[i+1])-1
            initialSeeds+=[(seedStart,seedEnd)]
        almanac=Almanac(initialSeeds)
        continue

    if line.endswith(":"):
        if conversionMap is not None:
            almanac.addConversion(conversionMap)
        src,dst=parse("{}-to-{} map:",line)
        conversionMap=ConversionMap(src,dst)
    else:
        conversionMap.addRange(line)
if conversionMap is not None:
    almanac.addConversion(conversionMap)
    
print(almanac.getSmallestDst("location"))