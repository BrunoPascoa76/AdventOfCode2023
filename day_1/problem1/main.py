f=open("input.txt","r")
text=f.read()

sum=0
for line in text.splitlines():
    nums=[]
    for char in line:
        if char.isdigit():
            nums.append(char)
    if nums!=[]:
        sum+=int(nums[0]+nums[-1])

f.close()
print(sum)