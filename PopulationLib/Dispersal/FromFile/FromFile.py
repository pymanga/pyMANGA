import pandas as pd
import numpy as np
from PopulationLib.Dispersal.Random import Random


class FromFile:
    def __init__(self, xml_args):
        self.xml_args = xml_args

    def getTags(self):
        tags = {
            "prj_file": self.xml_args,
            "required": ["type", "filename", "domain", "x_1", "x_2", "y_1", "y_2"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def getInitialGroup(self):
        plant_attributes_file = self.getPlantsFromFile()
        # Get parameters that are required for the selected plant module
        geometry_list = self.getGeometryList()
        geometry = {}
        for geo in geometry_list:
            try:
                geometry[geo] = plant_attributes_file[geo].flatten()
            except KeyError:
                print("ERROR: geometry parameters in initial population do not match plant module.")
                exit()
        positions = {"x": plant_attributes_file["x"].flatten(),
                     "y": plant_attributes_file["y"].flatten()}
        return positions, geometry

    def getGeometryList(self):
        # ToDo: Liste mit notwendigen Parametern irgendwoher holen?
        plant_model = self.xml_args.find("vegetation_model_type").text

        if plant_model == "Default":
            # ToDo: Welche Geometrie soll für Default definiert werden? Anpassung Benchmarks&ini_pop.csv notwendig
            # geometry_list = ["r_ag", "h_ag", "r_bg", "h_bg"]
            geometry_list = ["r_stem", "h_stem", "r_crown", "r_root"]
        elif plant_model in ["Bettina", "BettinaNetwork"]:
            geometry_list = ["r_stem", "h_stem", "r_crown", "r_root"]
        elif plant_model == "Kiwi":
            geometry_list = ["r_stem"]

        return geometry_list

    def getPlantAttributes(self, initial_group):
        if initial_group:
            positions, geometry = self.getInitialGroup()
        else:
            number_of_plants = self.n_recruitment_per_step
            positions = Random.getRandomPositions(self=self,
                                                  number_of_plants=number_of_plants)
            geometry = np.full(len(positions["x"]), False)
        return positions, geometry

    def getPlantsFromFile(self):
        # Loading the Population Data
        plant_file = pd.read_csv(self.filename, delimiter=";|,|\t", engine='python')
        headers = plant_file.head()
        plant_attributes = {}
        for header in headers:
            plant_attributes[plant_file[header].name] = plant_file[header].to_numpy()
        return plant_attributes

