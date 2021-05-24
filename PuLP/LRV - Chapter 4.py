
import pulp as plp
import pandas as pd

## exercise 4.4
#--------------

# a)

# initialize model
model = plp.LpProblem("Maximization problem", plp.LpMaximize)

# decision variables
x1 = plp.LpVariable('x1', lowBound=0)
x2 = plp.LpVariable('x2', lowBound=0)
x3 = plp.LpVariable('x3', lowBound=0)

# objective function
model += 4*x1 - 2*x2 + 3*x3

# constraints
model += 2*x1 + 2*x2 - x3 <= 6
model += x1 + 3*x2 - x3 <= 5
model += 2*x1 + x2 + 4*x3 <= 10

# solve the model (1 = optimal solution)
model.solve()

# optimized parameters
print("x1: " + str(x1.varValue))
print("x2: " + str(x2.varValue))
print("x3: " + str(x3.varValue))

# objective function
print("objective function: " + str(plp.value(model.objective)))

# b)

# The solution (1 1 1)T gives the slack variables s1 = 3, s2 = 2 and s3 = 3.
# The solution is feasible, but can never be optimal since all 6 variables
# in the objective function + slack variables are > 0. Thus it cannot be a
# a "corner point"/basic variable. The Simplex argorithm will not include this
# point in the search. 


## exercise 4.8
#--------------

# initialize model
model = plp.LpProblem("Maximization production", plp.LpMaximize)

# decision variables
x1 = plp.LpVariable('x1', lowBound=0)
x2 = plp.LpVariable('x2', lowBound=0)

# objective function
model += 3*x1 + 6*x2

# constraints
model += 2*x1 + 4*x2 <= 24
model += 3*x1 + 3*x2 <= 27
model += 3*x1 + 6*x2 <= 24
model += 4*x1 + 1*x2 <= 20


# solve the model (1 = optimal solution)
model.solve()

# optimized parameters
print("x1: " + str(x1.varValue))
print("x2: " + str(x2.varValue))

# objective function
print("objective function: " + str(plp.value(model.objective)))


## exercise 4.11
#---------------

model = plp.LpProblem("Maximization problem", plp.LpMaximize)

# decision variables
x1 = plp.LpVariable('part 1', lowBound=0)
x2 = plp.LpVariable('part 2', lowBound=0)
x3 = plp.LpVariable('part 3', lowBound=0)

# objective function
model += 50*x1 + 40*x2 + 60*x3

# constraints
model += 2*x1 + x2 + 2*x3 <= 120, "Cutting"
model += 3*x1 + 2*x2 + 2*x3 <= 150, "Shaping"
model += x1 >= 20, "forced production of part 1"

# solve the model (1 = optimal solution)
model.solve()

# optimized parameters
print("Part 1: " + str(x1.varValue))
print("Part 2: " + str(x2.varValue))
print("Part 3: " + str(x3.varValue))

# objective function
print("Objective function: " + str(plp.value(model.objective)))

# Is there any time left in any of the machines?
o = [{'name':name, 'slack': c.slack} 
     for name, c in model.constraints.items()]
print(pd.DataFrame(o))

# Slack variables s1 and s2 are both 0. Thus, there is no more available
# time for either cutting or shaping. Seems like efficient use of resources!

