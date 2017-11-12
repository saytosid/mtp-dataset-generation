
import random
import os
import thread
import sys

class Stresser(object):
    """
    docstring for Stresser
    Interface for all Stresses.
    """

    def __init__(self):
        print("Stresser Initialised")

    def doStress(self, intensity=1):
        # @param intensity - Intensity of stress on a scale of 1-5
        print("I am stressing with intensity {}; kiddin! I dont do anything apart from being a loud mouth !".format(intensity))


class CreateFile(Stresser):
    """Creates big file"""

    def __init__(self):
        super(CreateFile, self).__init__()

    def doStress(self, intensity=1):
        filename = str(random.randint(0, 1024))
        with open(filename, 'wb') as f:
            size_ = random.randint(intensity * 1000000,intensity * 10000000)
            for i in xrange(size_):
                if random.random() < 0.4:
                    f.write(' ')  # Sometimes add a space
                if random.random() < 0.2:
                    f.write('\n')  # Sometimes newline
                f.write(str(i))
        return filename

################# MICRO LOADS ##################################
class WordCount(Stresser):
    """Creates big file and does wc on it"""

    def __init__(self):
        super(WordCount, self).__init__()
        

    def doStress(self, intensity=1):
        '''Stresses the machine'''
        filename= CreateFile().doStress(intensity+1)
        print os.system('wc {}'.format(filename))
        os.system("rm {}".format(filename))

class Sort(Stresser):
    def __init__(self):
        super(Sort, self).__init__()
        
    def doStress(self, intensity=1):
        '''Stresses the machine'''
        filename= CreateFile().doStress(intensity+1)
        print os.system('sort {}'.format(filename))
        os.system("rm {}".format(filename))

class Grep(Stresser):
    def __init__(self):
        super(Grep, self).__init__()
        
    def doStress(self, intensity=1):
        '''Stresses the machine'''
        filename= CreateFile().doStress(intensity+1)
        print os.system('cat {} | grep 1'.format(filename))
        os.system("rm {}".format(filename))

class Concat(Stresser):
    def __init__(self):
        super(Concat, self).__init__()
        
    def doStress(self, intensity=1):
        '''Stresses the machine'''
        filename= CreateFile().doStress(intensity+1)
        print os.system('cat {}'.format(filename))
        os.system("rm {}".format(filename))
#################################################################

############## ML Loads #########################################
from sklearn.datasets import make_classification, make_regression
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.cluster import KMeans

import numpy as np
import pandas
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class ModelMaker(object):
    """docstring for ModelMaker"""
    def __init__(self):
        super(ModelMaker, self).__init__()
    
    def getKerasModel(self,num_layers,input_dim,output_dim):
        model = Sequential()
        model.add(Dense(32, input_dim=input_dim))
        model.add(Activation('relu'))
        for i in xrange(num_layers):
            model.add(Dense(32))
            model.add(Activation('relu'))
        model.add(Dense(output_dim))

        return model
        
model_maker = ModelMaker()

class NaiveBayesClassifier(Stresser):
    def __init__(self):
        super(NaiveBayesClassifier, self).__init__()
        
    def doStress(self, intensity=1):
        '''Stresses the machine'''
        X = np.loadtxt(fname='working_dir/clf_{}_X.gz'.format(intensity))
        Y = np.loadtxt(fname='working_dir/clf_{}_Y.gz'.format(intensity))
        gnb = GaussianNB()
        print gnb.fit(X, Y)

class NNClassifier(Stresser):
    def __init__(self):
        super(NNClassifier, self).__init__()

    def doStress(self, intensity=1):
        '''Stresses the machine'''
        
        X = np.loadtxt(fname='working_dir/clf_{}_X.gz'.format(intensity))
        Y = np.loadtxt(fname='working_dir/clf_{}_Y.gz'.format(intensity))
        nb_classes = 5
        targets = np.array(Y).reshape(-1)
        targets = map(int,targets)
        one_hot_targets = np.eye(nb_classes)[targets]
        Y = one_hot_targets
        clf = model_maker.getKerasModel(num_layers=intensity,input_dim=X.shape[1],output_dim=Y.shape[1])
        clf.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
        clf.fit(X,Y,epochs = intensity+2, verbose=2)

class NNRegressor(Stresser):
    def __init__(self):
        super(NNRegressor, self).__init__()

    def doStress(self, intensity=1):
        '''Stresses the machine'''
        X = np.loadtxt(fname='working_dir/reg_{}_X.gz'.format(intensity))
        Y = np.loadtxt(fname='working_dir/reg_{}_Y.gz'.format(intensity))
        reg = model_maker.getKerasModel(num_layers=intensity,input_dim=X.shape[1],output_dim=1)
        reg.compile(optimizer='rmsprop',
              loss='mse')
        reg.fit(X,Y,epochs = intensity + 2, verbose=2)

class KMeansCluster(Stresser):
    def __init__(self):
        super(KMeansCluster, self).__init__()
        
    def doStress(self, intensity=1):
        '''Stresses the machine'''
        X = np.loadtxt(fname='working_dir/reg_{}_X.gz'.format(intensity))
        Y = np.loadtxt(fname='working_dir/reg_{}_Y.gz'.format(intensity))

        kmeans = KMeans(n_clusters=8*intensity, init='k-means++', n_init=10,
                 max_iter=5*intensity, tol=1e-4, precompute_distances='auto',
                 verbose=1, random_state=None, copy_x=True,
                 n_jobs=intensity, algorithm='auto')
        kmeans.fit(X)


loads = [CreateFile(), WordCount(), Sort(), Grep(), Concat(), NaiveBayesClassifier(), NNClassifier(), NNRegressor(), KMeans()]
num_loads = len(loads)
if __name__ == '__main__':
    loads[6].doStress(1)
    


