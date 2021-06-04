### The Capacitated Plant Problem
#--------------------------------

import pulp as plp

# lists of customers and facilities
Customer = [1,2,3,4,5]
Facility = ['Factory1', 'Factory2', 'Factory3']

# dictionaries of fixed parameters in the model
Demand = {1:80,
          2:270,
          3:250,
          4:160,
          5:180}

Max_Supply = {'Factory1':500,
              'Factory2':500,
              'Factory3':500}

Fixed_cost = {'Factory1':1000,
              'Factory2':1000,
              'Factory3':1000}

transportation_cost = {'Factory1' : {1 : 4, 2 : 5, 3 : 6, 4 : 8, 5 : 10},
                       'Factory2' : {1 : 6, 2 : 4, 3 : 3, 4 : 5, 5 : 8},
                       'Factory3' : {1 : 9, 2 : 7, 3 : 4, 4 : 3, 5 : 4}
                      }


# construct the MIP-problem
model = plp.LpProblem("Capacitated plant problem", plp.LpMinimize)

# Fj and Xij decisions (using list comprehensions)
facilityIsActive = plp.LpVariable.dicts("Facility is active", Facility, 0, 1, plp.LpBinary)
serviceToCustomer = plp.LpVariable.dicts("Service", [(i,j) for i in Customer for j in Facility], 0)

# objective function (using list comprehensions)
model += plp.lpSum(Fixed_cost[j]*facilityIsActive[j] for j in Facility) + plp.lpSum(transportation_cost[j][i]*serviceToCustomer[(i,j)] \
                                                                                    for j in Facility\
                                                                                    for i in Customer)

# constraint 1: Match production with demand
for i in Customer:
    model += plp.lpSum(serviceToCustomer[(i,j)] for j in Facility) == Demand[i]

# constraint 2: Production & Shipping <= Capacity
for j in Facility:
    model += plp.lpSum(serviceToCustomer[(i,j)] for i in Customer) <= Max_Supply[j]*facilityIsActive[j]

# constraint 3: Shipping from i to j <= demand*facilityIsActive
for i in Customer:
    for j in Facility:
        model += serviceToCustomer[(i,j)] <= Demand[i]*facilityIsActive[j]
        

# solve optimization model
print(model.solve())

# display facility choice (binary decision variables)
tolerance = 0.0001
for j in Facility:
    if facilityIsActive[j].varValue > tolerance:
        print("Establish Facility at site: ", j)


# display the optimized production policy
for v in model.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

# display the optimized objective function
print("Objective function/ Minimized cost: ", plp.value(model.objective))











