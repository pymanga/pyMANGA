import pandas as pd
from PopulationLib.Dispersal.Random import Random


class FromFile:
    def __init__(self, xml_group):
        print("Population: FromFile.")
        self.tags_group = xml_group

    def getTags(self):
        tags = {
            "prj_file": self.tags_group,
            "required": ["type", "filename", "domain", "x_1", "x_2", "y_1", "y_2"],
            "optional": ["n_recruitment_per_step"]
        }
        return tags

    def initializeGroup(self, others):
        self.plant_attributes_file = self.getPlantsFromFile(others=others)

        # Get parameters that are required for the selected plant module
        parameter_list = self.getParameterList()
        self.plant_attributes = {}
        for parameter in parameter_list:
            try:
                self.plant_attributes[parameter] = self.plant_attributes_file[parameter].flatten()
            except AttributeError:
                print("Something went wrong")
                # ToDo: bessere Variablennamen + Error message

    def getParameterList(self):
        plant_model = self.tags_group.find("vegetation_model_type").text
        if plant_model == "Bettina" or plant_model == "BettinaNetwork":
            pl = ["r_stem", "h_stem", "r_crown", "r_root"]
        if plant_model == "Kiwi":
            pl = ["r_stem"]
        # ToDo: geht das auch cooler?
        parameter_list = ["x", "y"]
        for p in pl:
            parameter_list.append(p)
        return parameter_list

    def recruitPlants(self, others):
        self.xi, self.yi = Random.getRandomPositions(self=self,
                                                     others=others,
                                                     number_of_plants=others.n_recruitment_per_step)

    def getPlantsFromFile(self, others):
        # Loading the Population Data
        plant_file = pd.read_csv(others.filename)
        headers = plant_file.head()
        plant_attributes = {}
        for header in headers:
            plant_attributes[plant_file[header].name] = plant_file[header].to_numpy()
        return plant_attributes

