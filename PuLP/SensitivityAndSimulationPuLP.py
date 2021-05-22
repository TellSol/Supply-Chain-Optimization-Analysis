
#------------------------------------------------##
## SENSITIVITY ANALYSIS AND SIMULATION WITH PULP ##
#------------------------------------------------##

import pulp as plp
import pandas as pd
import random as rd
import matplotlib.pyplot as plt

## 1. SHADOW PRICES
#------------------

# Definition: The change in optimal value of the objective function with an
#             increase of the value of the given constraint (everything equal)


# lets rund an optimization, and loosen up on one of the constraints:


# initialize LpProblem class
model = plp.LpProblem("Maximize profits", plp.LpMaximize)

# define variables
A = plp.LpVariable('A', lowBound=0)
B = plp.LpVariable('B', lowBound=0)
C = plp.LpVariable('C', lowBound=0)

# define objective function
model += 500 * A + 450 * B + 600 * C

# C1: (working hours)
model += 6*A + 5*B + 8*C <= 60

# C2 (floor space)
model += 10.5*A + 20*B + 10*C <= 150

# C3 (demand of A)
model += A <= 8

# solve optimization problem
model.solve()

print("Model Status: {}".format(plp.LpStatus[model.status]))
print("Objective = ", plp.value(model.objective))
for v in model.variables():    
    print(v.name, "=", v.varValue)


# obtain SHADOW PRICES and interpret the output
o = [{'name':name, 'shadow price':c.pi}
    for name, c in model.constraints.items()]
print(pd.DataFrame(o))

# INTERPRETATION:

    # C1: If we increase the constraint from 60 to 61 hours, we would see an
    #     we would see an increase of 78.15 dollars to the objective function

    # C2: If we increase the constraint from 150 to 151 sq.feet, we would see 
    #     an increase of 2.96 dollars to the objective function

    # C3: If we increase the constraint from 8 to 9 units of A, we would see 
    #     no change to the objective function

    # THUS: Focus on increasing the working hours capacity!


## 2. SLACK OF A CONSTRAINT (SLACK VARIABLE):
#-------------------------------------------

# Definition: The amount of a resource that is unused

# we keep the previous opimization program and find the slack constraints
o = [{'name':name, 'shadow price':c.pi, 'slack':c.slack}
    for name, c in model.constraints.items()]
print(pd.DataFrame(o))


# INTERPRETATION:

    # C1 and C2 are utilizing their full capacity and are thus called "binding constraints"
    
    # C3 is not using all of its capacity and is thus called a "changing binding constraint"
    # as it cahnges solution when altered (review optimal decision of A 8 = 6.67 - 1.33)


# 3. SHADOW PRICE AND SLACK APPLICATION
#--------------------------------------

# initialize maximzation problem
model = plp.LpProblem("Maximize Bakery Profits", plp.LpMaximize)

# define variables
R = plp.LpVariable('Regular_production', lowBound=0, cat='Continuous')
J = plp.LpVariable('Jumbo_production', lowBound=0, cat='Continuous')

# define objective function
model += 5 * R + 10 * J, "Profit"

# Adjust the constraint (play with the values here and view the consequences
# shadow prices and slack constraints faces):
model += 0.5 * R + 1 * J <= 30
model += 1 * R + 2.5 * J <= 59

# Solve Model
model.solve()

# Print Status
print("Model Status: {}".format(plp.LpStatus[model.status]))
for v in model.variables():
    print(v.name, "=", v.varValue)
print("Objective = $", plp.value(model.objective))

# print Shadow and Slack with list comprehension
o = [{'name':name, 'shadow price':c.pi, 'slack': c.slack} 
     for name, c in model.constraints.items()]
print(pd.DataFrame(o))

# generally thinking: If slack constraints == 0, then all of the available
# capacity is utilized



## 4. SIMULATION TESTING WITH PULP
#---------------------------------

# up until now, we have ran models with no randomness in the parameters.
# however, that is seldom the case in the real world


# consider first optimization program, but now formulated stochasitcally

# lets say that the decision variables of the oobjective function follows N~[0,25]
model = plp.LpProblem("Maximize profits", plp.LpMaximize)

# define variables
A = plp.LpVariable('A', lowBound=0)
B = plp.LpVariable('B', lowBound=0)
C = plp.LpVariable('C', lowBound=0)

a,b,c = rd.normalvariate(0,25), rd.normalvariate(0,25), rd.normalvariate(0,25)

# define objective function
model += (500+a)*A + (450+b)*B + (600+c)*C

# C1: (working hours)
model += 6*A + 5*B + 8*C <= 60

# C2 (floor space)
model += 10.5*A + 20*B + 10*C <= 150

# C3 (demand of A)
model += A <= 8

# solve optimization problem
model.solve()

print("Model Status: {}".format(plp.LpStatus[model.status]))
print("Objective = ", plp.value(model.objective))
for v in model.variables():    
    print(v.name, "=", v.varValue)


## 4. APPLICATION: MONTE CARLO SIMULATION
#----------------------------------------
    
def run_optimization():
    
    # initialize optimization model
    model = plp.LpProblem("Maximize profits", plp.LpMaximize)
    
    # define variables
    A = plp.LpVariable('A', lowBound=0)
    B = plp.LpVariable('B', lowBound=0)
    C = plp.LpVariable('C', lowBound=0)
    
    a,b,c = rd.normalvariate(0,25), rd.normalvariate(0,25), rd.normalvariate(0,25)
    
    # define objective function
    model += (500+a)*A + (450+b)*B + (600+c)*C
    
    # C1: (working hours)
    model += 6*A + 5*B + 8*C <= 60
    
    # C2 (floor space)
    model += 10.5*A + 20*B + 10*C <= 150
    
    # C3 (demand of A)
    model += A <= 8
    
    # solve optimization problem
    model.solve()
    
    o = {'A': A.varValue, 'B': B.varValue, 'C': C.varValue,
         'OBJ': plp.value(model.objective)}
    return(o)


# conduct 100 monte carlo simuations
output = []

for i in range(100):
    output.append(run_optimization())

# store the results of each iteration in a pd.DataFrame
df = pd.DataFrame(output)

# check the frequecies of each decision variable
print(df['A'].value_counts())
print(df['B'].value_counts())
print(df['C'].value_counts())

# visualize the decision variables obtained by the monte carlo runs in a histogram
products = ['A', 'B', 'C']
for i in range(len(products)):
    plt.hist(df[str(products[i])], bins=50)
    plt.title("100 MonteCarlo Runs for " + str(products[i]))
    plt.ylabel("Frequency")
    plt.xlabel("Value of decision variable")
    plt.show()






