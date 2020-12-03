
### NETWORK ANALYSIS WITH IGRAPH ###

require(igraph)
require(tidyverse)

# 1. Measure connectedness of points
#-----------------------------------

# create a sample network
set.seed(1)
g1 <- sample_pa(10, power = 1, directed = FALSE)
plot(g1)

# display the number of connections of each node ()
degree(g1)

## NOTE: Node 1 especially is very important to the network (Might be a distribution center or a popular person?)


# 2. Measure betweenness of points
#---------------------------------

# create a sample network
set.seed(2)
g2 <- sample_pa(10, power = 1, directed = FALSE)
plot(g2)

# measure betweenness of graph
betweenness(g2)

## NOTE: Nodes 1 and 6 represent important bridges


# 3. Measure network denisty
#---------------------------

# create a sample network
set.seed(3)
g3 <- sample_pa(10, power = 1, directed = FALSE)
plot(g3)

edge_density(g3, loops = FALSE)

# create another sample network
set.seed(4)
g4 <- sample_pa(20, power = 1, directed = FALSE)
plot(g4)

edge_density(g4, loops = FALSE)

## NOTE: The edge_density measure is the same as 2/n, where n is the number of nodes


# 4. Identify cliques in a network
#---------------------------------

# create a sample network
set.seed(6)
gnp <- sample_gnp(20, 0.25, directed = FALSE, loops = FALSE)
plot(gnp)

clique_num(gnp)
cliques(gnp)
cliques(gnp, min = 3)

## NOTE: The network contains 100 cliques where 25 cliques have 3 (or more) nodes


# 5. Identify components in a network
#------------------------------------

# create a sample network
set.seed(7)
gnp1 <- sample_gnp(30, 0.04, directed = FALSE, loops = FALSE) 
plot(gnp1)

# identify the components of the graph
comp <- components(gnp1)

# attributes of the network-components
comp$membership
comp$no
comp$csize

## NOTE: This can for instance mean that Truck #30 and Truck #18 belongs to different warehouses
##       and therefore are in independent components

# 6. Take a random walk
#----------------------

# create a sample network
set.seed(8)
g5 <- sample_gnp(30, 0.08, directed = FALSE)
plot(g5)

# perform a random walk on the network
random_walk(g5, 26, 8, stuck = "return")


# 7. Visualize networks more effectively

# create a sample network and color nodes blue, edges black and DC-node 3 orange
set.seed(6)
g6 <- sample_gnp(15,0.2) %>% 
  set.vertex.attribute("color", value = "lightblue") %>% 
  set.edge.attribute("color", value = "black") 
V(g6)[3]$color <- "orange"

plot(g6)

# split a network into components and assign them distinct colors
set.seed(10)
g7 <- sample_gnp(10 ,0.12, loops = FALSE)

for (i in 1:length(V(g7))){
  if (components(g7)$membership[i] == 1){
    V(g7)[i]$color <- "orange"
  } else if (components(g7)$membership[i] == 2){
    V(g7)[i]$color <- "lightblue"
  } else{
    V(g7)[i]$color <- "lightgreen"
  }
}
plot(g7)




