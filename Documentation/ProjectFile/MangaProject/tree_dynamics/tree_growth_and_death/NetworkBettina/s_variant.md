Variant used to simulate root graft formation (RGF). 

Possible inputs are: "V0", "V1" or "V2"

Meaning: 

- 'V0' ... RGF does not effect tree growth and trees are immediately grafted if roots are in contact.
- 'V1' ... The duration of RGF is fixed (2 years) and tree growth is reduced by a factor f_growth.
- 'V2' ... The duration of RGF is determined by a minimum radius of the grafted roots which in turn is defined by the factor f_radius. The  energy for root graft growth is taken from the energy designated to radial growth: w_gr = f_growth ∗ w_rstem.