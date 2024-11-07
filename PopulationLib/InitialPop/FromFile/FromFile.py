import pandas as pd
from ProjectLib import helpers as helpers


class FromFile:
    """
    FromFile dispersal module
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): distribution module specifications from project file tags
        """
        print(">>>>>> FromFile init")

        self.getInputParameters(args=xml_args)

    def getInputParameters(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "filename"]
        }
        myself = super(FromFile, self)
        helpers.getInputParameters(myself, **tags)

    def getInitialGroup(self):
        """
        Return positions and geometries of first plants in the model (i.e., the initial population).
        Returns:
            dict, np.array
        """
        plant_attributes_file = self.getPlantsFromFile()
        geometry_list, network_list = self.getGeometryList()

        int = set(geometry_list).intersection(list(plant_attributes_file))
        if len(int) == 0:
            print("ERROR: geometry parameters in initial population do not match plant module.")
            print("Accepted columns names:", geometry_list)
            exit()
        else:
            # Get parameters that are required for the selected plant module
            geometry, network = {}, {}
            for geo in geometry_list:
                try:
                    geometry[geo] = plant_attributes_file[geo].flatten()
                except KeyError:
                    pass
            for net in network_list:
                try:
                    network[net] = plant_attributes_file[net].flatten()
                except KeyError:
                    pass
            positions = {"x": plant_attributes_file["x"].flatten(),
                         "y": plant_attributes_file["y"].flatten()}
            return positions, geometry, network

    def getGeometryList(self):
        """
        Return list of geometries accepted in pyMANGA plant modules.
        Returns:
            list
        """
        geometry_list = ["r_stem", "h_stem", "r_crown", "r_root",
                         "r_ag", "h_ag", "r_bg", "h_bg"]
        network_list = ["partner"]
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

    def getPlantAttributes(self):
        print(">>>>>> FromFile getPlantAttributes")

        positions, geometry, network = self.getInitialGroup()

        return positions, geometry, network



