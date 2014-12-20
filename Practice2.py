import random, pylab, numpy
#import pylab
#
##Session 1
#
#def possible_mean(L):
#    return sum(L)/len(L)
#
#def possible_variance(L):
#    mu = possible_mean(L)
#    temp = 0
#    for array in arrays:
#        print possible_variance(array) 
#
#    for e in L:
#        temp += (e-mu)**2
#    return temp / len(L)
#arrays = [0,1,2,3,4,5,6,7,8],[5,10,10,10,15],[0,1,2,4,6,8],[6,7,11,12,13,15],[9,0,0,3,3,3,6,6]
#

#Session 2

# Global Variables
MAXRABBITPOP = 1000
CURRENTRABBITPOP = 500
CURRENTFOXPOP = 30

def rabbitGrowth():
    """ 
    rabbitGrowth is called once at the beginning of each time step.

    It makes use of the global variables: CURRENTRABBITPOP and MAXRABBITPOP.

    The global variable CURRENTRABBITPOP is modified by this procedure.

    For each rabbit, based on the probabilities in the problem set write-up, 
      a new rabbit may be born.
    Nothing is returned.
    """
    # you need this line for modifying global variables
    global CURRENTRABBITPOP
    rabbitBirthProb = 1.0 - CURRENTRABBITPOP/float(MAXRABBITPOP)
    tempPop = CURRENTRABBITPOP
    for rabbit in range(CURRENTRABBITPOP):
        if random.random() <= rabbitBirthProb:
            if  tempPop < MAXRABBITPOP:
                tempPop += 1
    CURRENTRABBITPOP = tempPop            
def foxGrowth():
    """ 
    foxGrowth is called once at the end of each time step.

    It makes use of the global variables: CURRENTFOXPOP and CURRENTRABBITPOP,
        and both may be modified by this procedure.

    Each fox, based on the probabilities in the problem statement, may eat 
      one rabbit (but only if there are more than 10 rabbits).

    If it eats a rabbit, then with a 1/3 prob it gives birth to a new fox.

    If it does not eat a rabbit, then with a 1/10 prob it dies.

    Nothing is returned.
    """
    # you need these lines for modifying global variables
    global CURRENTRABBITPOP, MAXRABBITPOP
    global CURRENTFOXPOP
    tempRabbitPop = CURRENTRABBITPOP
    tempFoxPop = CURRENTFOXPOP
    eatRabbitProb = CURRENTRABBITPOP/float(MAXRABBITPOP)
    for fox in range(CURRENTFOXPOP):
        if tempRabbitPop > 10:
            if random.random() <= eatRabbitProb:
                tempRabbitPop -= 1 
                if random.random() <= 1/3.0:
                    tempFoxPop += 1
            else:
                if random.random() <= 0.9:
                    if tempFoxPop > 10:
                        tempFoxPop -= 1
    CURRENTRABBITPOP = tempRabbitPop
    CURRENTFOXPOP = tempFoxPop
def runSimulation(numSteps):
    """
    Runs the simulation for `numSteps` time steps.

    Returns a tuple of two lists: (rabbit_populations, fox_populations)
      where rabbit_populations is a record of the rabbit population at the 
      END of each time step, and fox_populations is a record of the fox population
      at the END of each time step.

    Both lists should be `numSteps` items long.
    """
    rabbit_populations = []
    fox_populations = []
    for i in range(numSteps):
        rabbitGrowth()
        rabbit_populations.append(CURRENTRABBITPOP)
        foxGrowth()
        fox_populations.append(CURRENTFOXPOP)
    return (rabbit_populations,fox_populations)
(rabbit_populations,fox_populations) = runSimulation(200)

coeff = numpy.polyfit(range(len(fox_populations)), fox_populations, 2)
pylab.plot(numpy.polyval(coeff, range(len(fox_populations))))
pylab.plot(range(200), rabbit_populations, range(200), fox_populations)
pylab.show()