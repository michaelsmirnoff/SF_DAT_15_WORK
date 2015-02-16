import matplotlib.pyplot as plt
from pylab import *
min_approvals = [0, 50, 60, 20, 100, 30]
nonmin_approvals = [0, 100, 90, 80, 75, 60]
years = [0,1,2,3,4,5]
years2 = ['0', '2009', '2010', '2011', '2012', '2013']
#plt.plot(x, y, label)
axes = figure().add_subplot(111)
a = axes.get_xticks().tolist()
a = years2
axes.set_xticklabels(a)
plt.plot(years, min_approvals, marker = 'o', color = 'r', label = 'minority approval rate')
plt.plot(years, nonmin_approvals, label='non-minority approval rate')
plt.ylabel('approval rate')
plt.title('Approval Rates by Minority Status')
plt.legend()
plt.ylim((0,100))
plt.show()