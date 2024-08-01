from ResourceLib import ResourceModel
from ResourceLib.BelowGround.Network.Network import Network
from ResourceLib.BelowGround.Network.NetworkFixedSalinity import NetworkFixedSalinity
from ResourceLib.BelowGround.Individual.SaltFeedbackBucket import SaltFeedbackBucket


class NetworkSaltFeedbackBucket(Network, SaltFeedbackBucket):
    """
    NetworkSaltFeedbackBucket below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        super(Network, self).__init__(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        # Use Network method
        super().prepareNextTimeStep(t_ini=t_ini, t_end=t_end)
        # Use SaltFeedbackBucket method
        super(Network, self).prepareNextTimeStep(t_ini=t_ini, t_end=t_end)

    def addPlant(self, plant):
        # Use Network method
        super().addPlant(plant=plant)

        # If below-ground resources does not yet exist for the plant, set
        # sink term to 0 (i.e., in the first timestep of a plant)
        try:
            gci = plant.getGrowthConceptInformation()
            plant_water_uptake = gci["bg_resources"]  # m³ water per time step
        except KeyError:
            plant_water_uptake = 0

        if self._r_root[-1] < self.mesh_size:
            #print("\t> Interpolate root radius")
            self._r_root[-1] = self.mesh_size

        self.calculatePlantSink(x=self._xe[-1], y=self._ye[-1], r_root=self._r_root[-1],
                                bg_resources=plant_water_uptake)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each plant based on pore-water salinity below the
        center of each plant and the exchange between grafted trees.
        Sets:
            numpy array of shape(number_of_trees)
        """
        # SaltFeedbackBucket start
        self.getBorderSalinity()
        self.getInflowSalinity()
        self.getInflowMixingRate()
        self.calculateCellSalinity()
        # SaltFeedbackBucket end

        # FixedSalinity start
        self.calculatePsiOsmo()
        # FixedSalinity end

        super().calculateBelowgroundResources()

    def calculatePsiOsmo(self):
        """
        Calculate osmotic water potential (Pa) in the soil based on pore water salinity.
        Sets:
            numpy array of shape(number_of_plants)
        """
        salinity_plant = super().getPlantSalinity()
        self._psi_osmo = -85000000 * salinity_plant

    def getInputParameters(self, args):
        tags1 = Network.getInputTags(self, args)
        tags2 = SaltFeedbackBucket.getInputTags(self, args)
        tags = {"prj_file": args,
                "required": list(set(tags1["required"] + tags2["required"])),
                "optional": list(set(tags1["optional"] + tags2["optional"]))}
        ResourceModel.getInputParameters(self, **tags)
        super().setInputParameters()

        if not hasattr(self, "exchange"):
            self.exchange = "on"
            print("> Set below-ground network parameter 'exchange' to default:", self.exchange)