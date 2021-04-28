---
title: "The Model"
linkTitle: "The Model"
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

As already described in the <a href="/docs/sample_model_exmouth_gulf/exmouth_gulf/">introductory chapter</a>, there are numerous mangrove forests in the Exmouth Gulf.
With the help of MANGA, the growth dynamics of the mangroves are reproduced in a model.
The main focus is on the structure typical for mangrove forests and the dominance of individual mangrove species under different site conditions.
In addition to the growth behavior of the mangroves, the salinity of the porewater - also as a sensitive parameter influencing growth - is considered in more detail.
In this context the interacting influences of mangrove growth and gradients of salinity in porewater are also considered.
This chapter describes the composition of the model, the basics of modeling with MANGA, and the results of the study.

<h1>Model Domain</h1>

A 185 m long and 10 m wide transect is represented in the model (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_1">Figure 1</a>). Allometry data from a transect measurements, as well as measurement results from a long-term study, are used to evaluate the model results. The long-term study documents the effects of fertilization on the growth of 72 mangroves, half of them are located on the landward and half of them on the seaward side of the transect (see also <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4</a>).

<br>
<figure>
<a name="Figure_1"></a>
<img src="/pictures/exmouth_gulf/Transect_Sketch.png">
<figcaption><font size = "1"><i><b>Figure 1:</b> Diagram of model abstraction from site conditions in the Exmouth Gulf</i></font></figcaption>
</figure><br>

The model shows the mangrove growth at the location in the Exmouth Gulf shown in the following figure.

<br>
<p>
<iframe src="https://www.google.com/maps/d/embed?mid=1EiX5yyZGJgVSu7pueUi5_jK160ndg0tG" width="640" height="480"></iframe>
</p>
<br>

Elevation profiles from the digital elevation model of the five transects (<a href="/en/docs/example-model_exmouth_gulf/results/#Figure_2">Figure 2 A</a>) were overlaid and the top of the terrain from the five signals (<a href="/en/docs/example_exmouth_gulf/results/#Figure_2">Figure 2 B</a>) was interpolated from the baseline of the signals.
This DEM was used for descretization of the groundwater model (<a href="/en/docs/example_exmouth_gulf/results/#Figure_2">Figure 2 C</a>).

<br>
<figure>
<a name="Figure_2"></a>
<img src="/pictures/exmouth_gulf/dem.png" style="width:75%">
<figcaption><font size = "1"><i><b>Figure 2:</b> Elevation profiles along transect lines</i></font></figcaption>
</figure><br>

<h1>Modeling</h1>

<h2>Model variants</h2>

Mangrove growth was simulated using three different models (see also <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_1">Table 1</a>). 

In the model "<b>Model Without Feedback</b>" the dynamic changes in abiotic influences (tides, groundwater recharge and salinity of seawater) are included via boundary conditions.
The influence of plant water extraction on porewater salinity was not accounted for.

The model "<b>Model Without Tide</b>" considers the effects of plant water extraction on the salinity of the porewater and all abiotic influences of the first model - with exception of the tides.

Finally, the third model variant "<b>Full Model</b>" reproduces both, the dynamics of tides and the coupling of plant water extraction and porewater.

The following <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_1">Table 1</a> summarizes the specifications of the three model variants.

<br>
<figure>
<figcaption align="top"><font size = "1"><i><b>Table 1:</b> Model variants</i></font></figcaption>
<a name="Table_1"></a>
<table width="100%">
 <tr>
  <td  width="27%" style="text-align: center; vertical-align: middle;">
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Tides
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Coupling plant water balance and porewater
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Other abiotic factors
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Model Without Feedback
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Model Without Tide
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="red" size="5"> <b> &#10008; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
 </tr>
 <tr>
  <td width="27%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
   Full Model
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="26%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
  <td width="23%" style="text-align: center; vertical-align: middle; border-left:1px solid #000; border-right:1px solid #000; border-top:1px solid #000; border-bottom:1px solid #000">
    <font color="green" size="5"> <b> &#10004; </b> </font>
  </td>
 </tr>
</table>
</figure><br>

<h2>Discretization</h2>

<h3>Groundwater model</h3>

The groundwater model represents the subsurface with a grid of dimensions of 10 m x 230 m x 3 m on five FEM layers with 5880 cells.
The following <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_2">Figure 2</a> shows the spatial discretization from the seaward perspective.

<br>
<figure>
<a name="Figure_2"></a>
<img src="/pictures/exmouth_gulf/dis.png">
<figcaption><font size = "1"><i><b>Figure 2:</b> Spatial discretization of the groundwater model</i></font></figcaption>
</figure><br>

The mangroves extract soil water from the subsurface from a depth of 40 cm to 80 cm below the ground surface.
<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_3">Figure 3</a> shows the model area (gray) and the area of water extraction by the mangroves (blue).
Note the 50-fold vertical scaling.

<br>
<figure>
<a name="Figure_3"></a>
<img src="/pictures/exmouth_gulf/model_area_legend.png">
<figcaption><font size = "1"><i><b>Figure 3:</b> Area of water extraction by mangroves</i></font></figcaption>
</figure><br>

The groundwater model is discretized in time with a step length of one hour.
The tidal range as a dynamic boundary condition is represented with the time series of the years 1991 to 1993, which is set in loops over the entire model runtime.

<h3>Tree growth model</h3>

Since each mangrove is represented as a single individual, there is no real spatial discretization.
Temporally, the tree growth model is discretized with a time step length of half a year (1&nbsp;a&nbsp;=&nbsp;365.25&nbsp;d).

<h2>Boundary conditions groundwater model</h2>

The salinity of the seawater was set at 50 g/kg, the pore water at the landward end of the transect was assigned a salinity of 70 g/kg.
The transpiration of the mangroves locally increases the salinity.
The water level is determined in terms of hydrostatic pressure at the seaward and landward ends of the model area.
In order to represent the tides, the lake-side water level was integrated into the model as a dynamic Dirichlet boundary condition.
The water level measurements of the Department of Transport of the Government of Western Australia served as data basis.
The land-based water level is represented by a constant Dirichlet boundary condition.
Evaporation of the trees is integrated by sink terms in the area of the roots (see also <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_3">Figure 3</a>).
Inflow in the form of precipitation is indirectly considered via salinity at the landward edge of the model area.
The model boundaries which are not mentioned explicitly, are all defined as no flow boundary conditions.
<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_1">Figure 1</a> shows a schematic diagram of this.


<h2>Parameterization</h2>

The following tables show the parameterizations of the subsurface (<a href="/docs/sample_model_exmouth_gulf/model_results/#Table_2">Table 2</a>) and the mangroves (<a href="/docs/sample_model_exmouth_gulf/model_results/#Table_3">Table 3</a>), global weighting factors (<a href="/docs/sample_model_exmouth_gulf/model_results/#Table_4">Table 4</a>), and the initial values of the geoemtries of the mangrove seedlings (<a href="/docs/sample_model_exmouth_gulf/model_results/#Table_5">Table 5</a>).

<h3>Subsurface</h3>

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
<td style="text-align: left;">1&nbsp;×&nbsp;10<sup>-9</sup> m<sup>2</sup>/s</td>
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
<td style="text-align: left;">1&nbsp;×&nbsp;10<sup>3</sup> kg/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>μ</em></span></td>
<td style="text-align: left;">Dynamic Viscosity</td>
<td style="text-align: left;">1&nbsp;×&nbsp;10<sup>-3</sup> Pas</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>κ</em></span></td>
<td style="text-align: left;">Intrinsic permeability</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-11</sup> m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>Φ</em></span></td>
<td style="text-align: left;">Soil porosity</td>
<td style="text-align: left;"><span class="math inline">0.5</span></td>
</tr>
</tbody>
</table>

<h3>Botany</h3>

<h4>Water balance of the mangroves</h4>

<table>
<tablecaption align="top"><font size = "1"><i><b>Table 3:</b> Parameterization of the biotic factors</i></font></tablecaption>
<a name="Table_3"></a>
<thead>
<tr class="header">
<th width="10%" style="text-align: left;">Symbol</th>
<th width="40%" style="text-align: left;">Species parameter</th>
<th width="25%" style="text-align: left;">Avicennia marina</th>
<th width="25%" style="text-align: left;">Rhizophora mangle </th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>D</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Leaf water potential</td>
<td style="text-align: left;">-8.15&nbsp;×&nbsp;10<sup>6</sup> kg/s<sup>2</sup>/m</td>
<td style="text-align: left;">-6.45&nbsp;×&nbsp;10<sup>6</sup> kg/s<sup>2</sup>/m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>f</em></sub></span></td>
<td style="text-align: left;">Xylem conductivity</td>
<td style="text-align: left;">1.04&nbsp;×&nbsp;10<sup>-10</sup> kg/s/m<sup>2</sup></td>
<td style="text-align: left;">3.12&nbsp;×&nbsp;10<sup>-10</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>L</em><sub><em>p</em></sub> ⋅ <em>k</em><sub><em>g</em><em>e</em><em>o</em></sub></span></td>
<td style="text-align: left;">Fine root permeability ⋅  scaling factor</td>
<td style="text-align: left;">1.32&nbsp;×&nbsp;10<sup>-11</sup> kg/s/m<sup>4</sup></td>
<td style="text-align: left;">1.32&nbsp;×&nbsp;10<sup>-11</sup> kg/s/m<sup>4</sup></td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>m</em></sub></span></td>
<td style="text-align: left;">Maintenance cost per biomass</td>
<td style="text-align: left;">1.4&nbsp;×&nbsp;10<sup>-6</sup> kg/s/m<sup>3</sup></td>
<td style="text-align: left;">1.4&nbsp;×&nbsp;10<sup>-6</sup> kg/s/m<sup>3</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>k</em><sub><em>g</em><em>r</em><em>o</em><em>w</em><em>t</em><em>h</em></sub></span></td>
<td style="text-align: left;">Growth speed scaling</td>
<td style="text-align: left;">3.5&nbsp;×&nbsp;10<sup>-3</sup></td>
<td style="text-align: left;">3.5&nbsp;×&nbsp;10<sup>-3</sup></td>
</tr>
</tbody>
</table>

<h4>Global weighting factors</h4>

<table>
<tablecaption align="top"><font size = "1"><i><b>Table 4:</b> Global weighting factor</i></font></tablecaption>
<a name="Table_4"></a>
<thead>
<tr class="header">
<th width="10%" style="text-align: left;">Symbol</th>
<th width="40%" style="text-align: left;">Global weighting factor</th>
<th width="25%" style="text-align: left;">Avicennia marina</th>
<th width="25%" style="text-align: left;">Rhizophora mangle </th>
</tr>
</thead>
<tbody>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>C</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Solar resource inputs</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-8</sup> kg/s/m<sup>2</sup></td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-8</sup> kg/s/m<sup>2</sup></td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>σ</em></span></td>
<td style="text-align: left;">First sigmoidal slope</td>
<td style="text-align: left;">1.5&nbsp;×&nbsp;10<sup>-2</sup></td>
<td style="text-align: left;">1.5&nbsp;×&nbsp;10<sup>-2</sup> </td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>σ</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Second sigmoidal slope</td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-2</sup></td>
<td style="text-align: left;">5&nbsp;×&nbsp;10<sup>-2</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>ω</em><sub><em>h</em></sub></span></td>
<td style="text-align: left;">Heigth growth scaling factor</td>
<td style="text-align: left;">0.12</td>
<td style="text-align: left;">0.12</td>
</tr>
</tbody>
</table>

<h4>Initial values of the geometrical characteristics of the mangrove seedlings</h4>

<table>
<tablecaption align="top"><font size = "1"><i><b>Table 5:</b> Initial value of the geometrical characteristics of the mangrove seedlings</i></font></tablecaption>
<a name="Table_5"></a>
<thead>
<tr class="header">
<th width="10%" style="text-align: left;">Symbol</th>
<th width="40%" style="text-align: left;">Geometric measure</th>
<th width="25%" style="text-align: left;">Avicennia marina</th>
<th width="25%" style="text-align: left;">Rhizophora mangle </th>
</tr>
</thead>
<tbody>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Root radius</td>
<td style="text-align: left;">0.25 m</td>
<td style="text-align: left;">0.25 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>C</em></sub></span></td>
<td style="text-align: left;">Crown radius</td>
<td style="text-align: left;">0.3 m</td>
<td style="text-align: left;">0.3 m</td>
</tr>
<tr class="even">
<td style="text-align: left;"><span class="math inline"><em>r</em><sub><em>S</em></sub></span></td>
<td style="text-align: left;">Stem radius</td>
<td style="text-align: left;">0.01 m</td>
<td style="text-align: left;">0.01 m</td>
</tr>
<tr class="odd">
<td style="text-align: left;"><span class="math inline"><em>h</em><sub><em>R</em></sub></span></td>
<td style="text-align: left;">Root depth</td>
<td style="text-align: left;">0.015 m</td>
<td style="text-align: left;">0.015 m</td>
</tr>
</tbody>
</table>

<h1>Resource competition</h1>

For representing the mangroves in the model area, it is necessary to establish a stable population, which means to reach quasi-stationary conditions.
For this purpose, 30 mangroves are randomly positioned in the model area as seedlings.
In each time step (length: half a year), 30 new mangroves are added, which are also randomly positioned in the model area.
Due to the competition-based tree growth model, these new mangroves die more or less quickly.
Thus, the probability that a young mangrove in the catchment area of an already older one dies again very quickly is very high.
The reason for this is the above-ground competition, especially the lack of sunlight.
Due to the concentration of salinity, caused by extraction of fresh water from the other mangroves, salt plumes are formed in the pore water.
These lead to growth penalties for the mangroves located downstream (especially for young mangroves).
Different mangrove species have varying tolerance to high salt concentrations.
In this research, the two species Avicennia marina ("gray mangrove") and Rhizophora mangle ("red mangrove") were studied in more detail.

<h1>Results</h1>

In this research, two processes were viewed more closely with the help of the MANGA model.
On the one hand, the development of typical structures in mangrove forests is be mapped, on the other hand, the growth behavior of the two mangrove species under different environmental conditions is investigated.
In the following the results of the research are briefly summarized.

<h2>Forest structure</h2>

The following visualization shows the dynamic development of the mangrove population in the model area and the development of the biomass.
The increasingly stable mangrove population can be clearly seen in the first 100 time steps.
Over the X-length of the transect are relatively quickly building areas in which large and thus very old mangroves grow, and areas in which young mangroves quickly die again.
Due to the fact that 30 new mangroves are added to the model as seedlings in each time step and the nutrient competition is initially very low, the biomass in the model initially grows very strongly.
As the number of mangroves in the model area increases, the competition between individual trees increases, too.
After the global maximum of the biomass, the biomass decreases slightly due to worsening nutrient conditions for some mangroves.
After a certain time, a quasi-stationary state of the mangrove population is reached.

<br>
<figure id="vis">
<a name="Visualisierung_1"></a>
<form oninput="x.value=parseInt(a.value)" id="slider" >
<script type="text/javascript">
 /*<![CDATA[*/
  document.getElementById("slider").addEventListener("input", aktualisiere);
   function aktualisiere() {
	  var TS = (document.querySelector("output[name=x]")) ;
	  var a = '/pictures/exmouth_gulf/TS/ts_'+TS.value+'.png' ;
          document.getElementById("abb").setAttribute('src', a) ;
}
/*]]>*/
</script>
<img src='/pictures/exmouth_gulf/TS/ts_0.png' id="abb">
</br>
</br>
<p align="left">
<font size = "6">&nbsp;  Timestep:&nbsp;&nbsp;&nbsp;&nbsp; </font>
  <input type="range" id="a" min="0" max="1650" step="50"> &nbsp;
<font size = "6">  <output name="x" for="a">0</output> </font>&nbsp;&nbsp;
</p>
</figure>
<figcaption><font size = "1"><i><b>Visualisation 1:</b> Dynamic development of the mangrove population over the modeling period</i></font></figcaption>
<br>

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

In the following video the model area was divided into ten sectors.
The dynamic development of the mangrove population and the salt concentration in the bottom water as well as the biomass of the mangroves in the individual sectors are shown.
Compared to the previous visualization, one main cause of the formation of the typical forest structure can be seen in this video, namely the concentration of salinity in the pore water in certain areas.
The high correlation between salt concentration and biomass in the individual sectors can be seen already from a model runtime of 40 years.
Already from 100 years, the structure of typical mangrove forests is recognizable.

<br>
<figure>
<iframe src="https://player.vimeo.com/video/481362688" width="640" height="360" frameborder="1" allow="autoplay; fullscreen" allowfullscreen></iframe>
<figcaption><font size = "1"><i><b>Video 1:</b> Dynamic development of mangrove population and salinity concentration in porewater over the modeling period.</i></font></figcaption>
</figure><br>

The results of the "<b>Full Model</b>" are in qualitative agreement with the measured field data (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4</a>).
This is true for both the tree height profile (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 A</a>) and for the porewater salinity profile (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 B</a>) in the studied transect.
In particular, the variation in porewater salinity was well mapped (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 A</a>).
The coefficient of determination of the Bravais-Pearson correlation is R²&nbsp;=&nbsp;0.64 for tree height and R²&nbsp;=&nbsp;0.88 for porewater salinity.
A comparison of the results of the "<b>Full Model</b>" with the results of the two model variants "<b>Model Without Feedback</b>" and "<b>Model Without Tide</b>" shows a significantly worse reproduction of the measured field data by the two simpler models (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4 C and 4 D</a>).

<br>
<figure>
<a name="Figure_4"></a>
<img src="/pictures/exmouth_gulf/Figure_3.png">
<figcaption><font size = "1"><i><b>Figure 4:</b> Simulated and measured mangrove stand properties along transect</i></font></figcaption>
</figure><br>

The "Treatment Averages" plotted in <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_4">Figure 4</a> are from mangroves that have been studied in more detail in long-term experiments.
A comparison of the results of these observations with the modeling results also shows a high degree of agreement.

In order to investigate the effects of the temporal dynamics of tides and plant water extraction on the salinity in the pore water, this effect was normalized using the following formula:

<br>
<figure>
<div align="center">
<img src="/pictures/exmouth_gulf/formel.png" width="50%">
</div>
</figure><br>

These relative effects are shown in the following <a href="/docs/sample_setup_exmouth_gulf/model_results/#Figure_5">Figure 5</a> for tree height and porewater salinity.
A value of zero would mean that there is no difference in results between Full Model and the respective simplified model type.
The larger the value becomes, the higher the deviation.

<br>
<figure>
<a name="Figure_5"></a>
<img src="/pictures/exmouth_gulf/Figure_3_2.png">
<figcaption><font size = "1"><i><b>Figure 5:</b> Relative impact of not considering tidal range ("Model Wihtout Tide") and plant water extraction ("Model Without Feedback").</i></font></figcaption>
</figure><br>

Due to the greater effects of the tidal range in the area close to the sea, the model "<b>Without Tide</b>" can only represent the tree heights and the porewater salinity here with a relatively large deviation compared to the "<b>Full Model</b>".
However, with further inlands, the water level fluctuations due to tides become smaller.
Tree heights and salinities can be represented in this range (x > 75 m) with smaller relative deviations from the "<b>Full Model</b>".

The Model "<b>Without Feedback</b>" fails to predict mangrove growth height as the "<b>Full Model</b>" does, especially in the middle to landward area (60 m < x < 165 m) of the transect. In this area the salinity of the porewater is concentrated by the plant water extraction, but this is not represented in this type of model.

<h2>Species dominance</h2>

In the previous section, it was shown that MANGA, with the consideration of salinity in the bottom water and the tidal range, is able to represent the forest structures typical for mangrove forests.
Using the extensive parameterization capabilities of the tree growth model (see also the section <a href="/docs/sample_setup_exmouth_gulf/model_results/#Parametrization">parametrization</a>), MANGA can also be used to study the growth of single specific individual species.
For example, different mangrove species have different tolerances to excessive salinity.
In this project, the growth behavior of two species, Avicennia marina and Rhizophora mangle, was studied in more detail.

<a href="/docs/sample_setup_exmouth_gulf/model_results/#Figure_6">Figure 6</a> shows the species dominance of these two mangrove species at different salinity concentrations (see <a href="/docs/sample_setup_exmouth_gulf/model_results/#Table_6">Table 6</a>) in porewater.
The different setups shown in the figure differ only with respect to the boundary conditions of the seaward and landward salinity concentrations of the porewater.
For the consideration of species dominance in the model domain, we introduce the species dominance d and define it as follows:

<br>
<figure style="width:75%">
<div align="center">
<img src="/pictures/exmouth_gulf/formel_normierung_speziendominanz_2.jpg" style="width:70%">
</div>
</figure><br>

Here, V<sub>i</sub>(x,t) represent the volume of mangrove species Rhizophora mangle (V<sub>Rhi</sub>(x,t)) and Avicennia marina (V<sub>Avi</sub>(x,t)) present at the time step (t) and X coordinate (x).

<br>
<table>
<tablecaption align="top"><font size = "1"><i><b>Table 6:</b> Setup configuration</i></font></tablecaption>
<a name="Table_6"></a>
            <tr>
                <th>Setup</th>
                <td style="text-align: center;">A</td>
		<td style="text-align: center;">B</td>
		<td style="text-align: center;">C</td>
                <td style="text-align: center;">D</td>
		<td style="text-align: center;">E</td>
		<td style="text-align: center;">F</td>
            </tr>
            <tr>
                <th>seeward salinity [g/kg]</th>
                <td>15</td>
		<td>15</td>
		<td>25</td>
                <td>50</td>
		<td>50</td>
		<td>35</td>
            </tr>
            <tr>
                <th>landward salinity [g/kg]</th>
                <td>25</td>
		<td>40</td>
		<td>55</td>
                <td>60</td>
		<td>45</td>
		<td>35</td>
            </tr>
</table>

<br>
<figure>
<a name="Figure_6"></a>
<img src="/pictures/exmouth_gulf/Spezien_1.png" style="width:75%">
<figcaption><font size = "1"><i><b>Figure 6:</b> Resulting simulated forest properties from all simulated setups presented in dependence on established porewater salinity</i></font></figcaption>
</figure><br>

<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6A to 6D</a> show an initially monospecific Rhizophora forest (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6A</a>) due to both seaward and landward low salinity concentrations.
As salinity increases, a mixed forest of both species is established (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6B and 6C</a>). <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6D</a> then depicts a monospecific Avicennia marina forest due to the high salt concentrations.
Both <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6E and 6F</a> are similar to setup configurations <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6B and 6C</a> in that the values of salinities on landward and seaward sides of the transect, respectively, assume approximately the other value.
Thus, they too represent a mixed forest of both species.
These results are shown again in a different way in the following <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_7">Figure 7</a>.

<br>
<figure>
<a name="Figure_7"></a>
<img src="/pictures/exmouth_gulf/Spezien_2.png" style="width:75%">
<figcaption><font size = "1"><i><b>Figure 7:</b> Dependence of species dominance on landward (x-axis) and seaward (y-axis) salinity.</i></font></figcaption>
</figure><br>

When looking at the mixed forests, real mixed populations are existing only in a few individual sections.
In most areas a clear dominance of one species is expressed.
These sharp transitions between the individual dominance zones show that coexistence between the different species is only possible in areas of certain pore water salinities.
The location of the boundaries and the change in species dominance d (slope of the curve) depend on the individual-specific parameters in the tree growth model.
Soil water salinity is also affected by the number of individuals per area and tree heights.
These two parameters are in turn influenced by the same individual-specific parameters.

Consequently, the coupling between plant water balance and porewater significantly influences the formation of forest structure.
In the setups that result to the formation of a mixed forest, either two-zone (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6C and 6E</a>) or three-zone (<a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_6">Figure 6B and 6F</a>) mixed forests are formed.
The two zones at the seaward and landward end of the model are mainly controlled by the parameters of salinity as boundary condition.
In the model center, the transpiration of the mangroves leads to a concentration of the porewater salinity.
If this exceeds a certain value, the more salt-resistant species Avicennia marina dominates.

As also shown in <a href="/docs/sample_model_exmouth_gulf/model_results/#Figure_8">Figure 8</a>, the results of considering species dominance in the model are consistent with the measured field data in those transects considered in the project.

<br>
<figure>
<a name="Figure_8"></a>
<img src="/pictures/exmouth_gulf/Spezien_3.png" style="width:75%">
<figcaption><font size = "1"><i><b>Figure 8:</b> Resulting simulated forest properties from all simulated setups presented in dependence on established porewater salinity</i></font></figcaption>
</figure><br>

Consequently, the MANGA model software is able to represent not only the evolving structure of a mangrove forest, but also its composition of different species.

<h1>Conclusion</h1>

With "<b>Full Model</b>" the structure which is typical for mangrove forests can be modeled.
Specifically, the forest structure of the Avicennia marina monoculture forest in the considered area in the Exmouth Gulf in Western Australia could be reproduced in a consistent manner with the available field data.
Variations in tree heights and soil water salinity between model and measured values are within the range of variability in field measurements.
MANGA is capable of doing this without further calibration of plant-specific parameters.
The "<b>Full Model</b>" was able to identify areas in the model area where either tides or vegetation significantly influence structural properties. 

Based on the results of the modeling, it must be assumed that a correct representation of mangrove growth with MANGA is only possible if the tidal range and the influences of water extraction of the mangroves from the subsurface are considered.
Calibration of the plant parameters is not necessary for this purpose.
Also not considered are heterogeneous hydrogeological properties of the subsurface, e.g. concerning hydraulic conductivity or porosity. 

The gradients of the salt concentration in the porewater caused by the plant water extraction have a significant effect on the growth dynamics of the mangrove population, especially in the landward area.
Further, it can be concluded from the results that the influence of tides is a major influencing factor on the gradients of salinity concentration in bottom water.
This influence is greatest at the seaward end of the transect.
As the height of the tide decreases, or the duration of inundation decreases, the feedback between plant water and bottom water budgets takes on increasing importance in this process.

Using the sensitivity analysis of the model with respect to species dominance, it was shown that species composition can be described by considering soil water balance and plant water withdrawal across the system boundary.
By variation of just two parameters (see <a href="/docs/sample_model_exmouth_gulf/model_results/#Table_3">Table 3</a>) that directly affect tree water uptake, typical zonation patterns in mixed mangrove forests could be reproduced.
This was accomplished even with roughly estimated plant-specific parameters for one of the two species.
If the boundary conditions of the salt concentrations on the land- and seaward side are both chosen very high or very low, monoculture forests are formed.
If a moderate mean value of the salinities is chosen, mixed forests of both species are formed.
These show zones with clear dominance of one species, separated by sharp transitions.
These transitions are shown to depend on the porewater salinity.
The species composition in the model agrees with the measured field data.

<h1>Outlook</h1>

There is evidence in the literature that mangroves adapt to their environmental conditions over time.
A lower salt concentration in the bottom water provides higher xylem conductance and thus greater transpiration.
At the same time, however, a low salt concentration in the subsurface also provides higher leaf water potentials that inhibit transpiration.
These mutually balancing processes provide approximately constant transpiration rates at different porewater salinities.
A more detailed study of these processes may help to understand the ability of mangroves to adapt their physiology to appropriate sites prevailing environmental conditions.

Precipitation was not dynamically integrated as a separate process in this project, as still described, but is represented by the land-based constant boundary condition of water level and salinity.
The Exmouth Gulf is generally a region of very low annual precipitation sums.
However, the variability of individual rainfall events is very high.
Due to cyclones, heavy rainfall events occur regularly and account for a not insignificant portion of the total precipitation.
The influence of precipitation on the mangrove population was studied indirectly by setting different values of the boundary condition of landward porewater salinity.
Since this boundary condition was shown to be a very sensitive variable, it follows that precipitation also has an influence on mangrove species composition and, in general, the formation of typical mangrove forest structures.
In the course of climate change, it can be assumed that heavy rainfall events or generally extreme weather situations will increase and that sea level will rise.
Since the model was able to represent the populations according to reality, it could also be used to investigate the effects of climate change on the sensitive ecosystems of the mangrove forests.
Further, the model can provide important clues in the study of all relationships between forest structures and plant characteristics.
Models that represent the processes based on more conceptual approaches than MANGA can be calibrated and verified with MANGA.
