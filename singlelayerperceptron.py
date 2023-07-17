import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import time

cons = 1
class_1_mean = [20,20,20]
class_1_cov = [[cons,0,0],[0,cons,0],[0,0,cons]]
class_2_mean = [10,10,10]
class_2_cov = [[cons,0,0],[0,cons,0],[0,0,cons]]
class_3_mean = [1,1,1]
class_3_cov = [[cons,0,0],[0,cons,0],[0,0,cons]]

 
n1 = 100; n2 = 100;n3 = 100; 
ones = [np.ones(n1)]
cl_1 = np.random.multivariate_normal(class_1_mean,class_1_cov,n1).T
cl_2 = np.random.multivariate_normal(class_2_mean,class_2_cov,n2).T
cl_3 = np.random.multivariate_normal(class_3_mean,class_3_cov,n3).T

c1 = (np.concatenate((ones, cl_1), axis=0)).transpose()
c2 = (np.concatenate((ones, cl_2), axis=0)).transpose()
c3 = (np.concatenate((ones, cl_3), axis=0)).transpose()
total = 0
alpha = 0.01 #learning rate
param1 = [0,0.1,0.1,0.1]
param2 = [0,0.1,0.1,0.1]
flag = 1
i1 = 0; i2 = 0; i3 = 0;
iterations = 0;
while(total <n1+n2+n3 and iterations <1000000):
	iterations = iterations + 1
	if flag == 1 :
		temp1 = np.dot(c1[i1], param1)
		temp2 = np.dot(c1[i1], param2)
		if temp1<0 and temp2<0 :
			param1 = np.add(param1, alpha*c1[i1])
			param2 = np.add(param2, alpha*c1[i1])
			total = 0
		elif temp1>=0 and temp2<0 :
			param2 = np.add(param2, alpha*c1[i1])
			total = 0
		elif temp1<0 and temp2>=0 :
			param1 = np.add(param1, alpha*c1[i1])
			total = 0
		else :
			total = total + 1;
		flag = 2;
		i1 = (i1+1)%n1
	elif flag == 2 :
		temp1 = np.dot(c2[i2], param1)
		temp2 = np.dot(c2[i2], param2)
		if temp1<0 and temp2>=0 :
			param1 = np.add(param1, alpha*c2[i2])
			param2 = np.add(param2, -1*alpha*c2[i2])
			total = 0
		elif temp1>=0 and temp2>=0 :
			param2 = np.add(param2, -1*alpha*c2[i2])
			total = 0
		elif temp1<0 and temp2<0 :
			param1 = np.add(param1, alpha*c2[i2])
			total = 0
		else :
			total = total + 1;
		flag = 3;
		i2 = (i2+1)%n2
	elif flag == 3 :
		temp1 = np.dot(c3[i3], param1)
		temp2 = np.dot(c3[i3], param2)
		if temp1>=0 and temp2<0 :
			param1 = np.add(param1, -1*alpha*c3[i3])
			#param2 = np.add(param2, alpha*c3[i3])
			total = 0
		elif temp1<0 and temp2<0 :
			#param2 = np.add(param2, alpha*c3[i3])
			total = total + 1
		elif temp1>=0 and temp2>=0 :
			param1 = np.add(param1, -1*alpha*c3[i3])
			param2 = np.add(param2, -1*alpha*c3[i3])
			total = 0
		else :
			param2 = np.add(param2, -1*alpha*c3[i3])
			total = 0;
		flag = 1;
		i3 = (i3+1)%n3

#fig = plt.figure()
#ax = fig.add_subplot(111)
#x = np.linspace(-5,5,100)
#y = (-1*param1[1]*x -1*param1[0])/param1[2]
#y1 = (-1*param2[1]*x -1*param2[0])/param2[2]
#ax.plot(x, y, '-r', linewidth=3)
#ax.plot(x, y1, '-g', linewidth=3)
#plt.grid()
#plt.scatter(cl_1[0], cl_1[1], c = 'r', alpha=0.5)
#plt.scatter(cl_2[0], cl_2[1], c = 'b', alpha=0.5)
#plt.scatter(cl_3[0], cl_3[1], c = 'y', alpha=0.5)
#plt.savefig('boundary.png')
print("Number of iterations",iterations)
