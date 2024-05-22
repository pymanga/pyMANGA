import pandas as pd
import numpy as np
from PopulationLib.Dispersal.Random import Random


class FromFile:
    """
    FromFile dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        self.xml_args = xml_args

    def getTags(self):
        """
        Return tags to search for in the project file
        Returns:
            dict
        """
        tags = {
            "prj_file": self.xml_args,
            "required": ["type", "filename", "domain", "x_1", "x_2", "y_1", "y_2"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def getInitialGroup(self):
        """
        Return positions and geometries of first plants in the model (i.e., the initial population).
        Returns:
            dict, np.array
        """
        plant_attributes_file = self.getPlantsFromFile()
        # Get parameters that are required for the selected plant module
        geometry_list, network_list = self.getGeometryList()
        geometry, network = {}, {}
        for geo in geometry_list:
            try:
                geometry[geo] = plant_attributes_file[geo].flatten()
            except KeyError:
                print("ERROR: geometry parameters in initial population do not match plant module.")
                exit()
        for net in network_list:
            try:
                network[net] = plant_attributes_file[net].flatten()
            except KeyError:
                print("ERROR: geometry parameters in initial population do not match plant module.")
                exit()
        positions = {"x": plant_attributes_file["x"].flatten(),
                     "y": plant_attributes_file["y"].flatten()}
        return positions, geometry, network

    def getGeometryList(self):
        """
        Return geometries associated with a certain plant module.
        Returns:
            list
        """
        # ToDo: Liste mit notwendigen Parametern irgendwoher holen?
        plant_model = self.xml_args.find("vegetation_model_type").text
        geometry_list, network_list = [], []
        if plant_model == "Default":
            # ToDo: Welche Geometrie soll für Default definiert werden? Anpassung Benchmarks&ini_pop.csv notwendig
            # geometry_list = ["r_ag", "h_ag", "r_bg", "h_bg"]
            geometry_list = ["r_stem", "h_stem", "r_crown", "r_root"]
        elif plant_model in ["Bettina"]:
            geometry_list = ["r_stem", "h_stem", "r_crown", "r_root"]
        elif plant_model in ["BettinaNetwork"]:
            geometry_list = ["r_stem", "h_stem", "r_crown", "r_root"]
            network_list = ["partner"]
        elif plant_model == "Kiwi":
            geometry_list = ["r_stem"]

        if not geometry_list:
            print("ERROR: No plant geometry is implemented for the selected plant type.")
            exit()
        return geometry_list, network_list

    def getPlantsFromFile(self):
        """
        Read csv file to retrieve position and geometry of initial population.
        Returns:
            dict
        """
        # Loading the Population Data
        try:
            plant_file = pd.read_csv(self.filename, delimiter=";|,|\t", engine='python')
        except pd.errors.ParserError:
            plant_file = pd.read_csv(self.filename, delimiter=";", engine='python')
        headers = plant_file.head()
        plant_attributes = {}
        for header in headers:
            plant_attributes[plant_file[header].name] = plant_file[header].to_numpy()
        return plant_attributes

    def getPlantAttributes(self, initial_group):
        if initial_group:
            positions, geometry, network = self.getInitialGroup()
        else:
            number_of_plants = self.n_recruitment_per_step
            positions = Random.getRandomPositions(self=self,
                                                  number_of_plants=number_of_plants)
            geometry = np.full(len(positions["x"]), False)
            network = {}
        return positions, geometry, network



