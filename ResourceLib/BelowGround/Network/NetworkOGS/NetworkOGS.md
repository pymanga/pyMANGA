The NetworkOGS below-ground resource module.

NetworkOGS is a child of the modules `pyMANGA.ResourceLib.BelowGround.Network.Network.Network` and 
`pyMANGA.ResourceLib.BelowGround.Individual.OGSLargeScale3D.OGSLargeScale3D`.

Pore water salinity is calculated using the [OpenGeoSys](https://www.opengeosys.org/) approach.
Resource limitation is taken into account in the calculation of water distribution between root grafted trees.

Attributes:
    type (string): "NetworkOGS" (module name)
    f_radius (float): proportion of stem radius to set min. radius of grafted roots. Range: >0 to 1.
    ogs_project_folder (string): path to folder containing OGS input files
    ogs_project_file (string): name of OGS project file
    source_mesh (string): name of source mesh file
    bulk_mesh (string): name of bulk mesh file
    delta_t_ogs (float): (optional) time step length for OGS calculations. Can minimize computation time.
    python_script (string): (optional) name of python script for OGS to compute boundary conditions and source terms if other than default settings are to be used. Example file: python_source.py.
    abiotic_drivers (abiotic_drivers-nesting float): (optional) specification of abiotic drivers
    seaward_salinity (abiotic_drivers-nesting float): (optional) seawater salinity in kg/kg
    tide_daily_amplitude (abiotic_drivers-nesting float): (optional) amplitude of daily tide. Default: 1, i.e. the daily tide varies between -1 and 1 m around the average.
    tide_daily_period (abiotic_drivers-nesting float): (optional) period of daily tide. Default value is 12*60*60, i.e. the daily tide has a cycle of a half day.
    tide_monthly_amplitude (abiotic_drivers-nesting float): (optional) amplitude of monthly tide. Default: 0.5, i.e. the monthly fluctuation of means varies between -.5 and .5 m around mean sea level (0m).
    tide_monthly_period (abiotic_drivers-nesting float): (optional) period of monthly tide. Default: 24*60*60*15, i.e. the monthly tide has a cycle of 15 days.

Example:
    ```xml
    <belowground_competition>
        <type>NetworkOGS</type>
        <f_radius>0.25</f_radius>
        <ogs_project_folder>Benchmarks/ExampleSetups/OGSExampleSetup</ogs_project_folder>
        <ogs_project_file>testmodel.prj</ogs_project_file>
        <source_mesh>source_domain.vtu</source_mesh>
        <bulk_mesh>testbulk.vtu</bulk_mesh>
        <delta_t_ogs>86400</delta_t_ogs>
        <abiotic_drivers>
            <seaward_salinity>0.035</seaward_salinity>
        </abiotic_drivers>
        <python_script>python_script.py</python_script>
    </belowground_competition>
    ```
