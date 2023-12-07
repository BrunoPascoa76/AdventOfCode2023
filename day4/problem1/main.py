file=open("../input.txt")
input=file.read()
file.close()

total=0
for card in input.splitlines():
    cardInfo,numsInfo=card.split(":")
    cardNum=cardInfo.split(" ")[-1]

    winInfo,haveInfo=numsInfo.split("|")
    winNums={int(number) for number in winInfo.split(" ") if number.isdigit()}
    haveNums={int(number) for number in haveInfo.split(" ") if number.isdigit()}

    numMatches=len(haveNums.intersection(winNums))

    if numMatches>0:
        total+=2**(numMatches-1)

print(total)