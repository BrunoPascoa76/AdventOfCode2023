schematic=[]

def isPartNumber(row1,col1,row2,col2):
    for r in range(row1-1,row2+2):
        for c in range(col1-1,col2+2):
            if (r,c) in symbols:
                return True
    return False

class Number:
    def __init__(self,digit,row,col):
        self.coordinates=[(row,col)]
        self.buffer=digit
        self.value=-1

    def fillBuffer(self,digit,row,col):
        self.buffer+=digit
        self.coordinates+=[(row,col)]

    def flushBuffer(self):
        self.value=int(self.buffer)
    
    def adjacentTo(self,r,c):
        cStart=self.coordinates[0]
        cEnd=self.coordinates[-1]
        if r not in range(cStart[0]-1,cEnd[0]+2) or c not in range(cStart[1]-1,cEnd[1]+2):
            return False
        return True
    
file=open("../input.txt")
input=file.read()
file.close()
row=0
col=0
numbers=[]
stars=[]
total=0

def addChar(char,row,col):
    global numbers
    if numbers==[] or numbers[-1].value!=-1:
        numbers+=[Number(char,row,col)]
    else:
        numbers[-1].fillBuffer(char,row,col)


for line in input.splitlines():
    col=0
    schematic+=[[]]
    for char in line:
        schematic[row]+=[char]
        
        if char.isdigit():
            addChar(char,row,col)
        else:
            if len(numbers)>0:
                numbers[-1].flushBuffer()
            if char=="*":
                stars+=[(row,col)]
        col+=1
    row+=1

for row,col in stars:
    adjNumbers=[number for number in numbers if number.adjacentTo(row,col)]
    if len(adjNumbers)==2:
        total+=adjNumbers[0].value*adjNumbers[1].value

print(total)




