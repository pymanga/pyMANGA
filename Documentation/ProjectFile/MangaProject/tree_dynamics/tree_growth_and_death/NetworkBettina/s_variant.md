Variant used to simulate root graft formation (RGF). 

Possible inputs are: "V0_instant", "V1_fixed" or "V2_adapted"

The suffix describes the duration of the RGF process, i.e.: 

- 'V0_instant' ... RGF happens immediately if roots are in contact and thus does not effect tree growth.
- 'V1_fixed' ... The duration of RGF is fixed (2 years) and tree growth is reduced by the factor f_growth.
- 'V2_adapted' ... The duration of RGF is a function of the minimum radius of the grafted roots and the energy available for graft growth. The minimum radius, in turn, is defined by the factor f_radius. The  energy for root graft growth is taken from the energy designated to radial growth: w_gr = f_growth ∗ w_rstem.