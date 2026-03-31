# Description

This module calculates the growth (production of biovolume) of saltmarsh plants, e.g., grasses, shrubs and herbs.
The growth is calculated using a simple model based on resource limitation and competition.

# Usage

```xml
<population>
    <group>
        <vegetation_model_type> Saltmarsh </vegetation_model_type>
        <species> Saltmarsh </species>
    </group>
</population>
```

Go to [Examples](#examples) for more information.

# Attributes

- ``vegetation_model_type`` (string): "Saltmarsh" (no other values accepted)
- ``species`` (string): Path to file defining species or plant functional type (PFT). Possible Inputs: "Saltmarsh" (will use default saltmarsh species defined in `pyMANGA.PopulationLib.Species.Saltmarsh` or path to custom species file.)

# Value

Three dictionaries each with length = 1 (i.e., for each individual plant).

The dictionary ``geometry`` contains information about plant geometry.
The dictionary ``growth_concept_information`` contains information about plant growth concept.
The dictionary ``parameter`` contains the relevant parameters.

# Details
## Purpose

The purpose of this module is to describe the growth of saltmarsh plants based on resource limitation and competition.

## Plant geometry

Saltmarsh plants are represented as two cylinders:

* one above-ground (AG)
* one below-ground (BG)

Each cylinder is described by:

* radius ($r_{ag}$, $r_{bg}$)
* height ($h_{ag}$, $h_{bg}$)

From this, volumes are computed:

* Above-ground volume: $V_{ag}$ = $\pi \cdot r_{ag}^2 \cdot h_{ag}$
* Below-ground volume: $V_{bg}$ = $\pi \cdot r_{bg}^2 \cdot h_{bg}$
* Total volume: $volume = V_{ag} + V_{bg}$

## Process overview

- ``plantVolume``: calculates $V_{ag}$, $V_{bg}$, and $V_{total}$
- ``agResources``: computes available above-ground resources $res_{ag}$
- ``bgResources``: computes available below-ground resources $res_{bg}$
- ``plantMaintenance``: computes maintenance costs $maint$
- ``growthResources``: computes effective resources $res_{eff}$ and net growth $grow$
- ``plantGrowth``: allocates net growth to $V_{ag}$ and $V_{bg}$ and updates geometries ($r$, $h$)
- ``waterUptake``: computes transpiration

## Sub-processes

### Plant volume (``plantVolume``)

Above-ground volume ($V_{ag}$), below-ground volume ($V_{bg}$), total volume ($volume$) an the ratio between above-ground and below-ground volume are calculated from plant geometry:

$$
V_{ag} = \pi \cdot r_{ag}^{2} \cdot h_{ag} \\
$$
$$
V_{bg} = \pi \cdot r_{bg}^{2} \cdot h_{bg} \\
$$
$$
volume = V_{ag} + V_{bg} \\
$$
$$
r_{V_{ag,bg}} = \frac{V_{ag}}{V_{bg}}
$$

### Above-ground resources (``agResources``)

Available above-ground resources depend on the above-ground limitation factor <span style="white-space: nowrap;">($f_{reslim,ag} \in (0,1)$)</span>, plant above-ground radius <span style="white-space: nowrap;">($r_{ag}$)</span>, solar radiation <span style="white-space: nowrap;">($p_{sun}$)</span>, and the timestep length <span style="white-space: nowrap;">($\Delta t$)</span>:

$$
res_{ag} = f_{reslim,ag} \cdot \pi \cdot r_{ag}^{2} \cdot p_{sun} \cdot \Delta t
$$

### Below-ground resources (``bgResources``)

Available below-ground resources depend on the below-ground limitation factor <span style="white-space: nowrap;">($f_{reslim,bg} \in (0,1)$)</span>, plant geometry <span style="white-space: nowrap;">($r_{bg}, h_{bg}, h_{ag}$)</span>, solar radiation <span style="white-space: nowrap;">($p_{sun}$)</span>, water uptake efficiency parameter <span style="white-space: nowrap;">($p_{water}$)</span> and timestep length <span style="white-space: nowrap;">($\Delta t$)</span>:

$$
res_{bg} = f_{reslim,bg} \cdot \pi \cdot r_{bg}^{2} \cdot h_{bg} \cdot p_{sun} \cdot p_{water}
\cdot \left( h_{ag} + 0.5 \cdot h_{bg} \right)^{-1} \cdot \Delta t
$$

### Maintenance costs (``plantMaintenance``)

Maintenance costs <span style="white-space: nowrap;">($maint$)</span> are proportional to total biovolume <span style="white-space: nowrap;">($V_{total}$)</span> and scaled by the species-specific maintenance factor <span style="white-space: nowrap;">($p_{maint}$)</span>:

$$
maint = V_{total} \cdot p_{maint} \cdot \Delta t
$$

### Effective resources and net growth (``growthResources``)

The resources effectively available to the plant <span style="white-space: nowrap;">($res_{eff}$)</span> are given by the minimum of the above-ground and below-ground resources <span style="white-space: nowrap;">($res_{ag}$ and $res_{bg}$)</span>:

$$
res_{eff} = \min(res_{ag},\ res_{bg})
$$

Potential growth <span style="white-space: nowrap;">($grow_{pot}$)</span> is obtained using the species-specific growth factor <span style="white-space: nowrap;">($p_{grow}$)</span>:

$$
grow_{pot} = res_{eff} \cdot p_{grow}
$$

Subtracting maintenance costs <span style="white-space: nowrap;">($maint$)</span> from potential growth <span style="white-space: nowrap;">($grow_{pot}$)</span> yields the net growth or shrinkage <span style="white-space: nowrap;">($grow$)</span>:

$$
grow = grow_{pot} - maint
$$

If $grow$ is negative, the plant shrinks. In this case, it is additionally multiplied by the species- or PFT-specific dieback factor <span style="white-space: nowrap;">($p_{dieback}$)</span>:

$$
grow = grow \cdot p_{dieback} \quad \text{if} \ grow < 0
$$

### AG/BG allocation and biovolume update (``plantGrowth``)

#### If $grow > 0$

Net growth is allocated dynamically adjusted based on the relative limitation of AG vs BG.

The resource limitation ratio <span style="white-space: nowrap;">($ratio_{ag,bg}$)</span> is computed from the limitation factors <span style="white-space: nowrap;">($f_{reslim,ag}$ and $f_{reslim,bg}$)</span>:

$$
ratio_{ag,bg} = \frac{f_{reslim,ag}}{f_{reslim,ag} + f_{reslim,bg}}
$$

Since $f_{\mathrm{reslim},ag} \in (0,1)$ and $f_{\mathrm{reslim},bg} \in (0,1)$, it follows that $ratio_{ag,bg} \in (0,1)$.

A temporary adjustment factor <span style="white-space: nowrap;">($Ad$)</span> is defined as:

$$
f_{ad} = 0.5 - ratio_{ag,bg}
$$

Thus:

$$
f_{ad} \in (-0.5,\ 0.5)
$$

The allocation weight <span style="white-space: nowrap;">($w_{ratio_{ag,bg}}$)</span> is then obtained by multiplying the species-specific baseline allocation parameter <span style="white-space: nowrap;">($p_{ratio_{ag,bg}}$)</span> by the adjustment factor $1 - f_{ad}$ :

$$
w_{ratio_{ag,bg}} = p_{ratio_{ag,bg}} \cdot (1 - f_{ad})
$$

Net growth is then split as:

$$
\Delta V_{bg} = grow \cdot w_{ratio_{ag,bg}}
\qquad \text{and} \qquad
\Delta V_{ag} = grow \cdot (1 - w_{ratio_{ag,bg}})
$$

#### If $grow \le 0$

The model symmetrically reduces AG and BG biovolume:

$$
\Delta V_{ag} = \Delta V_{bg} = \frac{grow}{2}
$$

### Volume update and geometry recalculation (``plantGrowth``)

$$
V_{ag} = V_{ag} + \Delta V_{ag}
\qquad \text{and} \qquad
V_{bg} = V_{bg} + \Delta V_{bg}
$$

Plant geometry is recalculated from updated compartment volumes with species specific shape parameters <span style="white-space: nowrap;">($p_{ratio\_ag}$ and $p_{ratio\_bg}$)</span> that define the ratio of radius to height for AG and BG cylinders, respectively:

$$
r_{ag} = p_{ratio\_{ag}} \cdot h_{ag}
\qquad \text{and} \qquad
r_{bg} = p_{ratio\_{bg}} \cdot h_{bg}
$$

With these fixed ratios, height is derived from cylinder volume:

$$
h_{ag} = \left( \frac{V_{ag}}{\pi \cdot p_{ratio\_{ag}}^{2}} \right)^{1/3}
\qquad \text{and} \qquad
h_{bg} = \left( \frac{V_{bg}}{\pi \cdot p_{ratio\_{bg}}^{2}} \right)^{1/3}
$$

Radii follow directly:

$$
r_{ag} = p_{ratio\_{ag}} \cdot h_{ag}
\qquad \text{and} \qquad
r_{bg} = p_{ratio\_{bg}} \cdot h_{bg}
$$

### Water uptake / transpiration (``waterUptake``)

Transpiration is computed proportional to total plant volume, species-specific transpiration factor <span style="white-space: nowrap;">($p_{transpiration}$)</span> and timestep length <span style="white-space: nowrap;">($\Delta t$)</span>:

$$
transpiration = V_{total} \cdot p_{transpiration} \cdot \Delta t
$$

## Application & Restriction

The saltmarsh module was tested satisfactorily in combination with the following modules:

- `pyMANGA.PopulationLib.Production.FixedRate`
- `pyMANGA.PopulationLib.Dispersal.Uniform`
- `pyMANGA.PopulationLib.InitialPop.FromFile`
- `pyMANGA.ResourceLib.Aboveground.AsymmetricZOI`
- `pyMANGA.ResourceLib.Belowground.Individual.FixedSalinity`
- `pyMANGA.ResourceLib.Belowground.Individual.SymmetricZOI`
- `pyMANGA.PlantModelLib.Mortality.Random`
- `pyMANGA.PlantModelLib.Mortality.Memory`
- `pyMANGA.PlantModelLib.Mortality.VolumeThreshold`
- `pyMANGA.PlantModelLib.Mortality.NoGrowth`
- all modules of `pyMANGA.ModelOutputLib` 

If it is combined with other modules, meaningful results cannot be guaranteed.

This plant module requires species files that contain the necessary parameters. Species files created for mangrove species e.g. cannot be used.


# References

coming soon

# Authors

Jonas Vollhüter, Selina Baldauf, Uta Berger, Ronny Peters, Marie-Christin Wimmler, Britta Tietjen.

# See Also

`pyMANGA.PopulationLib.Species.Saltmarsh`

# Examples

The following example defines a population of plants of the type $PFT\ 1$, whose species-specific parameterization is loaded from the corresponding file. While plant growth is simulated with the Saltmarsh vegetation model, mortality is controlled by the three simultaneously active concepts Memory, Random, and VolumeThreshold. The Memory concept is parameterized with a memory period of approximately one year <span style="white-space: nowrap;">($3.154 \cdot 10^7\ s$)</span>, the Random concept uses a mortality probability of $0.25$, and the VolumeThreshold concept removes individuals whose geometries fall below the in the species file defined thresholds. Individuals are distributed randomly within a $2\ m ×\ 2\ m$ domain, with an initial population size of $40$ individuals and a recruitment rate of $4$ new individuals per time step.

````xml
<population>
        <group>
            <name>Saltmarsh_1</name>
            <species>Benchmarks/ExampleSetups/Saltmarsh/PFTs/Saltmarsh_1.py</species>
            <vegetation_model_type>Saltmarsh</vegetation_model_type>
            <mortality>Memory Random VolumeThreshold</mortality>
            <period>3.154e+7*1</period>
            <threshold>0.05</threshold>
            <probability>0.25</probability>
            <domain>
                <x_1>0</x_1>
                <y_1>0</y_1>
                <x_2>2</x_2>
                <y_2>2</y_2>
            </domain>
            <initial_population>
                <type>Random</type>
                <n_individuals>40</n_individuals>
            </initial_population>
            <production>
                <type>FixedRate</type>
                <per_model_area>4</per_model_area>
            </production>
            <dispersal>
                <type>Uniform</type>
            </dispersal>
        </group>
</population>
````

Further examples can be found under `pyMANGA.Benchmarks.ExampleSetups.Saltmarsh`
