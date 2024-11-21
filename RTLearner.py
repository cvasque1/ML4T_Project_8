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

class RTLearner(object):
    """
    This is a Random Tree Learner (RTLearner).

    :param leaf_size: Is the maximum number of samples to be aggregated at a leaf.
    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """
    def __init__(self, leaf_size=1, verbose=False):
        """
        Constructor method
        """
        self.decision_tree = None
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.learner_type = "RTLearner"


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
        :return: The type of learner (RT Learner)
        :rtype: str
        """
        return self.learner_type


    def get_leaf_size(self):
        """
        :return: The leaf size
        :rtype: int
        """
        return self.leaf_size


    def determine_best_factor_split(self, data_x):
        return np.random.randint(0, data_x.shape[1])


    def build_tree(self, data_x, data_y):
        """
        Build a Random Tree based on the training data

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        # Base cases: data rows <= leafs size or all y-values are the same
        if data_x.shape[0] <= self.leaf_size or np.all(data_y == data_y[0]):
            return np.array([[-1, np.mean(data_y), np.nan, np.nan]])

        split_factor = self.determine_best_factor_split(data_x)
        split_val = np.median(data_x[:, split_factor])

        # Create a mask that splits data into left and right subtrees based on split value
        left_tree_data_mask = data_x[:, split_factor] <= split_val
        right_tree_data_mask = data_x[:, split_factor] > split_val

        # If all split data is on one side of the split, return a leaf
        if np.all(left_tree_data_mask == False) or np.all(right_tree_data_mask == False):
            return np.array([[-1, np.mean(data_y), np.nan, np.nan]])

        # Build left and right subtrees
        left_tree = self.build_tree(data_x[left_tree_data_mask], data_y[left_tree_data_mask])
        right_tree = self.build_tree(data_x[right_tree_data_mask], data_y[right_tree_data_mask])

        root = np.array([[split_factor, split_val, 1, left_tree.shape[0] + 1]])
        return np.vstack((root, left_tree, right_tree))


    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        self.decision_tree = self.build_tree(data_x, data_y)


    def query_single_point(self, point):
        """
        Estimate a single point given the model we built.

        :param point: A numpy array row corresponding to a specific query.
        :type point: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: float
        """
        node_index = 0
        while True:
            node = self.decision_tree[int(node_index)]
            if node[0] == -1: # Reached a leaf
                return node[1]
            else:
                split_factor = int(node[0])
                split_val = node[1]
                if point[split_factor] <= split_val:
                    node_index += node[2]
                else:
                    node_index += node[3]


    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        return np.array([self.query_single_point(p) for p in points])


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
