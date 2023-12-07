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
    
    def getSmallestDst(self,dstType):
        return min([self.convert(seed,"seed",dstType) for seed in self.initialSeeds])

            

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
        initialSeeds=[int(seed) for seed in seedInfo.lstrip(" ").split(" ")]
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