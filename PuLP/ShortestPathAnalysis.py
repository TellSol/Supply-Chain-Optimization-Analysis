# import the pulp package
import pulp as plp

N = 6  # Number of nodes in network
M = 2  # number of end nodes (source and destination)
INT = 4 # Number of intermediate nodes
H = 10000.0 # Arbitrary high cost
a = range(1, N+1)
al = range(N)
b = range(1,N+1)
bl = range(N)

# Index list for decision variables x
xindx = [(a[i],b[j]) for j in bl for i in al]

T = INT + M # number of artificial variables (y)
tindx = range(1, T+1)

# construct the LP-model instance
model = plp.LpProblem("Shortest Path Problem",plp.LpMinimize)

# Decision variables
x = plp.LpVariable.dicts("X", xindx,0,None)
y = plp.LpVariable.dicts("Y", tindx,0,None)

# The Pulp objective function
model += 0.0*x[1,1] + 4.0*x[1,2] + 2.0*x[1,3] + H*x[1,4] +H*x[1,5] + H*x[1,6]\
    + H*x[2,1] + 0.0*x[2,2] + H*x[2,3] + 5.0*x[2,4] + H*x[2,5]+ H*x[2,6]\
    + H*x[3,1] + 1.0*x[3,2] + 0.0*x[3,3] + 8.0*x[3,4] + 10.0*x[3,5]+ H*x[3,6]\
    + H*x[4,1] + H*x[4,2] + H*x[4,3] + 0.0*x[4,4] + 2.0*x[4,5]+ 6.0*x[4,6]\
    + H*x[5,1] + H*x[5,2] + H*x[5,3] + H*x[5,4] + 0.0*x[5,5] + 2.0*x[5,6] \
    + H*x[6,1] + H*x[6,2] + H*x[6,3] + H*x[6,4] + H*x[6,5] + 0.0*x[6,6] \
    , "Transportation cost"


# source and sink constraints
model += x[1,2] + x[1,3] -y[1] >= 1,"Source node"
model += x[4,6] + x[5,6] -y[2] >= 1,"Destination node"


# intermediate node constraints
model += x[1,2] + x[3,2] - x[2,4] - y[3] >= 0, "Node 2"
model += x[1,3] - x[3,2] - x[3,4] - x[3,5] - y[4] >= 0,"Node 3"
model += x[2,4] + x[3,4] - x[4,5] - x[4,6] - y[5] >= 0, "Node 4"
model += x[3,5] + x[4,5] - x[5,6] - y[6] >= 0, "Node 5"


# Solve the optimization problem using the GLPK-engine
isOpt = model.solve(plp.GLPK())

if isOpt == 1:
    print("optimal solution found")
else:
    print("optimal solution not found")


# display the optimized path and objective function
for v in model.variables():
    if v.varValue == 1.0:
        print(str(v.name) + ' = ' + str(v.varValue))

print("Minimized objective function: " + str(plp.value(model.objective)))


# Cluncky objective function. Can it be written more elegantly?