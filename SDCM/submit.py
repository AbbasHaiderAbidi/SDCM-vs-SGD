import numpy as np
import random as rnd
import time as tm

# You may define any new functions, variables, classes here
# For example, functions to calculate next coordinate or step length


def getRandpermCoord( currentCoord,  randperm, randpermInner, y):
	
	if randpermInner >= y.size-1 or randpermInner < 0 or currentCoord < 0:
		randpermInner = 0
		randperm = np.random.permutation( y.size )
		return ( randperm, randpermInner )
	else:
		randpermInner = randpermInner + 1
		return ( randperm, randpermInner )


def doSDCM(alpha, theta, X, y, C, randperm,randpermInner, i, normSq):   
	w = theta[0:-1]
	b = theta[-1]
	(randperm, randpermInner ) = getRandpermCoord( i, randperm, randpermInner , y)
	i=randperm[randpermInner]
	x = X[i,:]
	newAlphai =  alpha[i] + (1 - y[i] * (x.dot(w) + b)) / (normSq[i] - (1/(2*C)))
	if newAlphai < 0 :
		newAlphai = 0
	w = w + (newAlphai - alpha[i]) * y[i] * x
	b = b + (newAlphai - alpha[i]) * y[i]
	alpha[i] = newAlphai        
	return (np.append( w, b ), i,  randperm, randpermInner, alpha )



################################
# Non Editable Region Starting #
################################
def solver( X, y, C, timeout, spacing ):
	(n, d) = X.shape
	t = 0
	totTime = 0
	randperm = np.random.permutation( y.size )
	randpermInner = -1
	# w is the normal vector and b is the bias
	# These are the variables that will get returned once timeout happens
	w = np.zeros( (d,) )
	b = 0
	tic = tm.perf_counter()
################################
#  Non Editable Region Ending  #
################################
	
	alpha = np.ones((y.size ,))/512
	# alpha = np.random.randint(2,size=(y.size,))
	alphay = np.multiply( alpha, y )
	w = X.T.dot( alphay )
	b = alpha.dot( y )
	theta_SDCM=np.append(w,b)
	normSq = np.square( np.linalg.norm( X, axis = 1 ) ) + 1
	i = -1
	cumulative_w=w
	cumulative_b=b
	# You may reinitialize w, b to your liking here
	# You may also define new variables here e.g. eta, B etc

################################
# Non Editable Region Starting #
################################
	while True:
		t = t + 1
		if t % spacing == 0:
			toc = tm.perf_counter()
			totTime = totTime + (toc - tic)
			if totTime > timeout:
				return (w, b, totTime)
			else:
				tic = tm.perf_counter()
################################
#  Non Editable Region Ending  #
################################

		(theta_SDCM, i, randperm, randpermInner , alpha)= doSDCM(alpha ,theta_SDCM, X, y, C, randperm,randpermInner, i, normSq)
		
		cumulative_w=cumulative_w + theta_SDCM[0:-1]
		w=cumulative_w/(t+1)

		cumulative_b = cumulative_b + theta_SDCM[-1]
		b=cumulative_b/(t+1)

		# Write all code to perform your method updates here within the infinite while loop
		# The infinite loop will terminate once timeout is reached
		# Do not try to bypass the timer check e.g. by using continue
		# It is very easy for us to detect such bypasses - severe penalties await
		
		# Please note that once timeout is reached, the code will simply return w, b
		# Thus, if you wish to return the average model (as we did for GD), you need to
		# make sure that w, b store the averages at all times
		# One way to do so is to define two new "running" variables w_run and b_run
		# Make all GD updates to w_run and b_run e.g. w_run = w_run - step * delw
		# Then use a running average formula to update w and b
		# w = (w * (t-1) + w_run)/t
		# b = (b * (t-1) + b_run)/t
		# This way, w and b will always store the average and can be returned at any time
		# w, b play the role of the "cumulative" variable in the lecture notebook
		# w_run, b_run play the role of the "theta" variable in the lecture notebook
		
	return (w, b, totTime) # This return statement will never be reached