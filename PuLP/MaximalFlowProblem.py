
### MAXIMAL FLOW PROBLEM
#-----------------------

import pulp as plp

# define useful variables
N = 5
INT = 3
a = range(1, N+1)
al = range(N)
b = range(1,N+1)
bl = range(N)
xindx = [(a[i],b[j]) for j in bl for i in al]
T = INT + 1
tindx = range(1, T+1)

# initialize optimization model
model = plp.LpProblem("Maximize flight ", plp.LpMaximize)

# decision variables
x = plp.LpVariable.dicts("X", xindx, lowBound=0, upBound=None)
y = plp.LpVariable.dicts("X", tindx, lowBound=0, upBound=None)

# objective function
model += x[1,2], "Maximum Flow"

# Source and Destination Constraints
model += x[1,2] - x[4,5] - x[3,5] + y[1] <= 0, "Source to destination"

# Arc capacity constraints
model += x[1,2] <= 7,"Arc 1-2"
model += x[2,3] <= 4,"Arc 2-3"
model += x[2,4] <= 3,"Arc 2-4"
model += x[3,4] <= 6,"Arc 3-4"
model += x[3,5] <= 3,"Arc 3-5"
model += x[4,5] <= 4,"Arc 4-5"

# Intermediate Node Constraints
model += x[1,2] - x[2,3] - x[2,4] + y[2] <= 0,"Node 2"
model += x[2,3] - x[3,4] - x[3,5] + y[3] <= 0,"Node 3"
model += x[2,4] + x[3,4] - x[4,5] + y[4] <= 0,"Node 4"

# solve optimization model
model.solve()

# display optimized path and objective function
for v in model.variables():
    print(str(v.name) + "=" + str(v.varValue))

print("Objective Function: " + str(plp.value(model.objective)))









