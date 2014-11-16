import random
def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns the a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    yes = 0
    for i in range(numTrials):
        sameColor = 0
        bucket = ["red","red","red","green","green","green"]
        balls = []
        times = 3
        while times > 0:
            choice = random.choice(bucket) 
            if choice in balls:
                sameColor += 1
            balls.append(choice)
            times -= 1
        if sameColor == 2:
            yes += 1
    return yes/float(numTrials)
print noReplacementSimulation(10000)