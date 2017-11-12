from sklearn.datasets import make_classification, make_regression
import numpy as np

n_samples_factor = 1000000
for intensity in range(1,6):
	X,Y,= make_classification(n_samples=n_samples_factor, 
	            n_features=10+(intensity), n_informative=5+(intensity), 
	            n_repeated=0, n_classes=5)

	np.savetxt(fname='clf_{}_X.gz'.format(intensity),X=X)
	np.savetxt(fname='clf_{}_Y.gz'.format(intensity),X=Y)

	# x = np.loadtxt(fname='clf_{}_X.gz'.format(intensity))
	# y = np.loadtxt(fname='clf_{}_Y.gz'.format(intensity))
	
for intensity in range(1,6):
	X,Y,= make_regression(n_samples=n_samples_factor, n_features=10+(intensity), n_informative=5+intensity,
		n_targets=1, bias=0.0, effective_rank=None, tail_strength=0.5, noise=0.01, shuffle=True, coef=False,
		random_state=None)
		
	np.savetxt(fname='reg_{}_X.gz'.format(intensity),X=X)
	np.savetxt(fname='reg_{}_Y.gz'.format(intensity),X=Y)