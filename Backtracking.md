### Backtracking Search Algorithm:
- **input**: the constrain satisfaction problem definition 

    - A CSP consists of:
Variables (X): The entities to assign values (e.g., X = {X1, X2, X3}).
Domains (D): Possible values for each variable (e.g., D(X1) = {1, 2, 3}).
Constraints (C): Rules restricting the values that variables can take (X1 ≠ X2).

- **output**: *returns a solution or a failure* 

```python 
def BACKTRACKING_SEARCH(csp) 
return Backtrack({},csp)
```
##### Backtracking algorithm 

- output:  *returns a solution or a failure* 

```python 
def BACKTRACKING(assignment,csp)
```
- first we check if the variables are assigned
if true return the assignment and halt the algorithm 

```python 
if assignment is complete then 
return assignment
```

- if not then select an unassigned variable (a heuristic can be used here to know which variable to select )
    - Min remaining values MRV
    - Least constraining value

```python 
var = SELECT_UNASSIGNED_VARIABLE(csp)
```
- not sure about order ORDER_DOMAIN_VALUES here but what I understood is that they order the values in a way that enhances performance 
``` python 
for value in ORDER_DOMAIN_VALUES (var, assignment, csp)
```


``` python 
if value is consistent with assignment then
add {var = value} to assignment
```

- apply forward checking  or ac-3 where we can prune subtrees 
```python
inferences = INFERENCE(sp, var, value) #forward checking 
if inferences # failure then
add inferences to assignment
```
- do recurrence 
``` python
result = BACKTRACK(assignment, csp)
if result # failure then return result
remove {var = value} and inferences from assignment
return failure
```
