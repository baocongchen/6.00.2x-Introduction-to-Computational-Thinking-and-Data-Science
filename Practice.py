import random, pylab, math
from pylab import figure

class Location(object):
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y
        
    def move(self, deltaX, deltaY):
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def distFrom(self, other):
        ox = other.x
        oy = other.y
        xDist = self.x - ox
        yDist = self.y - oy
        return (xDist**2 + yDist**2)**0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

class Field(object):
    def __init__(self):
        self.drunks = {}
        
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc
            
    def moveDrunk(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep()
        currentLocation = self.drunks[drunk]
        #use move method of Location to get new location
        self.drunks[drunk] = currentLocation.move(xDist, yDist)
        
    def getLoc(self, drunk):
        if not drunk in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]


class Drunk(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'This drunk is named ' + self.name
 

def walkVector(f, d, numSteps):
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return(f.getLoc(d).getX() - start.getX(),
           f.getLoc(d).getY() - start.getY())

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0, 1.0), (0.0, -1.0), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

class ColdDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
            [(0.0,0.9), (0.0,-1.03), (1.03, 0.0), (-1.03, 0.0)]
        return random.choice(stepChoices)

class EDrunk(Drunk):
    def takeStep(self):
        ang = 2 * math.pi * random.random()
        length = 0.5 + 0.5 * random.random()
        return length * math.sin(ang), length * math.cos(ang)

class PhotoDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.0, 0.5),(0.0, -0.5),
                     (1.5, 0.0),(-1.5, 0.0)]
        return random.choice(stepChoices)

class DDrunk(Drunk):
    def takeStep(self):
        stepChoices =\
                    [(0.85, 0.85), (-0.85, -0.85),
                     (-0.56, 0.56), (0.56, -0.56)] 
        return random.choice(stepChoices)

def mairymCarlo(numTrials, d):
    distances = []
    field = Field()
    origin = Location(0, 0)
    drunk = d('burp')
    field.addDrunk(drunk,origin)
    for trial in range(numTrials):
        distances.append(walkVector(field, drunk, 1000))
    return distances
 
def genPlot(array, drunk):
    x = []
    y = []
    for i in array:
        x.append(i[0])
        y.append(i[1])
    pylab.title(drunk)
    pylab.xlim(xmin=-100, xmax=100)
    pylab.ylim(ymin=-100, ymax=100)
    pylab.plot(x, y, 'ro')
    pylab.grid(True)
    pylab.show()

for drunk in (UsualDrunk, ColdDrunk, EDrunk, PhotoDrunk, DDrunk):
    genPlot(mairymCarlo(500, drunk), drunk)
########
def sampleQuizzes():
    scores = []
    for i in range(10000):
        firstMidterm = random.randint(50, 80)
        secondMidterm = random.randint(60, 90)
        finalExam = random.randint(55, 95)
        total = (firstMidterm + secondMidterm)/4.0 + finalExam/2.0
        if 70 <= total <= 75:
            scores.append(total)
    return len(scores)/10000.0
#######
def plotQuizzes():
    scores = generateScores(10000)
    pylab.hist(scores, bins=7)
    pylab.xlabel("Final Score")
    pylab.ylabel("Number of Trials")
    pylab.title("Distribution of Scores")
    pylab.show()
#######
def probTest(limit):
    prob = 1
    rolls = 1
    while prob/6.0 > limit:
        prob *= 5/6.0
        rolls += 1
    return rolls

########
histogram = [ 0 for i in range(1,1001)]  # intialize the list to be all zeros
balls = ["white" for w in range(500)]
black = ["black" for b in range(500)]
balls.extend(black)
for trials in range(1000):
    number = 1
    while number < 1000:
        result = random.sample(balls,1)
        if result == ["white"]:
            histogram[number] += 1
            break
        else:
            number += 1