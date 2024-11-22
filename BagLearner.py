""""""
"""  		  	   		 	   		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		 	   		  		  		    	 		 		   		 		  

Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 	   		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 	   		  		  		    	 		 		   		 		  

Template code for CS 4646/7646  		  	   		 	   		  		  		    	 		 		   		 		  

Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 	   		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 	   		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 	   		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   		  		  		    	 		 		   		 		  
or edited.  		  	   		 	   		  		  		    	 		 		   		 		  

We do grant permission to share solutions privately with non-students such  		  	   		 	   		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 	   		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 	   		  		  		    	 		 		   		 		  

-----do not edit anything above this line---  		  	   		 	   		  		  		    	 		 		   		 		  
"""

import numpy as np
from scipy.stats import mode


class BagLearner(object):
    """
    This is a Bootstrap Aggregation Learner (BagLearner).

    :param learner: Points to any arbitrary learner class that will be used in the BagLearner.
    :type learner: learner
    :param kwargs: Keyword arguments that are passed on to the learner's constructor and they can vary according to the learner
    :param bags: The number of learners you should train using Bootstrap Aggregation.
    :type bags: int
    :param boost: If boost is true, then you should implement boosting (optional implementation)
    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """
    def __init__(self, learner, kwargs, bags, boost=False, verbose=False):
        """
        Constructor method
        """
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learner_type = "BagLearner"

        self.learners = []
        for i in range(bags):
            self.learners.append(self.learner(**kwargs))


    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "cvasquez36"


    def study_group(self):
        """
        :return: A comma separated string of GT_Name of each member of your study group
        :rtype: str
        """
        return "cvasquez36, ewu96, hwang759, kliu353, mma320, mmannerow3, steng31, qliang61"


    def get_learner_type(self):
        """
        :return: The type of learner (DT Learner)
        :rtype: str
        """
        return self.learner_type


    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        rows_in_data = data_x.shape[0]
        rows_per_bag = int(0.6 * rows_in_data)
        for l in self.learners:
            bag_data_indices = np.random.choice(rows_in_data, rows_per_bag, replace=True)
            bag_data_x, bag_data_y = data_x[bag_data_indices], data_y[bag_data_indices]
            l.add_evidence(bag_data_x, bag_data_y)


    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        predictions = np.array([learner.query(points) for learner in self.learners])
        return mode(predictions, axis=0).mode[0]
        # return np.mean(predictions, axis=0)


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
