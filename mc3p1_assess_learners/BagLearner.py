"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np
import math

class BagLearner(object):
    def __init__(self,learner = rt.RTLearner, kwargs = {"leaf_size":1}, bags = 20, boost = False, verbose = False):
        self.boost = boost
        self.verbose =verbose
        self.learners=[]
        if learner==rt.RTLearner:
                self.learners = [learner(**kwargs) for i in range(bags) ]
        else:
                self.learners = [learner for i in range(bags) ]

    def addEvidence(self,dataX,dataY):
        for learner in self.learners:
            new_dataX=[]
            new_dataY=[]
            for i in range(len(dataY)):
                selected_row = np.random.randint(len(dataY))
                new_dataX.append(dataX[selected_row,:])
                new_dataY.append(dataY[selected_row])
            new_dataX = np.asarray(new_dataX)
            new_dataY = np.asarray(new_dataY)
            learner.addEvidence(new_dataX, new_dataY)
    def query(self,points):
            predicts = [learner.query(points) for learner in self.learners]
            print len(np.mean(predicts,axis=0))
            return np.mean(predicts,axis=0)

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
