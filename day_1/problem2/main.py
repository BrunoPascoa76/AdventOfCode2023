f=open("../input.txt","r")
text=f.read() 

sum=0
numbers={"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}
for line in text.splitlines():
    nums=[]
    buffer=""
    for char in line:
        if char.isdigit():
            nums.append(char)
            buffer=""
        else:
            buffer+=char
        if len(buffer)>5:
            buffer=buffer[1:]  
        longNumbers=[v for k,v in numbers.items() if k in buffer]
        if longNumbers!=[]:
            nums+=longNumbers
            buffer=char #oneight

    if nums!=[]:
        sum+=int(nums[0]+nums[-1])

f.close()
print(sum)