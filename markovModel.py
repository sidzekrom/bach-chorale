from vectorize import *

#forward algorithm
class forward:
    def __init__(self, obsSequence):
        forwardDP = np.zeros(shape = (maxStates, len(obsSequence)))
        for i in range(maxStates):
            for j in range(len(obsSequence)):
                forwardDP[i, j] = -1
        observe = obsSequence
    def forward(self, timestep, stateIndex):
        if (self.forwardDP[stateIndex, timestep] != -1):
            return self.forwardDP[stateIndex, timestep]
        if (timestep == 0):
            self.forwardDP[stateIndex, timestep] = initialProb[stateIndex] *\
                    obser(stateIndex, self.observe[timestep])
            return initialProb[stateIndex]
        acc = 0
        for i in range(maxStates):
            acc += self.forward(timestep - 1, i) * transitionMatrix[i,\
                   stateIndex] * obser(stateIndex, self.observe[timestep])
        self.forwardDP[stateIndex, timestep] = acc
        return acc

#backward algorithm still in progress
class backward:
    def __init__(self, obsSequence):
        backwardDP = np.zeros(maxStates, len(obsSequence))
        for i in range(maxStates):
            for j in range(len(obsSequence)):
                backwardDP[i, j] = -1
        observe = obsSequence
    def backward(self, timestep, stateIndex):
        if (self.backwardDP[stateIndex, timestep] != -1):
            return self.backwardDP[stateIndex, timestep]
        if (timestep == len(self.observe)):
            self.backwardDP[stateIndex, timestep] = 1

