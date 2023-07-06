The BettinaNetwork plant model concept.

BettinaNetwork accounts for resource allocation to root graft formation.
Root grafts are the fusion of root tissue, allowing woody plants to exchange resources such as water ([Graham and Bormann, 1966](https://doi.org/10.1007/BF02858662)).

BettinaNetwork is a child module of `pyMANGA.PlantModelLib.Bettina.Bettina`, i.e., plant geometry and growth is based on the single tree model Bettina ([Peters et al., 2014](https://doi.org/10.1016/j.ecolmodel.2014.04.001)).
In combination with Network below-ground modules, this module allows water exchange between root grafted plants. 

One of the following processes can be used to simulate a root graft formation:

- 'V0_instant' ... RGF happens immediately if roots are in contact and thus does not effect tree growth.
- 'V1_fixed' ... The duration of RGF is fixed (2 years) and tree growth is reduced by the factor f_growth.
- 'V2_adapted' ... The duration of RGF is a function of the minimum radius of the grafted roots and the energy available for graft growth. The minimum radius, in turn, is defined by the factor f_radius. The energy for root graft growth is taken from the energy designated to radial growth: w_gr = f_growth ∗ w_rstem.


Note:
    This module only works with a Network below-ground module.

Attributes:
    type (string): "BettinaNetwork"
    variant (string): variant used to simulate root graft formation. Possible inputs are: "V0_instant", "V1_fixed", "V2_adapted.
    f_growth (float): growth reduction factor, i.e. relative resource allocation during root graft formation. Range: 0... 1.
    


Examples:
    ```xml
    <plant_dynamics>
        <type> BettinaNetwork </type>
        <variant> V2_adapted </variant>
        <f_growth> 0.25 </f_growth>
    </plant_dynamics>
    ```

Possible outputs:
    Growth and geometry output is similar to `pyMANGA.PlantModelLib.Bettina.Bettina`
    ```xml
    <output> 
        <network_output> rgf </network_output> <!-- counter that describes root graft formation status -->
        <network_output> partner </network_output> <!-- list with tree names of partners -->
        <network_output> potential_partner </network_output> <!-- list with tree names of potential partners -->
        <network_output> water_available </network_output> <!-- available water for growth and maintenance in litre per timestep -->
        <network_output> water_absorbed </network_output> <!-- water absorbed from the soil in litre per timestep -->
        <network_output> water_exchanged </network_output> <!-- water exchanged between connected trees in litre per timestep -->
        <network_output> variant </network_output> <!-- variant for root graft formation -->
        <network_output> psi_osmo </network_output> <!-- osmotic potential of pore water -->
        <network_output> groupID </network_output> <!-- -unique group ID indicating which trees belong to the same group ->
        <network_output> node_degree </network_output> <!-- indicate how many partners a tree has -->
    </output>    
    ```
    Model output 'salinity' does not reflect pore water salinity correctly in this module. 
    Use network output 'psi_osmo' instead!

