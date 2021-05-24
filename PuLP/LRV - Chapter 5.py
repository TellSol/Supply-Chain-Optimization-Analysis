
import pulp as plp
import pandas as pd

### exercise 5.4
#---------------

# a)

# initialize LP-model class
model = plp.LpProblem("Maximization", plp.LpMaximize)

# decision variables
x1 = plp.LpVariable("x1", lowBound=0)
x2 = plp.LpVariable("x2", lowBound=0)

# objective function
model += x1 + 3*x2

# constraints
model += x1 + x2 <= 8, "resource 1"
model += -x1 + x2 <= 4, "resource 2"
model += x1 <= 6, "resource 3"

# solve model and display solution
model.solve()

print("x1: " + str(x1.varValue))
print("x2: " + str(x2.varValue))

print("objective function: " + str(plp.value(model.objective)))

# b)

# print the shadow prices

o = [{'name':name, 'shadow price':c.pi}
    for name, c in model.constraints.items()]
print(pd.DataFrame(o))

# c)

# generate sensitivity report from the GLPK-engine
model.solve(plp.GLPK(options=['--ranges sensitivity.sen']))


# Q: how much can c1 and c2 change for the optimal solution to remain the same?
# A: x1 => [-3,3], x2 => [1,infinity)

# d)

# Q: how much can the RHS constraint coefficients change without affecting the shadow prices
# A: c1 => [4,16], c2 => [-4,8], c3 => [2,infinity)






