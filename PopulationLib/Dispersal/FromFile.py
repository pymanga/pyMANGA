import numpy as np
from PopulationLib import PlantGroup

class FromFile(PlantGroup):
    def __init__(self, args):
        """
        Dispersal concept model.
        Args:
            args:  FromFile module specifications from project file tags.
        """
        pass

    def plantPlantsFromFile(self, args):
        """
        Function initializing plant population of size n_individuals from a file within given
        rectangular domain.
        Args:
            args:
                arguments specified in project file. Please see tag
        Sets:
            multiple float
        """
        missing_tags = ["type", "filename"]
        self.n_recruitment = 0
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "filename":
                filename = arg.text
            elif tag == "n_recruitment_per_step":
                self.n_recruitment = int(arg.text)
            if tag != "n_recruitment_per_step":
                try:
                    missing_tags.remove(tag)
                except ValueError:
                    raise ValueError(
                        "Tag " + tag +
                        " not specified for random plant planting!")

        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Mandatory tag(s) " + string +
                "is(are) not given for plant planting in project file.")

        plant_file = open(filename)
        i = 0
        x_idx, y_idx = 99999, 99999
        r_crown_idx, r_stem_idx, r_root_idx, h_stem_idx = (99999, 99999, 99999,
                                                           99999)
        geometry = {}
        max_x, max_y = -99999, -99999
        min_x, min_y = 99999, 99999
        for line in plant_file.readlines():
            line = line.replace("\t", "").split(",")

            if i == 0:
                j = 0
                for tag in line:
                    tag = tag.strip()
                    print(tag)
                    if tag == "x" and x_idx == 99999:
                        x_idx = int(j)
                        i += 1
                    if tag == "y" and y_idx == 99999:
                        y_idx = int(j)
                        i += 1
                    if tag == "r_crown" and r_crown_idx == 99999:
                        r_crown_idx = int(j)
                        i += 1
                    if tag == "r_stem" and r_stem_idx == 99999:
                        r_stem_idx = int(j)
                        i += 1
                    if tag == "r_root" and r_root_idx == 99999:
                        r_root_idx = int(j)
                        i += 1
                    if tag == "h_stem" and h_stem_idx == 99999:
                        i += 1
                        h_stem_idx = int(j)
                    j += 1
                if i != 6:
                    raise KeyError(
                        6 - i, "Plant properties were not correctly " +
                        "indicated in the population input file! " +
                        "Please check the documentation!")
            else:
                x, y = float(line[x_idx]), float(line[y_idx])
                geometry["r_crown"] = float(line[r_crown_idx])
                geometry["r_root"] = float(line[r_root_idx])
                geometry["r_stem"] = float(line[r_stem_idx])
                geometry["h_stem"] = float(line[h_stem_idx])
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                min_x = min(min_x, x)
                min_y = min(min_y, y)
        self.x_1 = min_x
        self.y_1 = min_y
        self.l_x = max_x - self.x_1
        self.l_y = max_y - self.y_1

    def recruitPlants(self):
            """
            Randomly recruiting trees within given domain.
            Returns: random x and y of n_recruitment in the corresponding domain.
            """
            for i in range(self.n_recruitment):
                r_x, r_y = (np.random.rand(2))
                x_i = self.x_1 + self.l_x * r_x
                y_i = self.y_1 + self.l_y * r_y
                self.addTree(x_i, y_i)