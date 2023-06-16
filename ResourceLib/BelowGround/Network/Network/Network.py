#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2021-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
import numpy as np
from ResourceLib import ResourceModel


class Network(ResourceModel):
    #########
    # BASIC #
    #########

    ## Network approach to alter, i.e. increase or decrease, water availability
    #  due to water exchange with other plants (root grafting).
    #  Processes are partner selection, group formation and water exchange.\n
    #  @param: Tags to define Network, see tag documentation \n
    #  @date: 2021 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate below-ground competition of type " + case + ".")
        self.getInputParameters(args=args)

    ## This functions prepares the plant variables for the NetworkHydro
    #  concept.\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        # Parameters associated with the SimpleBettina model
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

    ## Before being able to calculate the resources, all plant entities need
    #  to be added with their relevant allometric measures for the next
    #  timestep.
    #  @param: plant
    def addPlant(self, plant):
        x, y = plant.getPosition()
        geometry = plant.getGeometry()
        parameter = plant.getParameter()
        self.network = plant.getNetwork()

        self.plants.append(plant)

        self._rgf_counter.append(self.network['rgf'])
        self._partner_names.append(self.network['partner'])
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

    ## This function creates a (dummy) array to be filled with values of
    # osmotic potential
    def addPsiOsmo(self):
        # Salinity is 0 ppt is the basic scenario
        self._psi_osmo = np.array([0] * self.no_plants)

    def calculateBelowgroundResources(self):
        """
        Calculate a growth reduction factor for each tree based on pore-water salinity below the
        center of each tree.
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

    ## This function calculates the below-ground resource factor,
    # that is the fraction of water available in base water uptake (i.e. no
    # salinity, no water exchange through root grafts)
    def getBGfactor(self):
        # Calculate water uptake with 0 ppt salinity
        res_b_noSal = self.getBGresourcesIndividual(
            psi_top=self._psi_top,
            psi_osmo=np.array([0] * self.no_plants),
            ag_resistance=self._above_graft_resistance,
            bg_resistance=self._below_graft_resistance)
        return self._water_avail / res_b_noSal

    ## This function updates the network parameters that are required in the
    # growth-and death concept BettinaNetwork
    def updateNetworkParametersForGrowthAndDeath(self):
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

    ## This function reads input parameters, i.e. proportion of grafted root
    # radius of stem radius, from the control file.
    def getInputParameters(self, args):
        missing_tags = ["type", "f_radius"]
        for arg in args.iterdescendants():
            tag = arg.tag
            if tag == "f_radius":
                self.f_radius = float(args.find("f_radius").text)
                if self.f_radius <= 0:
                    raise ValueError("Parameter f_radius needs to be > 0.")
            elif tag == "type":
                case = args.find("type").text
            try:
                missing_tags.remove(tag)
            except ValueError:
                print("WARNING: Tag " + tag + " not specified for " + case +
                      " growth-and-death " + "initialisation!")
        if len(missing_tags) > 0:
            string = ""
            for tag in missing_tags:
                string += tag + " "
            raise KeyError(
                "Tag(s) " + string +
                "are missing for below-ground initialisation in project "
                "file.")

    '''
    ##############################
    # Sub-model: group formation #
    ##############################

    The sub-model group formation manages the formation of groups. Therefore, 
    it requires a list with plant_names (self._plant_names) and a list with 
    partner_names (self._partners).
    The sub-model converts the partner_names into current index values, 
    then  creates a graph dictionary from the partner indices and assigns 
    groupIDs (self._gID).
    '''

    ## This function removes plants from partner list if they died in the
    # previous time step.
    def updatedPartnerNames(self):
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

    ## This function removes plants from potential partners list if they died in
    # the previous time step.
    def updatedPotentialPartnerNames(self):
        for i in range(0, len(self._potential_partner)):
            ## If the name of the _potential_partner isn't in the list
            # of plant names anymore it will be removed from the partner
            # list
            if (self._potential_partner[i]) and (self._potential_partner[i]
                                                 not in self._plant_names):
                self._potential_partner[i] = []
                self._rgf_counter[i] = -1

    ## This function gets the current indices of partners from their names.
    def updatePartnerIdices(self):
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

    ## Function that adds keys and values to dictionary
    def setKeyDictionary(self, dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = value
        elif len(dictionary[key]) == 0:
            dictionary[key] = {value}
        else:
            dictionary[key] = dictionary[key] | {value}

    ## Function that makes a graph dictionary only with functional grafts,
    # i.e. both involved plants have finished root graft formation
    def makeGraphDictionary(self):
        graph_dict_incomplete = {}
        # dictionary contains all links, no matter if they are functional
        for i in range(0, len(self._partner_indices)):
            graph_dict_incomplete[i] = set(self._partner_indices[i])
        if self._variant[0] == "V0_instant":
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

    ## This function finds all subcomponents of a graph, i.e. groups of
    # grafted plants.
    # The function is based on jimifiki's code
    # (ref:  https://stackoverflow.com/questions/10301000/python-connected
    # -components)
    # @param graph_dictionary - a dictionary with plant indices as keys and
    # the adjacent partner plants as values
    # @return a dictionary defining groups by an ID (key) and the indices of
    # the corresponding plants (value)
    def getComponents(self, graph_dictionary):

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

    ## This function assigns unique component/ group IDs based on the graph
    # dictionary.
    def assignGroupIDs(self):
        components = self.getComponents(graph_dictionary=self.graph_dict)
        self._gIDs = np.zeros(self.no_plants, dtype='object')
        for i in components.keys():
            self._gIDs[components[i]] = 'gID_' + str(i)

    ## This function calls all the sub-functions to get the current groups
    # and their unique IDs.
    def groupFormation(self):
        self.updatedPartnerNames()
        self.updatedPotentialPartnerNames()
        self.updatePartnerIdices()
        self.makeGraphDictionary()
        self.assignGroupIDs()

    '''
    ###################################
    # Sub-model: root graft formation #
    ###################################

    The sub-model root graft formation initializes the formation process.  
    Therefore, it requires a the x-, y-positions of plants, the root radii, 
    the rgf-value and the partner_indexes (sm: group-formation).
    The sub-model returns an array with booleans indicating whether the root 
    graft formation of a plant starts or not. Based on the array it updates
    the plant attribute 'rgf_counter'.
    '''

    ## This function calculates the distance between two plants in meter.
    # @return a scalar
    def getDistance(self, x1, x2, y1, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    ## This function returns a matrix indicating whether roots of plants are
    # in contact or not
    # @return a matrix of shape n-plants*n-plants with bool to indicate
    # whether plant root are in contact
    def getContactMatrix(self):
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

    ## Function that returns an array with pairs based on the contact matrix.
    # @return a 2d array with plant indices of connected plants (format:
    # from, to)
    def getPairsFromMatrix(self, contact_matrix):
        # reshape to a triangular matrix to avaid duplicated links
        contact_matrix_upper = np.triu(contact_matrix)
        pairs = np.argwhere(contact_matrix_upper == 1).tolist()
        return pairs

    ## Function to check if a pair of plants fullfiles all the conditions to
    # start root graft formation
    # @return bool that indicate whether a pair of plants fulfils the
    # requirements to start root graft formation
    # @param pair - a 2d array with plant indices of connected plants (format:
    # from, to)
    def checkRgfAbility(self, pair):
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

    ## Function that modifies the plant-own vairable 'rgf_counter'.
    # If a pair of plants are ale to start root graft formation the variable
    # is set to 1 and the adjacent plant is added to the list of potential
    # partners.
    # @param pair - a 2d array with plant indices of connected plants (format:
    # from, to)
    def getRGFforGrowthAndDeath(self, pairs):
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
                if (self._variant[l1] == "V2_adapted") and \
                        (self._variant[l2] == "V2_adapted"):
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
                                                             root_sums * l_gr,

    ## Function that calls all the sub procedures to initialize root graft
    # formation.
    def rootGraftFormation(self):
        contact_matrix = self.getContactMatrix()
        pairs = self.getPairsFromMatrix(contact_matrix=contact_matrix)
        self.getRGFforGrowthAndDeath(pairs=pairs)

    '''
    #####################################
    # Sub-model: below-ground resources #
    #####################################

    The sub-model below-ground resources calculates the below-ground 
    resources, which are water intake, water available and water exchanged, 
    as well as returns the below-ground resources factor to the
    growth and death dynamics concept. Therefore, it requires ...
    '''

    ## Function that calculates the below-graft resistance (i.e. stem and
    # crown xylem resistance).
    # @return a scalar
    # @param lp - hydraulic conductivity of root skin
    # @param k_geom - root surface per fine root biomass
    # @param kf_sap - hydraulic conductivity of xylem
    # @param r_root - root radius
    # @param h_root - height of fine roots
    # @param r_stem - stem radius
    def belowGraftResistance(self, lp, k_geom, kf_sap, r_root, h_root, r_stem):
        below_graft_resistance = 1 / (
                lp * k_geom * np.pi * r_root ** 2 * h_root) + \
                                 (0.5 ** 0.5 * r_root) / (
                                         kf_sap * np.pi * r_stem ** 2)
        return below_graft_resistance

    ## Function that calculates the above-graft resistance (i.e. stem and
    # crown xylem resistance).
    # @return a scalar
    # @param kf_sap - hydraulic conductivity of xylem
    # @param r_crown - crown radius
    # @param h_stem - stem height
    # @param r_stem - stem radius
    def aboveGraftResistance(self, kf_sap, r_crown, h_stem, r_stem):
        above_graft_resistance = (2 * r_crown + h_stem) / (kf_sap * np.pi *
                                                           r_stem**2)
        return above_graft_resistance

    ## Function that calculates the xylem resistance in the grafted roots.
    # @return a scalar
    # @param distance - distance between connected plants
    # @param r_graft - radius of grafted roots
    # @param kf_sap - hydraulic conductivity of xylem
    def getGraftResistance(self, distance, r_graft, kf_sap):
        graft_resistance = distance / (kf_sap * np.pi * r_graft**2)
        return graft_resistance

    ## Function that returns an array with the links of a specific plant.
    # @return a list with plant indices of adjacent plants
    # @param link_list - a 2d array with plant indices of connected plants
    # (format: from, to)
    # @param plant - index of the plant under consideration
    def getMyLinks(self, link_list, plant):
        my_links = []
        for links in link_list:
            if plant in links:
                my_links.append(links)
        return my_links

    ## Function that creates a 2d array with links (from, to) based of
    # graph-dictionary.
    # The function is based on the code of a python course on graphs
    # (ref: https://www.python-course.eu/graphs_python.php)
    # @return a 2d array with plant indices of connected plants
    # (format: from, to)
    # @param graph_dictionary - a dictionary with plant indices as keys and
    def getLinkList(self, graph_dict):
        link_list = []
        for vertex in graph_dict:
            for neighbour in graph_dict[vertex]:
                if {neighbour, vertex} not in link_list:
                    link_list.append({vertex, neighbour})
        link_list = [x for x in link_list if len(x) > 1]
        return link_list

    ## Function that creates the matrix to calculate below-ground resources
    # for each group of grafted plants. The matrix contains a set of linear
    # equations (Ax=B) allowing the calculation of water absorbed,
    # available, exchanged for all plants of a group. The equations result from
    # the electronic-hydraulic analogy and the utilization of Kirchhoff's laws.
    # @param members - list with indexes of group members
    # @param link_list - list with connected plants of the group
    # @return a matrix of shape size*size+1 (size = 2*n-plants + n-links);
    # the matrix represents
    # linear equations: Ax=B, whereby matrix[, 0:size] = A and
    # matrix[, size+1] = B
    def getBGresourcesMatrixGroup(self, members, link_list):
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

    ## Function that calculates water uptake of an individual plant in m³ per
    # time step, see  SimpleBettina.
    # @return a scalar
    # @param psi_top - difference between min. leaf water potential and
    # height potential
    # @param psi_osmo - osmotic potential, caused by pore-water salinity
    # @param ag_resistance - above-graft resistance
    # @param bg_resistance - below-graft resistance
    def getBGresourcesIndividual(self, psi_top, psi_osmo, ag_resistance,
                                 bg_resistance):
        res_b = -(psi_top - psi_osmo) / (
            (ag_resistance + bg_resistance) * np.pi) * self.time
        return res_b

    ## Function that calculates water absorbed, water available and water
    # exchanged for all plants of a group.
    # @param members - list with indexes of group members
    # @param link_list_group - list with connected plants of group
    # (format: from, to)
    def calculateBGresourcesGroup(self, members, link_list_group):
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

    ## Function that calculates water absorbed, available and exchanged for
    # all plants. Depending on the graft status of a plant, i.e. grafted vs.
    # non-grafted, this function calls the corresponding BG-resource function.
    def calculateBGresourcesPlant(self):
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
            if len(link_list_group) == 0:
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
