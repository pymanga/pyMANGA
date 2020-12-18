---
title: "The Model (Arbeitstitel)"
linkTitle: "The Model (Arbeitstitel)"
weight: 3
description:
---

<head>
<style type="text/css">
<!--
#vis {
  border: 1px solid black;
}
#Rahmen {
        border-width: 0.1em; 
        border-style: solid;
        text-align:right;
}
-->
</style>
</head>





# Model Domain

A transect 185 m long and 10 m wide is represented in the model (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_1">Figure 1</a>).
Allometry data from a transect measurement, as well as measurement results from a long-term study, are used to evaluate the model results. The long-term study documents the effects of fertilization on the growth of 72 mangroves, half of which are located on the landward and half on the seaward side of the transect (see also <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4</a>).

<figure>
<a name="Figure_1"></a>
<img src="/pictures/exmouth_gulf/Transect_Sketch.png">
<figcaption><font size = "1"><i><b>Figure 1:</b> Model Domain</i></font></figcaption>
</figure><br>


# Modeling (Arbeitstitel)

## Model variants

Mangrove growth was simulated using three different models (see also <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_1">Table 1</a>). 

In the model <b>"Model Without Feedback"</b> the dynamic changes in abiotic influences (tides, groundwater recharge and salinity of seawater are included via boundary conditions. The influence of plant water extraction on pore water salinity was not modeled.

The model <b>"Model Without Tide"</b> considers the effects of plant water extraction on the salinity of the pore water and all abiotic influences of the first model - with exception of the tides.

Finally, the third model variant (<b>"Full Model"</b>) reproduces both, the dynamics of tides and the coupling of plant water extraction and pore water.

The following <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_1">Table 1</a> summarizes the specifications of the three model variants.


<figure>
<figcaption align="top"><font size = "1"><i><b>Table 1:</b> Model variants</i></font></figcaption>
<a name="Table_1"></a>
<table border="1" rules="all" width="100%">
 <tr>
  <td  width="27%" style="text-align: center; vertical-align: middle;" style="display:none;">
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
   Tides
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
   Coupling plant water balance and pore water
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
   Other abiotic factors
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle;">
   Model Without Feedback
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle;">
   Model Without Tide
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle;">
   Full Model
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle;">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
</table>
</figure>
<br>

## Discretization

### Groundwater model

The groundwater model represents the subsurface with a grid of dimensions of 10 m x 230 m x 3 m on five FEM layers with 5880 cells. The following <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_2">Figure 2</a> shows the spatial discretization from a seaward perspective.

<figure>
<a name="Figure_2"></a>
<img src="/pictures/exmouth_gulf/dis.png">
<figcaption><font size = "1"><i><b>Figure 2:</b> Spatial discretization of the groundwater model</i></font></figcaption>
</figure><p>

The mangroves extract soil water from the subsurface from a depth of 40 cm to 80 cm below the ground surface. <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_3">Figure 3</a> shows the model area (gray) and the area of water extraction by the mangroves (blue). Note the 50-fold scaling in the z-direction. 

<figure>
<a name="Figure_3"></a>
<img src="/pictures/exmouth_gulf/model_area_legend.png">
<figcaption><font size = "1"><i><b>Figure 3:</b> Area of water extraction by mangroves</i></font></figcaption>
</figure><p>

The groundwater model is discretized in time with a time step length of one hour. The tidal range as a dynamic boundary condition is represented with the time series of the years 1991 to 1993, which is set in loops over the entire model runtime.

### Baumwachstumsmodell

Since each mangrove is represented as a single individual, a spatial discretization in proper sense does not take place. Temporally, the tree growth model is discretized with a time step length of half a year (1 a = 365.25 d).

## Boundery Conditions

### Tree growth model

## Parameterization

The following tables show the parameterizations of the subsurface (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_2">Table 2</a>) and the mangroves (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_3">Table 3</a>), global weighting factors (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_4">Table 4</a>), and the initial values of the geoemtries of the mangrove seedlings (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_5">Table 5</a>).

### Subsurface

<table>
<tablecaption align="top"><font size = "1"><i><b>Table 2:</b> Parameterizations of subsurface</i></font></tablecaption>
<a name="Table_2"></a>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Parameter Name</th>
<th style="text-align: left;">Value</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Molecular diffusion coefficient</td>
<td style="text-align: left;">1 × 10<sup>-9</sup> m<sup>2</sup>/s</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>T</em></sub></span></td>
<td style="text-align: left;">Transversal dispersivity</td>
<td style="text-align: left;">0.5 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>β</em><sub><em>L</em></sub></span></td>
<td style="text-align: left;">Longitudinal dispersivity</td>
<td style="text-align: left;">1 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>ρ</em></span></td>
<td style="text-align: left;">Water density</td>
<td style="text-align: left;">1 × 10<sup>3</sup> kg/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>μ</em></span></td>
<td style="text-align: left;">Dynamic Viscosity</td>
<td style="text-align: left;">1 × 10<sup>-3</sup> Pas</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>κ</em></span></td>
<td style="text-align: left;">Intrinsic permeability</td>
<td style="text-align: left;">5 × 10<sup>-11</sup> m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>Φ</em></span></td>
<td style="text-align: left;">Soil porosity</td>
<td style="text-align: left;"><span class="math inline">0.5</span></td>
</tr>
</tbody>
</table>

### Botany

#### Water balance of the mangroves

<table>
<tablecaption align="top"><font size = "1"><i><b>Table 3:</b> Parameterization of the biotic factors</i></font></tablecaption>
<a name="Table_3"></a>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Species parameter</th>
<th style="text-align: left;">Value</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Leaf water potential</td>
<td style="text-align: left;">8.15 × 10<sup>6</sup> kg/s<sup>2</sup>/m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>f</em></sub></span></td>
<td style="text-align: left;">Xylem conductivity</td>
<td style="text-align: left;">1.04 × 10<sup>-10</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>L</em><sub><em>p</em></sub> ⋅ <em>k</em><sub><em>g</em><em>e</em><em>o</em></sub></span></td>
<td style="text-align: left;">Fine root permeability <span class="math inline">⋅</span> scaling factor</td>
<td style="text-align: left;">1.32 × 10<sup>-11</sup> kg/s/m<sup>4</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Maintenance cost per biomass</td>
<td style="text-align: left;">1.4 × 10<sup>-6</sup> kg/s/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>g</em><em>r</em><em>o</em><em>w</em><em>t</em><em>h</em></sub></span></td>
<td style="text-align: left;">Growth speed scaling</td>
<td style="text-align: left;">2.5 × 10<sup>-3</sup></td>
</tr>
</tbody>
</table>

#### Global weighting factors


<table>
<tablecaption align="top"><font size = "1"><i><b>Table 4:</b> Global weighting factor</i></font></tablecaption>
<a name="Table_4"></a>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Global weighting factor</th>
<th style="text-align: left;">Value</th>
</tr>
</thead>
<tbody>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>C</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Solar resource inputs</td>
<td style="text-align: left;">5 × 10<sup>-8</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>σ</em></span></td>
<td style="text-align: left;">First sigmoidal slope</td>
<td style="text-align: left;">1.5 × 10<sup>-2</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>σ</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Second sigmoidal slope</td>
<td style="text-align: left;">5 × 10<sup>-2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>ω</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Heigth growth scaling factor</td>
<td style="text-align: left;">0.5</td>
</tr>
</tbody>
</table>

#### Initial values of the geometrical characteristics of the mangrove seedlings

<table>
<tablecaption align="top"><font size = "1"><i><b>Table 5:</b> Initial value of the geometrical characteristics of the mangrove seedlings</i></font></tablecaption>
<a name="Table_5"></a>
<thead>
<tr class="header">
<th style="text-align: left;">Symbol</th>
<th style="text-align: left;">Geometric measure</th>
<th style="text-align: left;">Value</th>
</tr>
</thead>
<tbody>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Root radius</td>
<td style="text-align: left;">0.26 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Crown radius</td>
<td style="text-align: left;">0.2 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stem radius</td>
<td style="text-align: left;">0.005 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Root depth</td>
<td style="text-align: left;">0.004 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Crown depth</td>
<td style="text-align: left;">0.004 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stem heigth</td>
<td style="text-align: left;">0.015 m</td>
</tr>
</tbody>
</table>

# Runtime [Arbeitstitel]

For representing the mangroves in the model area, it is necessary to establish a stable population, which means to reach quasi-stationary conditions. For this purpose, 30 mangroves are randomly positioned in the model area as seedlings. In each time step (length: half a year), 30 new mangroves are added, which are also randomly positioned in the model area. Due to the competition-based tree growth model, these new mangroves die more or less quickly. Thus, the probability that a young mangrove in the catchment area of an already older one dies again very quickly is very high. The reason for this is the above-ground competition, especially the lack of sunlight. Due to the concentration of salinity, caused by extraction of fresh water from the other mangroves, salt plumes are formed in the pore water. These provide worse growth conditions for the mangroves in downstream (especially for young mangroves).

# Results

The following visualization shows the dynamic development of the mangrove population in the model area and the development of the biomass. The increasingly stable mangrove population can be clearly seen over the first 100 time steps. Areas form relatively quickly over the x-length of the transect, in which large and thus very old mangroves grow, and those in which young mangroves quickly die again.


<figure id="vis">
<a name="Visualisierung_1"></a>
<form oninput="x.value=parseInt(a.value)" id="slider" >
<script type="text/javascript">
 /*<![CDATA[*/
  document.getElementById("slider").addEventListener("input", aktualisiere);
   function aktualisiere() {
	  var TS = (document.querySelector("output[name=x]")) ;
	  var a = '/pictures/exmouth_gulf/TS/ts_'+TS.value+'.png' ;
          document.getElementById("abb").setAttribute("src", a) ;
}
</script>
<img src="/pictures/exmouth_gulf/TS/ts_0.png" id="abb">
</br>
</br>
<p align="left">
<font size = "6">&nbsp;  Timestep:&nbsp;&nbsp;&nbsp;&nbsp; </font>
  <input type="range" id="a" min="0" max="1670" value="0"> &nbsp;
<font size = "6">  <output name="x" for="a">0</output> </font>&nbsp;&nbsp;
</p>
</figure>
<figcaption><font size = "1"><i><b>Visualization 1:</b> Dynamic evolution of the mangrove population over the modeling period.</i></font></figcaption>
<p>

<!--
<p>
<input type="button" value="click to go fullscreen" onclick="toggleFullScreen()">
</p>

<script type="text/javascript">
 /*<![CDATA[*/
function toggleFullScreen() {
  if ((document.fullScreenElement && document.fullScreenElement !== null) ||    
   (!document.mozFullScreen && !document.webkitIsFullScreen)) {
    if (document.documentElement.requestFullScreen) {  
      document.documentElement.requestFullScreen();  
    } else if (document.documentElement.mozRequestFullScreen) {  
      document.documentElement.mozRequestFullScreen();  
    } else if (document.documentElement.webkitRequestFullScreen) {  
      document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);  
    }  
  } else {  
    if (document.cancelFullScreen) {  
      document.cancelFullScreen();  
    } else if (document.mozCancelFullScreen) {  
      document.mozCancelFullScreen();  
    } else if (document.webkitCancelFullScreen) {  
      document.webkitCancelFullScreen();  
    }  
  }  
}

</script>
-->


The following video shows the dynamic development of the biomass in the entire model area and in individual sections. The formation of different zones of different growth height and individual density within the mangrove forest can be clearly seen here.

Test mit youtube, SimpleTest:

<iframe width="560" height="315" src="https://www.youtube.com/embed/rtIQ-Zg-t_M" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


<br>
<br>
<br>

Test mit Vimeo:

<br>
<br>
<br>


<iframe src="https://player.vimeo.com/video/481362688" width="640" height="360" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>





<br>
<br>
<br>

The results of the "<b>Full Model</b>" are in qualitative agreement with the measured field data (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4</a>). This is true for both the tree height profile (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 A</a>) and for the pore water salinity profile (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 B</a>) in the studied transect. In particular, the variation in pore water salinity was well mapped (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 A</a>). A comparison of the results of the "Full Model" with the results of the two model variants "Model Without Feedback" and "Model Without Tide" shows a significantly worse reproduction of the measured field data by the two simpler models (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 C and 4 D</a>).


<figure>
<a name="Figure_4"></a>
<img src="/pictures/exmouth_gulf/Figure_3.png">
<figcaption><font size = "1"><i><b>Figure 4:</b> Results</i></font></figcaption>
</figure><p>

The "Treatment Averages" plotted in <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4</a> are two areas where mangroves growing have been long term studied in more detail. A comparison of the results of these observations with the modeling results also shows a high degree of agreement.

In order to investigate the effects of taking into account the temporal dynamics of tides and plant water extraction on the salinity in the pore water, this effect was normalized using the following formula:

<figure>
<div align="center">
<img src="/pictures/exmouth_gulf/formel.png" width="50%">
</div>
</figure><p>

These relative effects are shown in the following <a href="/docs/sample_setup_exmouth_gulf/model_results/#Figure_5">Figure 5</a> for tree height and pore water salinity. A value of zero would mean that there is no difference in results between Full Model and the respective simplified model type. The larger the value becomes, the higher the deviation.

<figure>
<a name="Figure_5"></a>
<img src="/pictures/exmouth_gulf/Figure_3_2.png">
<figcaption><font size = "1"><i><b>Figure 5:</b> Relative impact of not considering tidal range ("Model Wihtout Tide") and plant water extraction ("Model Without Feedback").</i></font></figcaption>
</figure><p>

Due to the greater effects of the tidal range in the area close to the see, the model "<b>Without Tide</b>" can only represent the tree heights and the pore water salinity here with a relatively large deviation compared to the "<b>Full Model</b>". However, with further moving towards the mainland, the water level fluctuations due to tides become smaller. Tree heights and salinities can be represented in this range (x > 75 m) with smaller relative deviations from the "<b>Full Model</b>".

The Model "<b>Without Feedback</b>" has problems mapping mangrove growth height as the "<b>Full Model</b>" does, especially in the middle to landward area <pre>(60 m < x < 165 m) </pre> of the transect. 

!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Conclusion

The "<b>Full Model</b>" was used to represent the structure typical of mangrove forests. The measured field data and modeled values are within the variability of the field observations. MANGA is capable of doing this without further calibration of plant-specific parameters. The "<b>Full Model</b>" was able to identify areas in the model area where either tidal or vegetation significantly influences structural properties. 

Based on the results of the modeling, it must be assumed that a correct representation of mangrove growth with MANGA is only possible if the tidal range and the influences of mangrove water extraction from the subsurface are taken into account. The gradients of salinity in groundwater caused by plant water extraction significantly affect the growth dynamics of the mangrove population.
