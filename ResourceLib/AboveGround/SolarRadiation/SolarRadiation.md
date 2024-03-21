# Description

The solar radiation above-ground resource concept.  
This concept provides a above-ground resource factor calculated from the net solar radiation. Calculations are based on the FAO guidelines for computing crop water requirements [Allen et al. 1998](https://agris.fao.org/search/en/providers/122621/records/647231eb53aa8c896301eadc). The code is strongly inspired by the now deprecated python package [PyETo](https://github.com/woodcrafty/PyETo). The solar radiation used for the above-ground resources represents the difference between incoming net solar radiation and the outgoing net longwave radiation based on latitude and temperature. Further, default assumptions for albedo, altitude, and variation are made, but can also be provided as input in the project file.  

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

