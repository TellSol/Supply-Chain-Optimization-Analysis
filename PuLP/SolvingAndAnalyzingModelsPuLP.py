
### SOLVING AND ANALYZING MODELS USING PULP ###
#---------------------------------------------#

import pulp as plp

## 1. COMMON CONSTRAINT MISTAKES
#-------------------------------

# dependent constraints

# for each unit of B we must produce at least 3 of A: 3B <= A (not B <= 3A and 3B = A)
# example: 3(2) <= A gives 6 <= A


# APPLICATION 1: PRODUCTION >= DEMAND
#------------------------------------

demand = {'A':[0,0,0],
          'B':[8,7,6]}

costs = {'A':[20,17,18],
         'B':[15,16,15]}

# Initialize Model
model = plp.LpProblem("Aggregate Production Planning", plp.LpMinimize)

# Define Variables
time = [0, 1, 2]
prod = ['A', 'B']
X = plp.LpVariable.dicts("prod", [(p, t) for p in prod for t in time], 
                     lowBound=0, cat="Integer")

# Define Objective
model += plp.lpSum([costs[p][t] * X[(p, t)] for p in prod for t in time])

# Define Constraint So Production is >= Demand
for p in prod:
    for t in time:
        model += X[(p, t)] >= demand[p][t]
        
# view the current model
print(model)


# *VIEW DataCamp Code for further modelling mistakes in depth*


# APPPLICATION 2: TOTAL PRODUCTION = TOTAL DEMAND & TOTAL PRODUCTION <= PRODUCTION CAPACITY
#------------------------------------------------------------------------------------------

# dataFrames fix_cost and var_cost can be found in DataCamp

# Initialize, Define Decision Vars., and Objective Function
model = plp.LpProblem("Capacitated Plant Location Model", plp.LpMinimize)

loc = ['USA', 'Germany', 'Japan', 'Brazil', 'India']
size = ['Low_Cap','High_Cap']

x = plp.LpVariable.dicts("production_", [(i,j) for i in loc for j in loc],
                     lowBound=0, upBound=None, cat='Continuous')
y = plp.LpVariable.dicts("plant_", 
                     [(i,s) for s in size for i in loc], cat='Binary')

model += (plp.lpSum([fix_cost.loc[i,s] * y[(i,s)] for s in size for i in loc])
          + plp.lpSum([var_cost.loc[i,j] * x[(i,j)] for i in loc for j in loc]))

# Define the constraints

# set the sum of production at loc i == sum of demand unit j
for j in loc:
    model += plp.lpSum([x[(i, j)] for i in loc]) == demand.loc[j,'Dmd']

# set sum of production <= sum of capacity of the chosen plants
for i in loc:
    model += plp.lpSum([x[(i,j)] for j in loc]) <= plp.lpSum([cap.loc[i,s] * y[(i,s)]for s in size])


# CHALLENGE: insert the pd.dataframes and find the optimal solution


# 4. SOLVING PULP MODELS
#-----------------------
    
# Recall the two-variable problem:

model = plp.LpProblem("Maximize Glass Co. Profits", plp.LpMaximize)

# Define Decision Variables
wine = plp.LpVariable('Wine', lowBound=0, upBound=None, cat='Integer')
beer = plp.LpVariable('Beer', lowBound=0, upBound=None, cat='Integer')

# Define Objective Function
model += 5 * wine + 4.5 * beer

# Define Constraints
model += 6 * wine + 5 * beer <= 60
model += 10 * wine + 20 * beer <= 150
model += wine <= 60

# Solve Model (1 = Solved)
model.solve()

# display the optimimal choice of decision variables
print("OPTIMAL SOLUTION:")
print("Produce {} batches of wine glasses".format(wine.varValue))
print("Produce {} batches of beer glasses".format(beer.varValue))

# print the value of the objective function
print("GIVES THE OBJECTIVE FUNCTION VALUE OF: " + str(plp.value(model.objective)))

# check if the solution is optimal (can also be infeasible, not solved, unbounded etc.)
print("STATUS: ", plp.LpStatus[model.status])



# 5. VALIDATION OF PULP MODELS
#-----------------------------

# (contuning with the code from 4.)

# write a file to the current directory to inspect the
# optimization program components

fileName = "validationLP.txt"
model.writeLP(fileName)
f = open(fileName)
print(f.read())
f.close()

# other file formats are available as well
model.writeLP("validationLP.lp")
model.writeLP("validationLP.csv")

