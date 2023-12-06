def isPartNumber(row1,col1,row2,col2):
    for r in range(row1-1,row2+2):
        for c in range(col1-1,col2+2):
            if (r,c) in symbols:
                return True
    return False



file=open("../input.txt")
input=file.read()
file.close()
row=0
col=0
numbers=dict()
symbols=dict()
total=0

buffer=""
for line in input.splitlines():
    col=0
    for char in line:
        if buffer=="":
            startRow=row
            startCol=col
        
        if char.isdigit():
            buffer+=char
        else:
            if buffer!="":
                numbers[startRow,startCol,row,col-1]=int(buffer)
                buffer=""
            if char!=".":
                symbols[row,col]=char
        col+=1
    if buffer!="":
        numbers[startRow,startCol,row,col]=int(buffer)
        buffer=""
    row+=1

for (r1,c1,r2,c2),number in numbers.items():
    if isPartNumber(r1,c1,r2,c2):
        total+=number
print(numbers)
print(total)
