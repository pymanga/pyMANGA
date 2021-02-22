#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-Today
@author: marie-christin.wimmler@tu-dresden.de
"""
import numpy as np
from TreeModelLib.BelowgroundCompetition import BelowgroundCompetition


class SimpleNetwork(BelowgroundCompetition):
    #########
    # BASIC #
    #########

    ## Network approach to alter, i.e. increase or decrease, water availability
    #  due to water exchange with other trees (root grafting).
    #  Processes are partner selection, group formation and water exchange.\n
    #  @param: Tags to define SimpleNetwork, see tag documentation \n
    #  @date: 2021 - Today
    def __init__(self, args):
        case = args.find("type").text
        print("Initiate below-ground competition of type " + case + ".")

    ## This functions prepares the tree variables for the SimpleHydro
    #  concept.\n
    #  @param t_ini - initial time for next timestep \n
    #  @param t_end - end time for next timestep
    def prepareNextTimeStep(self, t_ini, t_end):
        # Parameters associated with the SimpleBettina model
        self.trees = []
        self._xe = []
        self._ye = []
        self._tree_names = np.empty(0)
        self._psi_height = []
        self._psi_leaf = []
        self._psi_osmo = []
        ## Water potential acting at the top of the tree, that is the difference between
        # min. leaf water potential and height potential
        self._psi_top = []
        self._r_root = []
        self._r_stem = []
        self._kf_sap = []
        self.belowground_resources = []
        self._t_ini = t_ini
        self._t_end = t_end
        self.time = t_end - t_ini

        # Parameters associated with the network concept
        # List of length n-trees, which contains the names of adjacent trees
        self._partner_names = []
        # List of length n-trees, which contains the current indices of adjacent trees
        self._partner_indices = []
        ## List of length n-trees, which contains the name of tree with which currently
        # develops a connection (root graft)
        self._potential_partner = []
        ## List of length n-trees, which contains a counter indicating the status of the
        # root graft formation (rgf) process. If > 0 the tree is in the process of rgf, if = -1
        # the tree is not in the process of rgf
        self._rgf_counter = []
        ## Dictionary that represents the network of grafted trees (= nodes)
        # Trees are the keys and Links are the adjacent tree(s)
        self.graph_dict = {}
        ## List of length n-trees, which contains the group IDs indicating which trees
        # belong to the same group.
        self._gIDs = []
        ## Resistance acting above the root graft, that is the sum of crown and stem
        # xylem resistance
        self._above_graft_resistance = np.empty(0)
        ## Resistance acting below the root graft, that is the sum of root xylem resistance
        # and root surface resistance
        self._below_graft_resistance = np.empty(0)

    ## Before being able to calculate the resources, all tree entities need
    #  to be added with their relevant allometric measures for the next timestep.
    #  @param: tree
    def addTree(self, tree):
        x, y = tree.getPosition()
        geometry = tree.getGeometry()
        parameter = tree.getParameter()
        self.network = tree.getNetwork()

        self.trees.append(tree)

        self._rgf_counter.append(self.network['rgf'])
        self._partner_names.append(self.network['partner'])
        self._potential_partner.append(self.network['potential_partner'])

        self._xe.append(x)
        self._ye.append(y)
        self.n_trees = len(self._xe)
        self._tree_names = np.concatenate((self._tree_names,
                                           [str(tree.group_name) + str(tree.tree_id)]))

        self._below_graft_resistance = np.concatenate((self._below_graft_resistance,
                                                       [self.belowGraftResistance(parameter["lp"],
                                                                                  parameter["k_geom"],
                                                                                  parameter["kf_sap"],
                                                                                  geometry["r_root"],
                                                                                  geometry["h_root"],
                                                                                  geometry["r_stem"])]
                                                       ))
        self._above_graft_resistance = np.concatenate((self._above_graft_resistance,
                                                       [self.aboveGraftResistance(
                                                          parameter["kf_sap"], geometry["r_crown"],
                                                          geometry["h_stem"], geometry["r_stem"])]
                                                       ))

        self._r_root.append(geometry["r_root"])
        self._r_stem.append(geometry["r_stem"])

        self._psi_leaf.append(parameter["leaf_water_potential"])
        self._psi_height.append((2 * geometry["r_crown"] + geometry["h_stem"]) * 9810)
        self._psi_top = np.array(self._psi_leaf) - np.array(self._psi_height)
        self._psi_osmo = np.array([0] * self.n_trees)  # Salinity is 0 ppt is the basic scenario

        self._kf_sap.append(parameter["kf_sap"])

    ## This function returns a list of the growth modification factors of all trees.
    #  calculated in the subsequent timestep.\n
    #  The factor is > 1, if trees receive water from their adjacent trees; < 1 if the
    #  lose water to the adjacent tree; or = 1 if no exchange happens
    #  @return: np.array with $N_tree$ scalars
    def calculateBelowgroundResources(self):
        self.groupFormation()
        self.rootGraftFormation()
        self.calculateBGresourcesTree()
        res_b = self.getBGresourcesIndividual(self._psi_top, self._psi_osmo,
                                              self._above_graft_resistance,
                                              self._below_graft_resistance)
        self.belowground_resources = self._water_avail / res_b

        # Update the parameter belonging to the tree and are needed in the growth-
        # and-death-concept
        for i, tree in zip(range(0, self.n_trees), self.trees):
            network = {}
            network['partner'] = self._partner_names[i]
            network['rgf'] = self._rgf_counter[i]
            network['potential_partner'] = self._potential_partner[i]
            network['water_available'] = self._water_avail[i]
            network['water_absorbed'] = self._water_absorb[i]
            network['water_exchanged'] = self._water_exchanged_trees[i]
            network['psi_osmo'] = self._psi_osmo[i]

            tree.setNetwork(network)

    '''
    ##############################
    # Sub-model: group formation #
    ##############################

    The sub-model group formation manages the formation of groups. Therefore, it requires 
    a list with tree_names (self._tree_names) and a list with partner_names (self._partners).
    The sub-model converts the partner_names into current index values, then creates a graph dictionary
    from the partner indices and assigns groupIDs (self._gID).
    '''

    ## This function removes trees from partner list if they died in the previous time step.
    def updatedPartnerNames(self):
        for i in range(0, len(self._partner_names)):
            partners_delete = []
            for j in range(0, len(self._partner_names[i])):
                ## If the name of the partner isn't in the list of tree names anymore it will be removed
                # from the partner list
                if self._partner_names[i][j] not in self._tree_names:
                    partners_delete.append(self._partner_names[i][j])
            if partners_delete:
                for p in partners_delete:
                    self._partner_names[i].remove(p)

    ## This function gets the current indices of partners from their names.
    def updatePartnerIdices(self):
        ## In order to access the partners by their indices the current indices must be
        # updated in each time step.
        tree_indices = np.array(range(0, self.n_trees))
        for i in self._partner_names:
            if not i:
                self._partner_indices.append([])
            else:
                h = []
                for j in i:
                    a = tree_indices[np.where(self._tree_names == j)][0]
                    h.append(a)
                self._partner_indices.append(h)

    ## This function creates a graph dictionary from the partner indices.
    def makeGraphDictionary(self):
        for i in range(0, len(self._partner_indices)):
            self.graph_dict[i] = set(self._partner_indices[i])

    ## This function finds all subcomponents of a graph, i.e. groups of grafted trees.
    # The function is based on jimifiki's code
    # (ref: https://stackoverflow.com/questions/10301000/python-connected-components)
    # @param graph_dictionary - a dictionary with tree indices as keys and
    # the adjacent partner trees as values
    # @return a dictionary defining groups by an ID (key) and the indices of the
    # corresponding trees (value)
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
                    myRoot[myMax] = (myMax, max(myRoot[myMin][1] + 1, myRoot[myMax][1]))
                    myRoot[myMin] = (myRoot[myMax][0], -1)
        myToRet = {}
        for myI in graph_dictionary:
            if myRoot[myI][0] == myI:
                myToRet[myI] = []
        for myI in graph_dictionary:
            myToRet[findRoot(myI, myRoot)[0]].append(myI)
        return myToRet

    ## This function assigns unique component/ group IDs based on the graph dictionary.
    def assignGroupIDs(self):
        components = self.getComponents(self.graph_dict)
        self._gIDs = np.zeros(self.n_trees, dtype='object')
        for i in components.keys():
            self._gIDs[components[i]] = 'gID_' + str(i)

    ## This function calls all the sub-functions to get the current groups and their unique IDs.
    def groupFormation(self):
        self.updatedPartnerNames()
        self.updatePartnerIdices()
        self.makeGraphDictionary()
        self.assignGroupIDs()

    '''
    ###################################
    # Sub-model: root graft formation #
    ###################################

    The sub-model root graft formation initializes the formation process. Therefore, it requires 
    a the x-, y-positions of trees, the root radii, the rgf-value and the partner_indexes (sm: group-formatio).
    The sub-model returns an array with booleans indicating whether the root graft formation of a tree
    starts or not. Based on the array it updates the tree attribute 'rgf_counter'.
    '''

    ## This function calculates the distance between two trees in meter.
    # @return a scalar
    def getDistance(self, x1, x2, y1, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    ## This function returns a matrix indicating whether roots of trees are in contact or not
    # @return a matrix of shape n-trees*n-trees with bool to indicate whether tree root are in
    # contact
    def getContactMatrix(self):
        x_mesh = np.array(np.meshgrid(self._xe, self._xe))
        y_mesh = np.array(np.meshgrid(self._ye, self._ye))
        # calculate distances between all trees
        distances = ((x_mesh[0] - x_mesh[1]) ** 2 + (y_mesh[0] - y_mesh[1]) ** 2) ** .5

        roots = np.array(np.meshgrid(self._r_root, self._r_root))
        root_sums = roots[0] + roots[1]

        # probability for root contact
        p_meeting = 1 - distances / root_sums
        # probability is 0 for tree = tree (diagonal)
        np.fill_diagonal(p_meeting, 0)

        # generate random float
        props = np.random.random((len(self._xe), len(self._xe)))
        contact_matrix = np.zeros(np.shape(x_mesh[0]))
        indices = np.where(props < p_meeting)
        contact_matrix[indices] += 1

        return contact_matrix

    ## Function that returns an array with pairs based on the contact matrix.
    # @return a 2d array with tree indices of connected trees (format: from, to)
    def getPairsFromMatrix(self, contact_matrix):
        pairs = []
        for i in range(0, self.n_trees):
            for j in range(i + 1, self.n_trees):
                if contact_matrix[i, j] == 1:
                    pairs.append([i, j])
        return pairs

    ## Function to check if a pair of trees fullfiles all the conditions to startk root graft formation
    # @return bool that indicate whether a pair of trees fulfils the requirements to start
    # root graft formation
    # @param pair - a 2d array with tree indices of connected trees (format: from, to)
    def checkRgfAbility(self, pair):
        l1, l2 = pair[0], pair[1]

        # ... find out if they are already grafted with one another, if yes jump to next pair
        # condition1 is met (i.e. true) if they are not already grafted
        condition1 = False if l2 in self._partner_indices[l1] else True
        # ... find out if they are currently within the root graft formation process, if yes jump to next pair
        condition2 = True if (self._rgf_counter[l1] == -1 and self._rgf_counter[l2] == -1) else False
        # ... condition 3 is still missing.
        condition3 = True  # if

        # ... find out if the grafting conditions are met, if yes set rgf = 1
        start_rgf = True if ((condition1 and condition2 and condition3) == True) else False
        return start_rgf

    ## Function that modifies the tree-own vairable 'rgf_counter'.
    # If a pair of trees are ale to start root graft formation the variable is set to 1 and
    # the adjacent tree is added to the list of potential partners.
    # @param pair - a 2d array with tree indices of connected trees (format: from, to)
    def getRGFforGrowthAndDeath(self, pairs):
        for i in range(0, len(pairs)):
            pair = pairs[i]
            if self.checkRgfAbility(pair=pairs[i]):
                l1, l2 = pair[0], pair[1]
                self._rgf_counter[l1], self._rgf_counter[l2] = 1, 1
                self._potential_partner[l1], self._potential_partner[l2] = self._tree_names[l2], self._tree_names[l1]

    ## Function that calls all the sub procedures to initialize root graft formation.
    def rootGraftFormation(self):
        contact_matrix = self.getContactMatrix()
        pairs = self.getPairsFromMatrix(contact_matrix)
        self.getRGFforGrowthAndDeath(pairs)

    '''
    #####################################
    # Sub-model: below-ground resources #
    #####################################

    The sub-model below-ground resources calculates the below-ground resources, which are water intake,
    water available and water exchanged, as well as returns the below-ground resources factor to the
    growth and death dynamics concept. Therefore, it requires ...
    '''

    ## Function that calculates the below-graft resistance (i.e. stem and crown xylem resistance).
    # @return a scalar
    # @param lp - hydraulic conductivity of root skin
    # @param k_geom - root surface per fine root biomass
    # @param kf_sap - hydraulic conductivity of xylem
    # @param r_root - root radius
    # @param h_root - height of fine roots
    # @param r_stem - stem radius
    def belowGraftResistance(self, lp, k_geom, kf_sap, r_root, h_root, r_stem):
        below_graft_resistance = 1 / (lp * k_geom * np.pi * r_root ** 2 * h_root) + \
                                 (0.5 ** 0.5 * r_root) / (kf_sap * np.pi * r_stem ** 2)
        return below_graft_resistance

    ## Function that calculates the above-graft resistance (i.e. stem and crown xylem resistance).
    # @return a scalar
    # @param kf_sap - hydraulic conductivity of xylem
    # @param r_crown - crown radius
    # @param h_stem - stem height
    # @param r_stem - stem radius
    def aboveGraftResistance(self, kf_sap, r_crown, h_stem, r_stem):
        above_graft_resistance = (2 * r_crown + h_stem) / (kf_sap * np.pi * r_stem ** 2)
        return above_graft_resistance

    ## Function that calculates the xylem resistance in the grafted roots.
    # @return a scalar
    # @param distance - distance between connected trees
    # @param r_graft - radius of grafted roots
    # @param kf_sap - hydraulic conductivity of xylem
    def getGraftResistance(self, distance, r_graft, kf_sap):
        graft_resistance = distance / (kf_sap * np.pi * r_graft ** 2)
        return graft_resistance

    ## Function that returns an array with the links of a specific tree.
    # @return a list with tree indices of adjacent trees
    # @param link_list - a 2d array with tree indices of connected trees (format: from, to)
    # @param tree - index of the tree under consideration
    def getMyLinks(self, link_list, tree):
        my_links = []
        for links in link_list:
            if tree in links:
                my_links.append(links)
        return my_links

    ## Function that creates a 2d array with links (from, to) based of graph-dictionary.
    # The function is based on the code of a python course on graphs
    # (ref: https://www.python-course.eu/graphs_python.php)
    # @return a 2d array with tree indices of connected trees (format: from, to)
    # @param graph_dictionary - a dictionary with tree indices as keys and
    def getLinkList(self, graph_dict):
        link_list = []
        for vertex in graph_dict:
            for neighbour in graph_dict[vertex]:
                if {neighbour, vertex} not in link_list:
                    link_list.append({vertex, neighbour})
        link_list = [x for x in link_list if len(x) > 1]
        return link_list

    ## Function that creates the matrix to calculate below-ground resources for each group
    # of grafted trees. The matrix contains a set of linear equations (Ax=B) allowing the calculation
    # of water absorbed, available, exchanged for all trees of a group. The equations result from
    # the electronic-hydraulic analogy and the utilization of Kirchhoff's laws.
    # @param members - list with indexes of group members
    # @param link_list - list with connected trees
    # @return a matrix of shape size*size+1 (size = 2*n-trees + n-links); the matrix represents
    # linear equations: Ax=B, whereby matrix[, 0:size] = A and matrix[, size+1] = B
    def getBGresourcesMatrixGroup(self, members, link_list):
        n_t = len(members)
        n_l = len(link_list)
        size = 2 * n_t + n_l
        matrix = np.zeros((size, size + 1))

        j = 0
        for i in members:
            bgCol = j
            agCol = n_t + j

            # 1st law: flow in and out of each tree node
            matrix[j, bgCol] = 1  # below-graft
            matrix[j, agCol] = -1  # above-graft

            my_links = self.getMyLinks(link_list, i)
            for k in my_links:
                gCol = 2 * n_t + np.where(link_list == k)[0]  # index of my_links in linkList
                if list(k)[0] == i:  # check if i is first element of link
                    matrix[j, gCol] = 1
                else:
                    matrix[j, gCol] = -1

            # 2nd law: flow along each along tree
            row = j + n_t
            matrix[row, bgCol] = self._below_graft_resistance[i]
            matrix[row, agCol] = self._above_graft_resistance[i]
            matrix[row, size] = self._psi_osmo[i] - self._psi_top[i]
            j += 1

        # 2nd law: flow between pairs of connected trees, below-graft
        for i in range(0, n_l):
            l1 = list(link_list[i])[0]  # link tree 1
            l2 = list(link_list[i])[1]  # link tree 2
            distance = self.getDistance(x1=self._xe[l1], x2=self._xe[l2],
                                        y1=self._ye[l1], y2=self._ye[l2])
            r_graft = 0.25 * (self._r_stem[l1] + self._r_stem[l2]) / 2
            kf_sap = (self._kf_sap[l1] + self._kf_sap[l2]) / 2
            graft_resistance = self.getGraftResistance(r_graft, distance, kf_sap)
            row = 2 * n_t + i
            col1 = np.where(members == l1)[0]
            col2 = np.where(members == l2)[0]
            matrix[row, col1] = -self._below_graft_resistance[l1]
            matrix[row, col2] = self._below_graft_resistance[l2]
            matrix[row, 2 * n_t + i] = graft_resistance
            matrix[row, size] = self._psi_osmo[l2] - self._psi_osmo[l1]  # y
        return matrix

    ## Function that calculates water uptake of an individual tree, see SimpleBettina.
    # @return a scalar
    # @param psi_top - difference between min. leaf water potential and height potential
    # @param psi_osmo - osmotic potential, caused by pore-water salinity
    # @param ag_resistance - above-graft resistance
    # @param bg_resistance - below-graft resistance
    def getBGresourcesIndividual(self, psi_top, psi_osmo, ag_resistance, bg_resistance):
        res_b = -(psi_top - psi_osmo) / ((ag_resistance + bg_resistance) * np.pi) * self.time
        return res_b

    ## Function that calculates water absorbed, water available and water exchanged for all
    # trees of a group.
    # @param members - list with indexes of group members
    # @param link_list_group - list with connected trees of group (format: from, to)
    def calculateBGresourcesGroup(self, members, link_list_group):
        ## get the system of linear equations (matrix) for the group of grafted trees;
        # linear equation Ax=B in matrix form
        matrix = self.getBGresourcesMatrixGroup(members, link_list_group)
        n_t = len(members)
        n_l = len(link_list_group)

        size = 2 * n_t + n_l
        # separate matrix to get left and right side of linear equations of type Ax=B
        A = matrix[:, 0:size]
        B = matrix[:, size]
        ## Get the inverse of the matrix A and find the dot product between the inverse and the
        # matrix B
        # the result is divided by pi (Peters et al. 2021) and multiplied by the time step length in sec
        X = np.linalg.inv(A).dot(B) / np.pi * self.time  # m³/tsl
        # Assign values from results vector X to different flow rates
        self._water_absorb[members] = X[0:n_t]
        self._water_avail[members] = X[n_t:2 * n_t]
        # water exchanged for each connection
        water_exchanged = X[2 * n_t:size]

        # sum up in- and out-flows (water_exchanged)
        # reshape link_list_group to shape = [2, n_l]
        # transform set of links to list of links
        linkList_group_list = [list(links) for links in link_list_group]
        # reshape link_list_group to shape = [2, n_l]
        reshape_llg = np.transpose(linkList_group_list)
        from_IDs = reshape_llg[0, :]    # from IDs
        to_IDs = reshape_llg[1, :]      # to IDs
        np.add.at(self._water_exchanged_trees, from_IDs, water_exchanged)
        np.add.at(self._water_exchanged_trees, to_IDs,
                  -1 * np.array(water_exchanged))

    ## Function that calculates water absorbed, available and exchanged for all trees.
    # Depending on the graft status of a tree, i.e. grafted vs. non-grafted, this function calls
    # the corresponding BG-resource function.
    def calculateBGresourcesTree(self):
        ids = np.array(range(0, self.n_trees))
        self._water_avail = np.zeros(self.n_trees)
        self._water_absorb = np.zeros(self.n_trees)
        self._water_exchanged_trees = np.zeros(self.n_trees)

        for gID in set(self._gIDs):
            # get tree indices of group members
            members = ids[np.where(self._gIDs == gID)]
            # make a graph dictionary of the group
            graph_dict_group = {i: self.graph_dict[i] for i in members}
            # make a list with indices of connected trees of the group
            link_list_group = np.array(self.getLinkList(graph_dict_group))
            if len(link_list_group) == 0:
                ## if the tree is not grafted water_absorbed and water_available corresponds to
                # SimpleBettina water uptake and water_exchange is 0
                self._water_absorb[members] = self.getBGresourcesIndividual(self._psi_top[members],
                                                                            self._psi_osmo[members],
                                                                            self._above_graft_resistance[members],
                                                                            self._below_graft_resistance[members])
                self._water_avail[members] = self._water_absorb[members]
            else:
                self.calculateBGresourcesGroup(members, link_list_group)
