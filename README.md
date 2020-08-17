# Kind of Problems That This Simulator Solves

We consider the capacitated facility location problem 
with hard capacities. We are given a set of facilities, 
F, and a set of clients D in a common metric space. 
Each facility i has a facility opening cost f<sub>i</sub> and 
capacity u<sub>i</sub> that specifies the maximum number of 
clients that may be assigned to this facility. We want
 to open some facilities from the set F and assign 
 each client to an open facility so that at most u<sub>i</sub> 
 clients are assigned to any open facility i. 
 The cost of assigning client j to facility i is 
 given by their distance c<sub>ij</sub> , and our goal is to 
 minimize the sum of the facility opening costs and 
 the client assignment costs.
 
## Example of Running Problem
 
 <img src="media/Comput_Intel_course_pic1.gif" width="500">
  
# The Algorithms That Were Implemented
- [x] Greedy Algorithm 
- [x] Construction Heuristic 
- [x] Simulated Annealing 
- [x] Local Search 
- [x] Genetic Algorithm 

## Experiments - Settings & Results


| 50 iterations, 10 facilities, 5 problems, 0.1 ratio in cities | 20 iterations, 30 facilities, 5 problems, 0.1 ratio in cities |
| ------------------------------------------------------------- | ------------- |
| ![](media/10_fac.png)              | ![](media/30_fac.png) |


