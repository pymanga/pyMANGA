

 **Mortality** concepts define why trees die.  
The following concepts are available for `SimpleBettina` and `NetworkBettina`

- `NoGrowth`: trees die if growth is <= 0
- `Random`: trees die randomly with a defined probability
- `Memory`: trees die if biomass increment falls below a threshold based on preceding growth
- `MinGirthGrowth`: trees die if average preceding girth growth is less than a defined rate

Mortality concepts are defined using the tag `<mortality>`. 
The default concept is `NoGrowth` (no specification in the input xml file required).
Concepts can be combined by listing them in `<mortality>`, separated by a whitespace, e.g. `<mortality> random memory </mortality>`.
  

### Concept `NoGrowth`

In `NoGrowth`, a tree dies if the growth variable is equal or below 0, i.e. no growth happens. 

This concept is based on mechanistic causes, e.g. resource deficit, and no tree dies of random reasons.


### Concept `Random`

In `Random`, a tree dies with a defined yearly mortality probability.
If a random number times the number of time steps per year is below this defined probability the tree dies.
The default probability is 0.2 %. Berger & Hildenbrandt (2000) suggested 0.2 and 0.16 % for Rhizophora mangle and Avicennia germinans, respectively.  
Use `<probability> 0.002 </probability>` to modify concept parameters.

In this concept, a tree does not die of mechanistic reasons. It is useful to combine `Random` with `NoGrowth` or `Memory`.  


### Concept `Memory`

In `Memory`, a tree remembers its biomass increment of the preceding N years.
If the current biomass increment is below a certain percentage of average growth increment of the last N years the tree dies (similar to Berger & Hildenbrandt (2000)).
The period the memory lasts (N) is defined with `<period> </period>` in the xml file (default: 5 years).
The threshold (percentage) is defined with `<threshold> </threshold>` in the xml file (default: 0.5). The value must be a number between 0 and 1.  
Use `<period> 2 </period>` and `<threshold> 0.5 </threshold>` to modify concept parameters.

This concept is based on mechanistic causes, e.g. slowing down of growth due to tree age, and no tree dies of random reasons.


### Concept `MinGirthGrowth`

The concept is similar to `Memory` but uses girth growth as the relevant parameter to assess survival.  

`MinGirthGrowth` requires a minimum yearly girth growth rate in [cm per year]. 
If a trees moving average girth growth over the previous N years fell below the minimum rate, the tree dies.
The default growth rate is 0.05 cm per year (Grueters et al. 2021 for Rhizophora).  
Use `<period> 2 </period>` and `<min_girth_growth> 0.5 </min_girth_growth>` to modify concept parameters.

NOTE: The concept is only applied to trees with age > N as otherwise trees will die immediately.  
That is, the tree dies not immediately after recruitment.

This concept is based on mechanistic causes, e.g. slowing down of growth due to tree age, and no tree dies of random reasons.
