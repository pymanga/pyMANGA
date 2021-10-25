

`RandomGrowth` is a mortality concept.

In `RandomGrowth`, a tree dies with a biomass-dependent probability.
If a random number fall below this defined probability, the tree dies.
This probability is a function of relative biomass increment per time step, and a calibration factor `k_die`.
As relative biomass increment decreases over time, the probability to die increases.

Use `<k_die> 1e-11 </k_die>` to modify concept parameters.

In this concept, a tree dies of semi-mechanistic reasons.

