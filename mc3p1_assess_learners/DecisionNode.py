

import numpy as np

class DecisionNode():
    def __init__(self, left,right,decision_function,val=None):
        self.left = left
        self.right = right
        self.decision_function = decision_function
        self.val = val
    def decide(self, feature):
        """Return on a label if node is leaf,or pass the decision down to the node's left/right child (depending on decisionfunction)."""
        if self.val is not None:
            return self.val
        elif self.decision_function(feature):
            return self.left.decide(feature)
        else:
            return self.right.decide(feature)


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
