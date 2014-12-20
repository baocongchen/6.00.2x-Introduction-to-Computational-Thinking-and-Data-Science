import pylab, random
class SimpleVirus(object):
 
    def __init__(self, maxBirthProb, clearProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
 
    def getMaxBirthProb(self):
        return self.maxBirthProb
 
    def getClearProb(self):
        return self.clearProb
 
    def doesClear(self):
        return random.random() <= self.getClearProb()
    
    def reproduce(self, popDensity):
        if random.random() <= self.getMaxBirthProb() * (1 - popDensity):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        
 
 
class Patient(object):
    
    def __init__(self, viruses, maxPop):
        self.viruses = viruses
        self.maxPop = maxPop
 
    def getViruses(self):
        return self.viruses
 
    def getMaxPop(self):
        return self.maxPop
 
    def getTotalPop(self):
        return len(self.viruses)
 
    def update(self):
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        popDensity = len(self.viruses) / float(self.maxPop)
        for v in self.viruses[:]:
            self.viruses.append(v.reproduce(popDensity))
        return len(self.viruses)

# Enter your definition for simulationWithoutDrug in this box
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    steps = 300
    trialResults = [[] for s in range(steps)]
    for __ in range(numTrials):
        viruses = [SimpleVirus(maxBirthProb, clearProb) for v in range(numViruses)]
        patient = Patient(viruses, maxPop)
        for step in range(steps):
            trialResults[step].append(patient.update())
    resultsSummary = [sum(l) / float(numTrials) for l in trialResults]
    pylab.plot(resultsSummary, label="Total Virus Population")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend()
    pylab.show()
    

# Enter your definitions for the ResistantVirus and TreatedPatient classes in this box.
class ResistantVirus(SimpleVirus):  
 
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.mutProb = mutProb
        self.resistances = resistances
 
    def isResistantTo(self, drug):
        return self.resistances.get(drug, False)
 
    def reproduce(self, popDensity, activeDrugs):
        if (all(self.isResistantTo(d) for d in activeDrugs) and
            random.random() <= self.getMaxBirthProb() * (1 - popDensity)):
            resistances = {k:v if random.random() > self.mutProb else not v
                           for k, v in self.resistances.items()}
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), 
                                  resistances, self.mutProb)
   
class TreatedPatient(Patient):
    
    def __init__(self, viruses, maxPop):
        Patient.__init__(self, viruses, maxPop)
        self.drugs =[]
 
    def addPrescription(self, newDrug):
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)
 
    def getPrescriptions(self):
        return self.drugs
 
    def getResistPop(self, drugResist):
        return len([v for v in self.viruses if all(v.isResistantTo(d) 
                                                   for d in drugResist)])
 
    def update(self):
        self.viruses = [v for v in self.viruses if not v.doesClear()]
        popDensity = len(self.viruses) / float(self.maxPop)
        for v in self.viruses[:]:
        
            self.viruses.append(v.reproduce(popDensity,
                                                self.getPrescriptions()))
        return len(self.viruses)
        
# Enter your definition for simulationWithDrug in this box
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    steps = 300
    treatOnStep = 150
    trialResultsTot = [[] for s in range(steps)]
    trialResultsRes = [[] for s in range(steps)]
    for __ in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb, clearProb, 
                                  resistances.copy(), mutProb)
                   for v in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        for step in range(steps):
            if step == treatOnStep:
                patient.addPrescription("guttagonol")
            patient.update()
            trialResultsTot[step].append(patient.getTotalPop())
            trialResultsRes[step].append(patient.getResistPop(["guttagonol"]))
    resultsSummaryTot = [sum(l) / float(len(l)) for l in trialResultsTot]
    resultsSummaryRes = [sum(l) / float(len(l)) for l in trialResultsRes]
    pylab.plot(resultsSummaryTot, label="Total Virus Population")
    pylab.plot(resultsSummaryRes, label="Resistant Virus Population")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend()
    pylab.show()
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False},
                       0.005, numTrials=5)