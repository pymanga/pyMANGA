#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from ResourceLib import ResourceModel


class Network(ResourceModel):
    """
    Network below-ground resource concept.
    """
    def __init__(self, args):
        """
        Args:
            args (lxml.etree._Element): below-ground module specifications from project file tags
        """
        case = args.find("type").text
        self.getInputParameters(args=args)

    def prepareNextTimeStep(self, t_ini, t_end):
        # Parameters associated with the Bettina model
        self.plants = []
        self._xe = []
        self._ye = []
        self._plant_names = np.empty(0)
        self._psi_height = []
        self._psi_leaf = []
        self._psi_osmo = []
        ## Water potential acting at the top of the plant, that is the
        # difference between min. leaf water potential and height potential
        self._psi_top = []
        self._r_root = []
        self._r_stem = []
        self._kf_sap = []
        self.belowground_resources = []
        self._t_ini = t_ini
        self._t_end = t_end
        self.time = t_end - t_ini

        # Parameters associated with the network concept
        # List of length n-plants, which contains the names of adjacent plants
        self._partner_names = []
        # List of length n-plants, which contains the current indices of
        # adjacent plants
        self._partner_indices = []
        ## List of length n-plants, which contains the name of plant with
        # which  currently
        # develops a connection (root graft)
        self._potential_partner = []
        ## List of length n-plants, which contains a counter indicating the
        # status of the root graft formation (rgf) process. If > 0 the plant
        # is in the process of rgf, if = -1 the plant is not in the process
        # of rgf
        self._rgf_counter = []

        self._variant = []
        self._node_degree = []
        # parameters for rgf variant "V2_adapted"
        self._r_gr_min = []
        self._r_gr_rgf = []
        self._l_gr_rgf = []
        self._weight_gr = []

        ## Dictionary that represents the network of grafted plants (= nodes).
        # Plants are the keys and Links are the adjacent plant(s)
        self.graph_dict = {}
        ## List of length n-plants, which contains the group IDs indicating
        # which plants belong to the same group.
        self._gIDs = []
        ## Resistance acting above the root graft, that is the sum of crown a
        # nd stem xylem resistance
        self._above_graft_resistance = np.empty(0)
        ## Resistance acting below the root graft, that is the sum of root
        # xylem resistance and root surface resistance
        self._below_graft_resistance = np.empty(0)

    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self.network = plant.getNetwork()

        self.plants.append(plant)
        self._rgf_counter.append(self.network['rgf'])
        try:
            eval_partner = eval(self.network['partner'])
        except TypeError:
            eval_partner = self.network['partner']
        self._partner_names.append(eval_partner)
        self._potential_partner.append(self.network['potential_partner'])

        self._variant.append(self.network['variant'])
        self._node_degree.append(self.network['node_degree'])

        # Only valid for Variant V2_adapted: list with min./current grafted root radius
        # of each pair; same structure as potential_partner
        # required for rgf
        # parameters for rgf variant "V2_adapted"
        self._r_gr_min.append(self.network['r_gr_min'])
        self._r_gr_rgf.append(self.network['r_gr_rgf'])
        self._l_gr_rgf.append(self.network['l_gr_rgf'])

        # List with grafted root radius; same structure as partner_names
        # required for water exchange
        self._weight_gr.append(self.network['weight_gr'])

        self._xe.append(x)
        self._ye.append(y)
        self.no_plants = len(self._xe)
        self._plant_names = np.concatenate(
            (self._plant_names, [str(plant.group_name) + str(plant.plant_id)]))

        self._below_graft_resistance = np.concatenate(
            (self._below_graft_resistance, [
                self.belowGraftResistance(lp=parameter["lp"],
                                          k_geom=parameter["k_geom"],
                                          kf_sap=parameter["kf_sap"],
                                          r_root=geometry["r_root"],
                                          h_root=geometry["h_root"],
                                          r_stem=geometry["r_stem"])
            ]))
        self._above_graft_resistance = np.concatenate(
            (self._above_graft_resistance, [
                self.aboveGraftResistance(kf_sap=parameter["kf_sap"],
                                          r_crown=geometry["r_crown"],
                                          h_stem=geometry["h_stem"],
                                          r_stem=geometry["r_stem"])
            ]))

        self._r_root.append(geometry["r_root"])
        self._r_stem.append(geometry["r_stem"])

        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._psi_height.append(
            -(2 * geometry["r_crown"] + geometry["h_stem"]) * 9810)
        self._psi_top = np.array(self._psi_leaf) - np.array(self._psi_height)

        # psi osmo is added separately in some below-ground competition concept
        self.addPsiOsmo()

        self._kf_sap.append(parameter["kf_sap"])

    def addPsiOsmo(self):
        """
        Create array with 0 to be filled with values of osmotic water potential
        Sets:
            numpy array of shape(number_of_plants)
        """
        # Salinity is 0 ppt is the basic scenario
        self._psi_osmo = np.array([0] * self.no_plants)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each tree based on water exchange between grafted trees.
        In Network resource concepts, this factor can reduce or facilitate growth.<br>
        If factor > 1: plant gets water from its neighbour<br>
        If factor == 1: no exchange and resource limitation<br>
        If factor < 1: plant loses water to its neighbour or resources are limited
        Sets:
            numpy array of shape(number_of_plants)
        """
        self.groupFormation()
        self.rootGraftFormation()
        self.calculateBGresourcesPlant()
        self.belowground_resources = self.getBGfactor()
        self.updateNetworkParametersForGrowthAndDeath()

    def getBGfactor(self):
        """
        Calculate below-ground resource factor as fraction of water available actual:potential.
        Returns:
            numpy array of shape(number_of_plants)
        """
        # Calculate water uptake with 0 ppt salinity
        res_potential = self.getBGresourcesIndividual(
            psi_top=self._psi_top,
            psi_osmo=np.array([0] * self.no_plants),
            ag_resistance=self._above_graft_resistance,
            bg_resistance=self._below_graft_resistance)
        return self._water_avail / res_potential

    def updateNetworkParametersForGrowthAndDeath(self):
        """
        Update network dictionary with parameters required in PlantLib
        Sets:
            dictionary
        """
        # Update the parameter belonging to the plant and are needed in the
        # growth- and-death-concept
        for i, plant in zip(range(0, self.no_plants), self.plants):
            network = {}
            # Parameters related to the root graft formation process
            network['potential_partner'] = self._potential_partner[i]
            network['rgf'] = self._rgf_counter[i]
            network['partner'] = self._partner_names[i]
            network['groupID'] = self._gIDs[i]
            # Parameter related to water exchange
            network['water_available'] = self._water_avail[i]
            network['water_absorbed'] = self._water_absorb[i]
            network['water_exchanged'] = self._water_exchanged_plants[i]
            network['psi_osmo'] = self._psi_osmo[i]
            # parameters for rgf variant "V2_adapted"
            network['weight_gr'] = self._weight_gr[i]
            network['r_gr_rgf'] = self._r_gr_rgf[i]
            network['r_gr_min'] = self._r_gr_min[i]
            network['l_gr_rgf'] = self._l_gr_rgf[i]
            network['variant'] = self._variant[i]
            network['node_degree'] = self._node_degree[i]

            plant.setNetwork(network)

    def getInputTags(self, args):
        tags = {
            "prj_file": args,
            "required": ["type", "f_radius"],
            "optional": ["exchange"]
        }
        return tags

    def getInputParameters(self, args):
        tags = self.getInputTags(args)
        super().getInputParameters(**tags)
        if not hasattr(self, "exchange"):
            self.exchange = "on"
            print("> Set below-ground network parameter 'exchange' to default:", self.exchange)

    '''
    ##############################
    # Sub-model: group formation #
    ##############################
    '''

    def groupFormation(self):
        """
        Group formation management.
        Call all sub-functions to define the current groups and their unique IDs.
        The procedures take a list of plant names (self._plant_names) and a list of partner names (self._partners).
        They convert the partner_names to current index values, then create a graph dictionary from the partner indices
        and assign groupIDs (self._gID).
        """
        self.updatedPartnerNames()
        self.updatedPotentialPartnerNames()
        self.updatePartnerIdices()
        self.makeGraphDictionary()
        self.assignGroupIDs()

    def updatedPartnerNames(self):
        """
        Remove plants from list of partners if they died in the previous time step.
        Sets:
            array of shape(number_of_plants)
        """
        self._plant_names = np.array(self._plant_names, dtype=object)
        for i in range(0, len(self._partner_names)):
            partners_delete = []
            for j in range(0, len(self._partner_names[i])):
                ## If the name of the partner isn't in the list of plant
                # names anymore it will be removed from the partner list
                if self._partner_names[i][j] not in self._plant_names:
                    partners_delete.append(self._partner_names[i][j])
            if partners_delete:
                for p in partners_delete:
                    self._partner_names[i].remove(p)

    def updatedPotentialPartnerNames(self):
        """
        Removes plants from list of potential partners if they died in the previous time step.
        Sets:
            array of shape(number_of_plants)
        """
        for i in range(0, len(self._potential_partner)):
            ## If the name of the _potential_partner isn't in the list
            # of plant names anymore it will be removed from the partner
            # list
            if (self._potential_partner[i]) and (self._potential_partner[i]
                                                 not in self._plant_names):
                self._potential_partner[i] = []
                self._rgf_counter[i] = -1

    def updatePartnerIdices(self):
        """
        Set partner indexes based on their names
        Sets:
            array of shape(number_of_plants)
        """
        ## In order to access the partners by their indices the current
        # indices must be updated in each time step.
        plant_indices = np.array(range(0, self.no_plants))
        for i in self._partner_names:
            if not i:
                self._partner_indices.append([])
            else:
                h = []
                for j in i:
                    a = plant_indices[np.where(self._plant_names == j)][0]
                    h.append(a)
                self._partner_indices.append(h)

    def setKeyDictionary(self, dictionary, key, value):
        """
        Set key and value in a dictionary.
        Args:
            dictionary (dict): dictionary
            key (array): list of strings
            value (array): list of strings or floats
        Sets:
            dictionary
        """
        if key not in dictionary:
            dictionary[key] = value
        elif len(dictionary[key]) == 0:
            dictionary[key] = {value}
        else:
            dictionary[key] = dictionary[key] | {value}

    def makeGraphDictionary(self):
        """
        Create dictionary with functional root grafts (functional = both involved plants have finished root graft
        formation)
        Sets:
            dictionary
        """
        graph_dict_incomplete = {}
        # dictionary contains all links, no matter if they are functional
        for i in range(0, len(self._partner_indices)):
            graph_dict_incomplete[i] = set(self._partner_indices[i])

        if self._variant[0] and "v0" in self._variant[0]:
            self.graph_dict = graph_dict_incomplete
        else:
            # helper
            link_list = []
            link_list2 = []
            for vertex in graph_dict_incomplete:
                self.setKeyDictionary(dictionary=self.graph_dict,
                                      key=vertex,
                                      value=set())
                for neighbour in graph_dict_incomplete[vertex]:
                    # Iterate through all plants and the neighbours
                    # If a new pair occurs it will be appended in link_list2
                    # If the pair occurs again it wll be appended in link_list
                    # This means that the link (or rgf process) is finished
                    # for both plants
                    if {neighbour, vertex} not in link_list2:
                        link_list2.append({vertex, neighbour})
                    else:
                        # plants are only put in the dict. if they occur more
                        # than once, i.e. both partners have finished rgf
                        link_list.append({vertex, neighbour})
                        self.setKeyDictionary(dictionary=self.graph_dict,
                                              key=vertex,
                                              value=neighbour)

    def getComponents(self, graph_dictionary):
        """
        Find all subcomponents of a graph, i.e. groups of grafted plants.
        Credit: [jimifiki](https://stackoverflow.com/questions/10301000/python-connected-components)
        Args:
            graph_dictionary (dict): dictionary with plant indices as keys and the adjacent partner plants as values
        Returns:
            dictionary defining groups by an ID (key) and the indices of the corresponding plants (value)
        """
        def findRoot(aNode, aRoot):
            while aNode != aRoot[aNode][0]:
                aNode = aRoot[aNode][0]
            return (aNode, aRoot[aNode][1])

        myRoot = {}
        for myNode in graph_dictionary.keys():
            myRoot[myNode] = (myNode, 0)
        for myI in graph_dictionary:
            for myJ in graph_dictionary[myI]:
                (myRoot_myI, myDepthMyI) = findRoot(myI, myRoot)
                (myRoot_myJ, myDepthMyJ) = findRoot(myJ, myRoot)
                if myRoot_myI != myRoot_myJ:
                    myMin = myRoot_myI
                    myMax = myRoot_myJ
                    if myDepthMyI > myDepthMyJ:
                        myMin = myRoot_myJ
                        myMax = myRoot_myI
                    myRoot[myMax] = (myMax,
                                     max(myRoot[myMin][1] + 1,
                                         myRoot[myMax][1]))
                    myRoot[myMin] = (myRoot[myMax][0], -1)
        myToRet = {}
        for myI in graph_dictionary:
            if myRoot[myI][0] == myI:
                myToRet[myI] = []
        for myI in graph_dictionary:
            myToRet[findRoot(myI, myRoot)[0]].append(myI)
        return myToRet

    def assignGroupIDs(self):
        """
        Assign unique component/ group ID based on the graph dictionary.
        Sets:
            array of shape(number_of_plants)
        """
        components = self.getComponents(graph_dictionary=self.graph_dict)
        self._gIDs = np.zeros(self.no_plants, dtype='object')
        for i in components.keys():
            self._gIDs[components[i]] = 'gID_' + str(i)

    '''
    ###################################
    # Sub-model: root graft formation #
    ###################################
    '''

    def rootGraftFormation(self):
        """
        Initialization of the formation process.
        Call all sub-functions to initialize the root graft formation process.
        The procedures require the x-, y-positions of plants and their root radii, rgf-value the partner_indexes.
        The procedures set an array with booleans indicating whether the root graft formation of a plant starts or not.
        Based on the array they update the plant attribute 'rgf_counter'.
        """
        contact_matrix = self.getContactMatrix()
        pairs = self.getPairsFromMatrix(contact_matrix=contact_matrix)
        self.getRGFforGrowthAndDeath(pairs=pairs)

    def getDistance(self, x1, x2, y1, y2):
        """
        Get distance between two plants (in meter).
        Args:
            x1: x-position of plant 1
            x2: x-position of plant 2
            y1: y-position of plant 1
            y2: y-position of plant 2
        Returns:
            float
        """
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    def getContactMatrix(self):
        """
        Get contact matrix indicating whether roots of plants are in contact or not.
        Returns:
            array with bools of shape(number_of_plants, number_of_plants)
        """
        x_mesh = np.array(np.meshgrid(self._xe, self._xe))
        y_mesh = np.array(np.meshgrid(self._ye, self._ye))
        # calculate distances between all plants
        distances = ((x_mesh[0] - x_mesh[1])**2 +
                     (y_mesh[0] - y_mesh[1])**2)**.5

        roots = np.array(np.meshgrid(self._r_root, self._r_root))
        root_sums = roots[0] + roots[1]

        # probability for root contact
        p_meeting = 1 - distances / root_sums
        # probability is 0 for plant = plant (diagonal)
        np.fill_diagonal(p_meeting, 0)

        # generate matrix with random floats
        probs = np.random.random((len(self._xe), len(self._xe)))
        # reshape to a triangular matrix
        probs = np.triu(probs)
        # Mirror upper triangle of the matrix
        probs += probs.transpose()

        contact_matrix = np.zeros(np.shape(x_mesh[0]))
        indices = np.where(probs < p_meeting)
        contact_matrix[indices] += 1

        return contact_matrix

    def getPairsFromMatrix(self, contact_matrix):
        """
        Get all pairs of plants with their roots in contact with each other.
        Format: from, to
        Args:
            contact_matrix (array): 2D matrix indicating whether roots are in contact
        Returns:
            array
        """
        # reshape to a triangular matrix to avoid duplicated links
        contact_matrix_upper = np.triu(contact_matrix)
        pairs = np.argwhere(contact_matrix_upper == 1).tolist()
        return pairs

    def checkRgfAbility(self, pair):
        """
        Check whether a pair of plants fulfills conditions to start root graft formation (pair = roots are touching)
        Condition 1: plants are not yet grafted
        Condition 2: plants are not yet in root graft formation process
        Condition 3: r_stem is 0.75 cm
        Args:
            pair (array): 2d array with plant indices of connected plants (format: from, to)
        Returns:
            bool
        """
        l1, l2 = pair[0], pair[1]

        ## ... find out if they are already grafted with one another,
        # if yes jump to next pair
        # condition1 is met (i.e. true) if they are not already grafted
        condition1 = False if l2 in self._partner_indices[l1] else True
        ## ... find out if they are currently within the root graft formation
        # process, if yes jump to next pair
        condition2 = True if (self._rgf_counter[l1] == -1
                              and self._rgf_counter[l2] == -1) else False
        # ... check if both plants have a certain size (i.e. DBH > 1.5 cm) in
        # order to avoid that freshly recruited plants start grafting
        condition3 = True if (self._r_stem[l1] > 0.0075
                              and self._r_stem[l2] > 0.0075) else False

        # ... find out if the grafting conditions are met, if yes set rgf = 1
        start_rgf = True if ((condition1 and condition2 and condition3)
                             == True) else False
        return start_rgf

    def getRGFforGrowthAndDeath(self, pairs):
        """
        Modify the plant-own variable 'rgf_counter'.
        If a pair of plants is ready to start root graft formation, the variable is set to 1 and the adjacent plant is
        added to the list of partners.
        Args:
            pairs (array): a 2d array with plant indices of connected plants (format: from, to)
        Sets:
            multiple arrays
        """
        # Create a list of length pairs with random integers to iterate
        # randomly through the list of pairs
        shuffled_indices = np.random.choice(len(pairs),
                                            len(pairs),
                                            replace=False)
        for i in shuffled_indices:
            pair = pairs[i]
            if self.checkRgfAbility(pair=pairs[i]):
                l1, l2 = pair[0], pair[1]
                self._rgf_counter[l1], self._rgf_counter[l2] = 1, 1
                self._potential_partner[l1], self._potential_partner[l2] = \
                    self._plant_names[l2], self._plant_names[l1]
                try:
                    if "v2" in (self._variant[l1] and self._variant[l2]):
                        # Set initial size of grafted root radius
                        self._r_gr_rgf[l1], self._r_gr_rgf[l2] = 0.004, 0.004
                        # Get min. radius of grafted roots
                        r_gr_min = self.f_radius * min(self._r_stem[l1],
                                                       self._r_stem[l2])
                        self._r_gr_min[l1], self._r_gr_min[l2] = [r_gr_min], \
                                                                 [r_gr_min]

                        # Get length of grafted root section
                        distance = self.getDistance(x1=self._xe[l1],
                                                    x2=self._xe[l2],
                                                    y1=self._ye[l1],
                                                    y2=self._ye[l2])
                        root_sums = self._r_root[l1] + self._r_root[l2]
                        l_gr = (distance + root_sums) / 2
                        self._l_gr_rgf[l1], self._l_gr_rgf[l2] = self._r_root[l1] / \
                                                                 root_sums * l_gr, \
                                                                 self._r_root[l2] / \
                                                                 root_sums * l_gr
                except TypeError:
                    print("WARNING: No network variant assigned.")

    '''
    #####################################
    # Sub-model: below-ground resources #
    #####################################
    '''
    def calculateBGresourcesPlant(self):
        """
        Calculate water absorbed, available and exchanged for all plants.
        Depending on the graft status of a plant, i.e. grafted vs. non-grafted, call the corresponding below-ground
        resource function.
        Sets:
            multiple float
        """
        ids = np.array(range(0, self.no_plants))
        self._water_avail = np.zeros(self.no_plants)
        self._water_absorb = np.zeros(self.no_plants)
        self._water_exchanged_plants = np.zeros(self.no_plants)
        for gID in set(self._gIDs):
            # get plant indices of group members
            members = ids[np.where(self._gIDs == gID)]
            # make a graph dictionary of the group
            graph_dict_group = {i: self.graph_dict[i] for i in members}
            # make a list with indices of connected plants of the group
            link_list_group = np.array(
                self.getLinkList(graph_dict=graph_dict_group))
            if len(link_list_group) == 0 or self.exchange == "off":
                ## if the plant is not grafted water_absorbed and
                # water_available corresponds to SimpleBettina water uptake
                # and water_exchange is 0
                self._water_absorb[members] = self.getBGresourcesIndividual(
                    psi_top=self._psi_top[members],
                    psi_osmo=self._psi_osmo[members],
                    ag_resistance=self._above_graft_resistance[members],
                    bg_resistance=self._below_graft_resistance[members])
                self._water_avail[members] = self._water_absorb[members]
            else:
                self.calculateBGresourcesGroup(members=members,
                                               link_list_group=link_list_group)

    def belowGraftResistance(self, lp, k_geom, kf_sap, r_root, h_root, r_stem):
        """
        Calculate resistance against flow for below-ground plant biomass (i.e., roots).
        Args:
            lp (float): hydraulic conductivity of root skin
            k_geom (float): root surface per fine root biomass
            kf_sap (float): hydraulic conductivity of xylem
            r_root (float): root radius
            h_root (float): height of fine roots
            r_stem (float): stem radius
        Returns:
            float
        """
        below_graft_resistance = 1 / (
                lp * k_geom * np.pi * r_root ** 2 * h_root) + \
                                 (0.5 ** 0.5 * r_root) / (
                                         kf_sap * np.pi * r_stem ** 2)
        return below_graft_resistance

    def aboveGraftResistance(self, kf_sap, r_crown, h_stem, r_stem):
        """
        Calculate resistance against flow for above-ground plant biomass (i.e., stem, crown).
        Args:
            kf_sap (float): hydraulic conductivity of xylem
            r_crown (float): crown radius
            h_stem (float): stem height
            r_stem (float): stem radius
        Returns:
            float
        """
        above_graft_resistance = (2 * r_crown + h_stem) / (kf_sap * np.pi *
                                                           r_stem**2)
        return above_graft_resistance

    def getGraftResistance(self, distance, r_graft, kf_sap):
        """
        Calculate resistance against flow within the grafted roots
        Args:
            distance (float): distance between connected plants
            r_graft (float): radius of grafted roots
            kf_sap (float): hydraulic conductivity of xylem
        Returns:
            float
        """
        graft_resistance = distance / (kf_sap * np.pi * r_graft**2)
        return graft_resistance

    def getMyLinks(self, link_list, plant):
        """
        Get array with the links (connections to other partners) for a specific plant
        Args:
            link_list (array): 2d array with plant indices of connected plants (format: from, to)
            plant (int): index of the plant under consideration
        Returns:
            array of shape (2, no_of_links)
        """
        my_links = []
        for links in link_list:
            if plant in links:
                my_links.append(links)
        return my_links

    def getLinkList(self, graph_dict):
        """
        Get 2d array with links (from, to) based of graph-dictionary.
        Credit: [python-course](https://www.python-course.eu/graphs_python.php)
        Args:
            graph_dict (dict): dictionary with plant indices as keys and partners as values
        Returns:
            array of shape(2, no_of_links_total)
        """
        link_list = []
        for vertex in graph_dict:
            for neighbour in graph_dict[vertex]:
                if {neighbour, vertex} not in link_list:
                    link_list.append({vertex, neighbour})
        link_list = [x for x in link_list if len(x) > 1]
        return link_list

    def getBGresourcesMatrixGroup(self, members, link_list):
        """
        Create the matrix to calculate the below-ground resources for each group of grafted plants.
        The matrix contains a set of linear equations (Ax=B) that allow the calculation of water absorbed, available and
        exchanged, and exchanged for all the plants in a group.
        The equations result from the electronic-hydraulic analogy and the use of Kirchhoff's laws.
        linear equations: Ax=B, whereby matrix[, 0:size] = A and matrix[, size+1] = B
        Args:
            members (array): list with indexes of group members
            link_list (array): list with connected plants of the group
        Returns:
            array of shape(size, size+1), with size = 2*no_of_plants + no_of_links
        """
        # Create empty matrix
        n_t = len(members)
        n_l = len(link_list)
        size = 2 * n_t + n_l
        matrix = np.zeros((size, size + 1))

        ## Basic indices to fill the matrix
        # columns: bg_1 ... bg_t | ag_1 ... ag_t | g_1 ... g_l
        # rows: node_1 ... node_t | plant_1 ... plant_t | link_1 ... link_l
        # Below-graft columns
        bg_col = np.array(range(0, len(members)))
        # Above-graft columns
        ag_col = bg_col + n_t
        # Graft columns
        g_col = (2 * n_t) + np.array(range(0, n_l))
        # node_rows
        node_row = np.array(range(0, len(members)))
        # plant_rows
        plant_rows = node_row + n_t
        # links_rows
        link_rows = (2 * n_t) + np.array(range(0, n_l))

        ## Kirchhoff's 1st law: flow in and out of each plant node
        # Add inflow, i.e. +1, to below-graft column; and outflow, i.e. -1 to
        # above-graft column
        matrix[node_row, bg_col] = 1  # below-graft
        matrix[node_row, ag_col] = -1  # above-graft

        # Add in-/ outflow through graft
        # Transform sets to lists in link_list
        link_list_group_list = [list(links) for links in link_list]
        # reshape link_list_group to shape = [2, n_l]
        reshape_llg = np.transpose(link_list_group_list)
        # Get from and to plant IDs
        from_IDs = reshape_llg[0, :]  # from IDs
        to_IDs = reshape_llg[1, :]  # to IDs
        # Get indices, i.e. rows, corresponding to from and to plant IDs
        from_index = node_row[np.searchsorted(members,
                                              from_IDs,
                                              sorter=node_row)]
        to_index = node_row[np.searchsorted(members, to_IDs, sorter=node_row)]
        # Set graft in- and outflow
        matrix[from_index, g_col] = 1
        matrix[to_index, g_col] = -1

        ## Kirchhoff's 2nd law: flow along the plant

        matrix[plant_rows, bg_col] = self._below_graft_resistance[members]
        matrix[plant_rows, ag_col] = self._above_graft_resistance[members]
        matrix[plant_rows,
               size] = self._psi_osmo[members] - self._psi_top[members]

        ## Kirchhoff's 2nd law: flow between two connected plants
        x_mesh = np.array(np.meshgrid(self._xe, self._xe))
        y_mesh = np.array(np.meshgrid(self._ye, self._ye))
        # calculate distances between all plants of the group
        distances = ((x_mesh[0] - x_mesh[1])**2 +
                     (y_mesh[0] - y_mesh[1])**2)**.5
        r_stem = np.array(np.meshgrid(self._r_stem, self._r_stem))
        r_root = np.array(np.meshgrid(self._r_root, self._r_root))

        # @mcwimm: at the moment the grafted root radius grows proportional to
        #  the stem radius. This might be updated to grow based on avail.
        #  resources.
        r_grafts = self.f_radius * np.minimum(r_stem[0], r_stem[1])
        l_gr = (r_root[0] + r_root[1] + distances) / 2
        kf_sap = np.array(np.meshgrid(self._kf_sap, self._kf_sap))
        kf_saps = (kf_sap[0] + kf_sap[1]) / 2
        graft_resistance = self.getGraftResistance(distance=l_gr[from_IDs,
                                                                 to_IDs],
                                                   r_graft=r_grafts[from_IDs,
                                                                    to_IDs],
                                                   kf_sap=kf_saps[from_IDs,
                                                                  to_IDs])
        matrix[link_rows, from_index] = -self._below_graft_resistance[from_IDs]
        matrix[link_rows, to_index] = self._below_graft_resistance[to_IDs]
        matrix[link_rows, g_col] = graft_resistance
        matrix[link_rows,
               size] = self._psi_osmo[to_IDs] - self._psi_osmo[from_IDs]  # y
        return matrix

    def getBGresourcesIndividual(self, psi_top, psi_osmo, ag_resistance,
                                 bg_resistance):
        """
        Get water uptake of an individual plant in m³ per time step based on BETTINA (Peters et al. 2014).
        Args:
            psi_top (float): difference between min. leaf water potential and height potential
            psi_osmo (float): osmotic potential, function of pore-water salinity
            ag_resistance (float): above-graft resistance
            bg_resistance (float): below-graft resistance
        Returns:
            float
        """
        res_b = -(psi_top - psi_osmo) / (
            (ag_resistance + bg_resistance) * np.pi) * self.time
        return res_b

    def calculateBGresourcesGroup(self, members, link_list_group):
        """
        Calculate water absorbed, water available and water exchanged for all plants of a group.
        Args:
            members (array): list with indexes of group members
            link_list_group (array): ist with connected plants of group (format: from, to)
        Sets:
            multiple float
        """
        ## Get the system of linear equations (matrix) for the group of
        # grafted plants;
        # linear equation Ax=B in matrix form
        matrix = self.getBGresourcesMatrixGroup(members=members,
                                                link_list=link_list_group)

        n_t = len(members)
        n_l = len(link_list_group)

        size = 2 * n_t + n_l
        ## separate matrix to get left and right side of linear equations of
        # type Ax=B
        A = matrix[:, 0:size]
        B = matrix[:, size]
        ## Get the inverse of the matrix A and find the dot product between
        # the inverse and the matrix B the result is divided by pi (Peters
        # et al. 2021) and multiplied by the time step length in sec
        X = np.linalg.inv(A).dot(B) / np.pi * self.time  # unit: m³/tsl
        # Assign values from results vector X to different flow rates
        self._water_absorb[members] = X[0:n_t]
        self._water_avail[members] = X[n_t:2 * n_t]
        # water exchanged for each connection
        water_exchanged = X[2 * n_t:size]

        ## Sum up in- and out-flows of each plant (water_exchanged)
        # transform set of links to list of links
        linkList_group_list = [list(links) for links in link_list_group]
        # reshape link_list_group to shape = [2, n_l]
        reshape_llg = np.transpose(linkList_group_list)
        from_IDs = reshape_llg[0, :]  # from IDs
        to_IDs = reshape_llg[1, :]  # to IDs
        np.add.at(self._water_exchanged_plants, from_IDs, water_exchanged)
        np.add.at(self._water_exchanged_plants, to_IDs,
                  -1 * np.array(water_exchanged))
