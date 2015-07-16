from vectorize import *

#forward algorithm done
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

#backward algorithm still done
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
            return 1
        acc = 0
        for i in range(maxStates):
            acc += self.backward(timestep + 1, i) *\
            transitionMatrix[stateIndex, i] * obser(stateIndex,\
            self.observe[timestep])
        self.backwardDP[stateIndex, timestep] = acc
        return acc

#skipping Viterbi for now because there is only one probable state sequence
#given how we optimized the model. If Baum Welch changes parameters, then
#we'll code Viterbi

#Baum-Welch!
class baumWelch:
    def __init__(self, obsSequence):
        observe = obsSequence
        #initializing a class for the forward algorithm on the obs sequence
        fwdAlgo = forward(observe)
        #initializing a class for the backward algorithm on the obs sequence
        bckAlgo = backward(observe)
        probObserve = 0
        #timestepCalc could actually be any state. I chose the middle state
        #since 2 * (n/2)^2 is optimal runtime.
        timestepCalc = len(observe) / 2
        #the following loop computes probObserve, which is formally
        #Pr(O|lambda). The probability of the observation sequence given
        #the parameters of the HMM
        for i in range(maxStates):
            probObserve += self.fwdAlgo.forward(timestepCalc, i) *\
                           self.bckAlgo.backward(timestepCalc, i)
    #the following function computes the probability of being at
    #state1 at timestep t and state2 at timestep t+1 given
    #the HMM parameters and observation sequence
    def computeStateTrans(self, timestep, state1, state2):
        return (self.fwdAlgo.forward(timestep, state1) *\
        transitionMatrix[state1,state2] * self.bckAlgo.backward\
        (timestep+1, state2) * obser(state2, self.observe[timestep])) /\
        probObserve
    #the following function computes the probability of being in
    #state i at time t given the observation sequence and HMM
    #parameters.
    def computeStateProb(self, timestep, stateIndex):
        return (self.fwdAlgo.forward(timestep, stateIndex) *\
        self.bckAlgo.backward(timestep, stateIndex)) / probObserve

#this performs a single iteration of the baum welch algorithm.
#the reason I am not performing all iterations in one function is
#the necessity to start a new class for each iteration since all the
#parameters are changed and forwardDP and backwardDP assume
#the old parameters unless they are reinitialized.
#the implementation below is incomplete because it lacks the step
#that updates the observation matrix. That will be done once we figure
#out a better way to represent that data and iterate through it systematically
def baumwelchupdate(obsSequence):
    bwl = baumWelch(obsSequence)
    for i in range(maxStates):
        initialProb[i] = bwl.computeStateProb(0, i)
    for i in range(maxStates):
        expectedArrivals = 0
        for j in range(len(obsSequence) - 1):
            expectedArrivals += bwl.computeStateProb(j, i)
        for j in range(maxStates):
            expectedTrans = 0
            for k in range(len(obsSequence) - 1):
                expectedTrans += bwl.computeStateTrans(k, i, j)
            transitionMatrix[i, j] = expectedTrans / expectedArrivals
    normalize_matrix(transitionMatrix)

#the Baum Welch algorithm implemented with iterations. numIter allows
#the user to specify the number of iterations they wish to make the
#algorithm go through
def baumWelchAlgo(obsSequence, numIter):
    for i in range(numIter):
        baumwelchupdate(obsSequence)
