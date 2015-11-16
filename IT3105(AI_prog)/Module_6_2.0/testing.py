from scipy import stats
import numpy as np
#np.random.seed(12345678)
#rvs1 = stats.norm.rvs(loc=5,scale=10,size=500)
#rvs2 = stats.norm.rvs(loc=5,scale=10,size=500)
#print("rvs1: ", rvs1)
#print("\n\nrvs2: ", rvs2)
r=[64,64,64,64,64,64,64,32,64,64,64,64,64,128,64,64,64,128,128,128,128,128,128,64,64,32,64,64,64,128,128,128,128,128,128,128,64,128,128,128,128,128,128,128,256,256,256,32,32,32]
alg=[256,256,64,256,256,256,128,256,256,128,256,256,64,256,128,256,256,64,256,128,256,512,256,64,128,256,256,128,128,256,128,256,256,256,128,128.256,128,256,256,256,128,256,128,256,128,256,256,32,256,512]
print(len(alg))
print(stats.ttest_ind(r,alg,equal_var=False))
print(stats.ttest_ind(alg,r,equal_var=False))