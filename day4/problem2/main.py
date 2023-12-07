file=open("../input.txt")
input=file.read()
file.close()
num_cards=len(input.splitlines())

class Card:
    def __init__(self,copies=1):
        self.winNums={}
        self.haveNums={}
        self.copies=copies

    def add_copies(self,amount=1):
        self.copies+=amount

    def add_nums(self,numsInfo):
        winInfo,haveInfo=numsInfo.split("|")
        self.winNums={int(number) for number in winInfo.split(" ") if number.isdigit()}
        self.haveNums={int(number) for number in haveInfo.split(" ") if number.isdigit()}

    def get_points(self):
        return len(self.haveNums.intersection(self.winNums))

cards={num:Card() for num in range(1,num_cards+1)}

for line in input.splitlines():
    cardInfo,numsInfo=line.split(":")
    cardNum=int(cardInfo.split(" ")[-1])

    if cardNum < num_cards:
        cards[cardNum].add_nums(numsInfo)
        points=cards[cardNum].get_points()
        copies=cards[cardNum].copies

        for num in range(cardNum+1,cardNum+1+points):
            if num not in cards:
                break
            cards[num].add_copies(copies)

print(sum([c.copies for c in cards.values()]))