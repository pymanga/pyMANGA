# Description

This module calculates the reduction in above-ground resource availability caused by available net solar radiation. Calculations for net radiation are based on the FAO guidelines for computing crop water requirements [Allen et al. 1998](https://agris.fao.org/search/en/providers/122621/records/647231eb53aa8c896301eadc). Net solar radiation is the difference between incoming net solar radiation and the outgoing net longwave radiation and it depends on the latitude and temperature of a certain location. 

The above-ground resource factor is the ratio of actual to maximum net radiation at a given time and location. Maximum net radiation is the maximum radiation for the given location.

Calculations are simplified by only needing yearly maximum and minimum temperature to reduce required user input. Results do not change significantly when using yearly temperatures compared to monthly temperatures. Each time step is then estimated from a sine curve that is fitted to the solar radiation data. By doing so, all calculations are done during the initialisation and do not require any further calculations during the simulation.  

# Usage 

```xml
    <resources>
        <aboveground>
            <type> SolarRadiation </type>
            <latitude> 0.65 </latitude>
            <tmin>24.33</tmin>
            <tmax>30.7</tmax>
        </aboveground>
        <belowground>
            <type> Default </type>
        </belowground>
    </resources>
```

# Attributes

* `type` (string): "SolarRadiation"
* `latitude` (float): Latitude of the location in radians.
* `tmin` (float): Minimum temperature in degrees Celsius.
* `tmax` (float): Maximum temperature in degrees Celsius.
* `albedo` (float): (optional) Albedo of the surface. Default: 0.23.
* `altitude` (float): (optional) Altitude of the location in meters. Default: 0.
* `noise` (float): (optional) Noise factor for the solar radiation. Default: Calculations explained in **Process overview** below. 

# Value

This factor is used to calculate the above-ground resources for the simulation. It is a float value between 0 and 1.  

# Details 

## Purpose

This module calculates the amount of solar radiation that is available for the plants as an above-ground resource. Solar radiation is the primary energy source for plants and is used for photosynthesis and growth. The net solar radiation is converted into a factor ranging from 0 to 1.  

## Process overview

When `SolarRadiation` is initialized, the solar radiation is calculated for the whole year. Then, at each time step, `calculateAbovegroundResources` is called and pulls the solar radiation for the respective day of the year and converts it into a factor usable by the `ResourceModel`.  

## Sub-processes

### calculateNetSolarRadiation

Calculates the net solar radiation based on the latitude, temperature, and altitude following the FAO guidelines for computing crop water requirements (Allen et al. 1998). This process also fits the calculated monthly solar radiation to a sine curve to estimate solar radiation for every day of the year.  

### sineFunction

Builds a basic sine function that takes time, amplitude, frequency, phase shift, and vertical shift as input parameter to return a time series that follows a sine curve. This process is used by `calculateNetSolarRadiation` to estimate solar radiation for every day of the year.  


## References 

Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998). Crop evapotranspiration: guidelines for computing crop water requirements. FAO Irrigation and drainage paper, 56, D05109.

## Authors 

Ruben M Jardner

## See Also

## Examples 

* Use solar radiation as above-ground resource. Latitude is set at 0.65 radians, minimum temperature is 24.33 degrees Celsius, and maximum temperature is 30.7 degrees Celsius. All other optional parameters are set to default values.  

```xml
    <resources>
        <aboveground>
            <type> SolarRadiation </type>
            <latitude> 0.65 </latitude>
            <tmin>24.33</tmin>
            <tmax>30.7</tmax>
        </aboveground>
        <belowground>
            <type> Default </type>
        </belowground>
    </resources>
```

* Use solar radiation as above-ground resource and provide input for all optional parameters.
  * Latitude is set at 0.65 radians.
  * Minimum temperature is 24.33 degrees Celsius.
  * Maximum temperature is 30.7 degrees Celsius.
  * Albedo is set to 0.23.
  * Altitude is set to 0 meters.
  * Noise is fixed at 0.1.

```xml
    <resources>
        <aboveground>
            <type> SolarRadiation </type>
            <latitude> 0.65 </latitude>
            <tmin>24.33</tmin>
            <tmax>30.7</tmax>
            <albedo> 0.23 </albedo>
            <altitude> 0 </altitude>
            <noise> 0.1 </noise>
        </aboveground>
        <belowground>
            <type> Default </type>
        </belowground>
    </resources>
```
