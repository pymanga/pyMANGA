

class Production:
    """
    Constructor to initialize production modules, by calling respective initialization methods.
    """
    def __init__(self, xml_args):
        """
        Args:
            xml_args (lxml.etree._Element): production module specifications from project file tags
        """
        self.xml_args = xml_args
        try:
            production = xml_args.find("production")
            self.production_type = production.find("type").text
        except AttributeError:
            self.production_type = "fixed"
            print("> Set Production type to Fixed (default).")

        if self.production_type.lower() == "fixed":
            from .Fixed import Fixed as BC
        elif self.production_type.lower() == "dbhdependent":
            from .DBHdependent import DBHdependent as BC
        else:
            raise KeyError("Population initialisation of type", self.production_type, "not implemented!")
        print("Population: " + self.production_type + ".")

        self.production = BC(self.xml_args)
        tags = {
            "prj_file": self.xml_args,
            "required": [],
            "optional": ["type"]
        }
        tags = self.production.getTags(tags)
        self.getInputParameters(**tags)

        if hasattr(self, "formula"):
            self.production.iniProductionFormula()

    def getNumberOfSeeds(self, plants):
        return self.production.getNumberOfSeeds(plants=plants)

    def getInputParameters(self, **tags):
        """
        Read module tags from project file.
        Args:
            tags (dict): dictionary containing tags found in the project file as well as required and optional tags of
            the module under consideration.
        """
        try:
            prj_file_tags = tags["prj_file"]
        except KeyError:
            prj_file_tags = []
            print("WARNING: Module attributes are missing.")
        try:
            required_tags = tags["required"]
        except KeyError:
            required_tags = []
        try:
            optional_tags = tags["optional"]
        except KeyError:
            optional_tags = []

        for arg in prj_file_tags.iterdescendants():
            tag = arg.tag
            for i in range(0, len(required_tags)):
                if tag == required_tags[i]:
                    try:
                        super(Production, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(Production, self).__setattr__(tag, str(arg.text))
            try:
                required_tags.remove(tag)
            except ValueError:
                pass

            for i in range(0, len(optional_tags)):
                if tag == optional_tags[i]:
                    try:
                        super(Production, self).__setattr__(tag, float(arg.text))
                    except ValueError:
                        super(Production, self).__setattr__(tag, str(arg.text))

        if len(required_tags) > 0:
            string = ""
            for tag in required_tags:
                string += tag + " "
            raise KeyError(
                "Missing input parameters (in project file) for population module initialisation: " + string)

        try:
            self.n_recruitment_per_step = int(self.n_recruitment_per_step)
        except AttributeError:
            self.n_recruitment_per_step = 0

        # Transfer attribute dictionary to respective dispersal module
        self.production.__dict__.update(self.__dict__)
