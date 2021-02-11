
### SUPPLY CHAIN ANALYTICS USING PULP ###
#---------------------------------------#

# import the required packages
import pulp as plp


## 1. A SIMPLE TWO VARIABLE PROBLEM
#----------------------------------

    # lets plan the optimal mix of production of beer and wine glasses.
    # >there is a maximum production capacity of 60 hours
    # >each batch of wine and beer glasses takes 6 and 5 hours respectively
    # >the warehouse has a maximum capacity of 150 rack spaces
    # >each batch of the wine and beer glasses takes 10 and 20 spaces respectively
    # >the production equipment can only make full batches, no partial batches
    # Also, we only have orders for 6 batches of wine glasses. Therefore, we do not 
    # want to produce more than this. Each batch of the wine glasses earns a profit 
    # of $5 and the beer $4.5.
    
    # The objective is to maximize the profit for the manufacturer.


# Initialize the model
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

# Solve Model
model.solve()
print("OPTIMAL SOLUTION:")
print("Produce {} batches of wine glasses".format(wine.varValue))
print("Produce {} batches of beer glasses".format(beer.varValue))
print("GIVES THE OBJECTIVE FUNCTION VALUE OF:")
print(plp.value(model.objective))


## 2. SCALE VARIABLES WITH LpSum AND LIST COMPREHENSION
#------------------------------------------------------

# input data for the model:
costs = {('Atlanta', 'East'): 232,
         ('Atlanta', 'Midwest'): 230,
         ('Atlanta', 'South'): 212,
         ('Atlanta', 'West'): 280,
         ('New York', 'East'): 211,
         ('New York', 'Midwest'): 240,
         ('New York', 'South'): 232,
         ('New York', 'West'): 300}

var_dict = {('Atlanta', 'East'): 'atle',
            ('Atlanta', 'Midwest'): 'atlm',
            ('Atlanta', 'South'): 'atls',
            ('Atlanta', 'West'): 'atlw',
            ('New York', 'East'): 'ne',
            ('New York', 'Midwest'): 'nm',
            ('New York', 'South'): 'ns',
            ('New York', 'West'): 'nw'}


# Initialize Model
model = plp.LpProblem("Minimize Transportation Costs", plp.LpMinimize)

# Build the lists and the demand dictionary
warehouse = ['New York', 'Atlanta']
customers = ['East', 'South', 'Midwest', 'West']
regional_demand = [1800, 1200, 1100, 1000]
demand = dict(zip(customers, regional_demand))

# Define Objective
model += plp.lpSum([costs[(w, c)] * var_dict[(w, c)] 
                for c in customers for w in warehouse])

# For each customer, sum warehouse shipments and set equal to customer demand
for c in customers:
    model += plp.lpSum([var_dict[(w, c)] for w in warehouse]) == demand[c]
    
# (THROWS AN ERROR. LOOK AT DC-OUTPUT CODE, LOGIC CAN BE APPLIED HERE!)

    
## 3. SCALE WITH THE LpVariable FUNCTION
#---------------------------------------

# Input data for the model
costs = {('Atlanta', 'East'): 232,
         ('Atlanta', 'Midwest'): 230,
         ('Atlanta', 'South'): 212,
         ('Atlanta', 'West'): 280,
         ('New York', 'East'): 211,
         ('New York', 'Midwest'): 240,
         ('New York', 'South'): 232,
         ('New York', 'West'): 300}

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

warehouse = ['New York', 'Atlanta']

customers = ['East', 'South', 'Midwest', 'West']

# Initialize optimization model
model = plp.LpProblem("Cost-Minimizing Transportation Plan", plp.LpMinimize)


# Define decision variables using list comprehension
key = [(m, w, c) for m in months for w in warehouse for c in customers]
var_dict = plp.LpVariable.dicts('num_of_shipments', 
                            key, 
                            lowBound=0, cat='Integer')

# Use the LpVariable dictionary variable to define objective
model += plp.lpSum([costs[(w, c)] * var_dict[(m, w, c)] 
                for m in months for w in warehouse for c in customers])

model.solve()

# Challenge: Print the results of the cost-minimizing transportation plan



## 4. APPLICATION: LINEAR SCHEDULING PROBLEM
#-------------------------------------------

    # PROBLEM:
    
    # Warehouse guys can work in 5 consecutive days
    # These are the hiring requirements:
    
    # Day of Week 	Employees Needed
    # 0 = Monday 	31
    # 1 = Tuesday 	45
    # 2 = Wednesday 40
    # 3 = Thursday 	40
    # 4 = Friday 	48
    # 5 = Saturday 	30
    # 6 = Sunday 	25
    
    # Decide the optimal shift composition to minimize the number of hires
    # and overlap.



# The class has been initialize, and x, days, objective function defined
model = plp.LpProblem("Minimize Staffing", plp.LpMinimize)

days = list(range(7))
x = plp.LpVariable.dicts('staff_', days, lowBound=0, cat='Integer')

model += plp.lpSum([x[i] for i in days])

# Define Constraints (without list comprehension)
model += x[0] + x[3] + x[4] + x[5] + x[6] >= 31
model += x[0] + x[1] + x[4] + x[5] + x[6] >= 45
model += x[0] + x[1] + x[2] + x[5] + x[6] >= 40
model += x[0] + x[1] + x[2] + x[3] + x[6] >= 40
model += x[0] + x[1] + x[2] + x[3] + x[4] >= 48
model += x[1] + x[2] + x[3] + x[4] + x[5] >= 30
model += x[2] + x[3] + x[4] + x[5] + x[6] >= 25

# inspect the constrained equation set built so far
print(model)

# Run the simplex algorithm to find optimal solution
model.solve()

# inspect the optimized decsion variables:

print("OPTIMAL SOLUTION:")
for i in range(len(x)):
    print("amount of workers on shift nr " + str(i) +":"" {} warehouse workers".format(x[i].varValue))



## 4. APPLICATION: PREVENTATIVE MAINTENANCE SCHEDULING
#-----------------------------------------------------

    # PROBLEM:
        
    # At a quarry they use diamond saws to cut slabs of marble. For preventative 
    # maintenance the saws are only allowed to run for 4 consecutive hours, afterwards 
    # a 1 hour inspection is completed before they are allowed to go back into service. 
    # The quarry operates 10-hour shifts. At the end of the shift if the saw blades have 
    # not been used for 4 consecutive hours the remaining time will be used at the start 
    # of the next shift.
        
    # Expected number of saw blades:
    
    # Hour 	Saws Needed
    # 0 	 7
    # 1 	 7
    # 2 	 7
    # 3 	 6
    # 4 	 5
    # 5 	 6
    # 6 	 6
    # 7 	 7
    # 8 	 7
    # 9 	 6
        
    # Determine the minimum number of saw blades needed for the shift.


# The class has been initialize, and x, hours and objective fuction defined
model = plp.LpProblem("Minimize Staffing", plp.LpMinimize)

hours = list(range(10))
x = plp.LpVariable.dicts('saws_', hours, lowBound=0, cat='Integer')

model += plp.lpSum([x[i] for i in hours])

# Define Constraints
model += x[0] + x[2] + x[3] + x[4] + x[5] + x[7] + x[8] + x[9] >= 7
model += x[0] + x[1] + x[3] + x[4] + x[5] + x[6] + x[8] + x[9] >= 7
model += x[0] + x[1] + x[2] + x[4] + x[5] + x[6] + x[7] + x[9] >= 7
model += x[0] + x[1] + x[2] + x[3] + x[5] + x[6] + x[7] + x[8] >= 6
model += x[1] + x[2] + x[3] + x[4] + x[6] + x[7] + x[8] + x[9] >= 5
model += x[0] + x[2] + x[3] + x[4] + x[5] + x[7] + x[8] + x[9] >= 6
model += x[0] + x[1] + x[3] + x[4] + x[5] + x[6] + x[8] + x[9] >= 6
model += x[0] + x[1] + x[2] + x[4] + x[5] + x[6] + x[7] + x[9] >= 7
model += x[0] + x[1] + x[2] + x[3] + x[5] + x[6] + x[7] + x[8] >= 7
model += x[1] + x[2] + x[3] + x[4] + x[6] + x[7] + x[8] + x[9] >= 6

model.solve()


# inspect the optimized decsion variables:
print("OPTIMAL SOLUTION:")
for i in range(len(x)):
    print("amount of saws for shift nr " + str(i) +":"" {}".format(x[i].varValue))
    


## 5. APPLICATION: CAPACITATED PLANT LOCATION SELECTION
#------------------------------------------------------
    
    # PROBLEM:
        
    # Construct an optimization program for a capacitated plant location selection
    # (No input data here, just for displaying possible problem formulation,
    # dataframes can be found on DC CH.2)


# Initialize Class
model = plp.LpProblem("Capacitated Plant Location Model", plp.LpMinimize)

# Define Decision Variables
location = ['USA', 'Germany', 'Japan', 'Brazil', 'India']
size = ['Low_Cap','High_Cap']

x = plp.LpVariable.dicts("production_",
                     [(i,j) for i in location for j in location],
                     lowBound=0, upBound=None, cat='Continous')
                     
y = plp.LpVariable.dicts("plant_", 
                     [(i,s) for s in size for i in location], cat='Binary')


# Define objective function

model += (
    
    # fixed cost component
    plp.lpSum([fix_cost.loc[i,s] * y[(i,s)] 
               for s in size for i in location])
    
    # variable cost component
   + plp.lpSum([var_cost.location[i,j] * x[(i,j)] 
                for i in location for j in location])
   )


## 6. LOGICAL CONSTRAINTS
#------------------------

# lets select the optimal loading policy of a cargo truck:


# input data (products has a given profitability and weight. Increased weight
# consumes more of the loading weight constraint)

products = ['A', 'B', 'C', 'D', 'E', 'F']

weight = {'A':12800, 
          'B':10900, 
          'C':11400, 
          'D':2100, 
          'E':11300, 
          'F':2300}

profitability = {'A':77878, 
                 'B':82713, 
                 'C':82728, 
                 'D':68423, 
                 'E':84119, 
                 'F':77765}

# initialize the LpProblem class
model = plp.LpProblem("Loading Truck Problem",
                      plp.LpMaximize)

# define decsion variables
x = plp.LpVariable.dicts('Ship_', products,
                         cat='Binary')

# define objective function
model += plp.lpSum(profitability[i]*x[i] for i in products)

# define constraints

#1: Cannot load more than 20 000 kg in total
model += plp.lpSum(weight[i]*x[i] for i in products) <= 20000

#2: Cannot load E and D in the same truck load
model += x['E'] + x['D'] <= 1

#3: If we ship D, then we must also ship product B (e.g. complementary goods)
model += x['D'] <= x['B']

# solve model and display optimal loading policy
model.solve()
for i in products:
    print("{} status {}".format(i, x[i].varValue))

print("GIVES THE OBJECTIVE FUNCTION VALUE OF:")
print(plp.value(model.objective))


## 7. APPLICATION: CARGO TRUCK DELIVERY CHOICE

# You have one available route of choice, and you want to minimize the distance travelled

# Location 	Distance
#     A 	   86
#     B 	   95
#     C 	   205
#     D 	   229
#     E 	   101
#     F 	   209

# constraints: > If you visit A you have to visit D
#              > If you visit B you have to visit E

# input data:
dist = {'A': 86, 
        'B': 95, 
        'C': 205, 
        'D': 229, 
        'E': 101, 
        'F': 209}

cust = ['A', 'B', 'C', 'D', 'E', 'F']

# initialize the model
model = plp.LpProblem("Loading Truck Problem", plp.LpMinimize)

# define variables
x = plp.LpVariable.dicts('ship_', cust, cat='Binary')
model += plp.lpSum([dist[i]*x[i] for i in cust])


# define constraints

#1: Forced to pick a route
model += x['A'] + x['B'] + x['C'] + x['D'] + x['E'] + x['F'] >= 1

#2: If visit A, then also D
model += x['A'] - x['D'] <= 0

#3: If visit B, then also E
model += x['B'] - x['E'] <= 0


# solve the optimization problem
model.solve()
for i in cust:
    print("{} status {}".format(i, x[i].varValue))
print("Total distance commited to is: " + str(plp.value(model.objective)))

