from parse import parse
import functools

class Reveal:
    def __init__(self,cubes):
        self.cubes=cubes
    
    @staticmethod
    def parse(reveal):
        cubes=dict()
        for cubeInfo in reveal.split(","):
            amount,color=parse("{} {}",cubeInfo.lstrip())
            amount=int(amount)
            if color not in cubes:
                cubes[color]=0
            cubes[color]+=amount
        return Reveal(cubes)
    
    def isValid(self,validationMap):
        if len([(k,v) for k,v in self.cubes.items() if k not in validationMap or v>validationMap[k]])>0:
            return False
        return True
    
    def __str__(self):
        return str(self.cubes)



class Game:
    def __init__(self,id_,reveals):
        self.id_=id_
        self.reveals=reveals

    @staticmethod
    def parse(line):
        gameId,revealInfo=line.split(":")
        id_=int(parse("Game {}",gameId)[0])
        
        reveals=[]
        for reveal in revealInfo.split(";"):
            reveals.append(Reveal.parse(reveal))

        return Game(id_,reveals)
    
    def isValid(self,validationMap):
        return all([reveal.isvalid(validationMap) for reveal in self.reveals])

    def minimumCubes(self):
        mCubes=dict()
        for reveal in self.reveals:
            for color,amount in reveal.cubes.items():
                if color not in mCubes or amount>mCubes[color]:
                    mCubes[color]=amount
        return mCubes

    def __str__(self):
        s="{Game: "+str(self.id_)+", reveals: ["
        for reveal in self.reveals:
            s+=str(reveal)+", "
        return s[:-2]+"]}"
    
file=open("../input1.txt")
input=file.read()
file.close()
games=[]

for line in input.splitlines():
    games.append(Game.parse(line))

total=0
for game in games:
    mCubes=list(game.minimumCubes().values())
    total+=functools.reduce(lambda a,b: a*b,mCubes)

print(total)