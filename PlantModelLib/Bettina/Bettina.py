#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PlantModelLib import PlantModel
import numpy as np
import math


class Bettina(PlantModel):
    def __init__(self, args):
        """
        Plant model concept.
        Args:
            args: Bettina module specifications from project file tags
        """
        case = args.find("type").text
        print("Growth and death dynamics of type " + case + ".")
        super().iniMortalityConcept(args)

    def prepareNextTimeStep(self, t_ini, t_end):
        """
        Prepare next time step by initializing relevant variables.
        Args:
            t_ini (int): start of current time step in seconds
            t_end (int): end of current time step in seconds
        """
        self.time = t_end - t_ini

    def progressPlant(self, tree, aboveground_resources,belowground_resources):
        """
        Manage growth procedures for a timestep --- read tree geometry and parameters,
        schedule computations, and update tree geometry and survival.
        Args:
            tree (dict): tree object
            aboveground_resources (float): aboveground resource growth reduction factor
            belowground_resources (float): belowground resource growth reduction factor
        """
        geometry = tree.getGeometry()
        growth_concept_information = tree.getGrowthConceptInformation()
        self.parameter = tree.getParameter()
        self.r_crown = geometry["r_crown"]
        self.h_crown = geometry["h_crown"]
        self.r_root = geometry["r_root"]
        self.h_root = geometry["h_root"]
        self.r_stem = geometry["r_stem"]
        self.h_stem = geometry["h_stem"]
        self.alive = geometry["alive"]
        self.beta_alt = self.parameter["beta"]
        self.survive = 1
        
        
        #####################################################
        self.flowLength()
        self.treeVolume()
        _salinity = self.getSalinityFromBGR(belowground_resources)
        alpha = self.parameter["alpha"]
        if self.beta_alt > 0:
            n_cond_alt = self.NCond(alpha,self.beta_alt) / self.momCorr(alpha,self.beta_alt,2,self.qgamma(0.99,alpha,self.beta_alt))
            kf_sap_alt = self.defKS(n_cond_alt,alpha,self.beta_alt) * self.momCorr(alpha,self.beta_alt,4,self.qgamma(0.99,alpha,self.beta_alt))
            print(alpha)
            print(_salinity)
            print(self.beta_alt)
            print(n_cond_alt)
            print(kf_sap_alt)
            print(" ")
        self.calcBeta(alpha,_salinity)
        n_cond = self.NCond(alpha,self.beta) / self.momCorr(alpha,self.beta,2,self.qgamma(0.99,alpha,self.beta))
        
        kf_sap = self.defKS(n_cond,alpha,self.beta) * self.momCorr(alpha,self.beta,4,self.qgamma(0.99,alpha,self.beta))
        print(kf_sap)

        if self.beta_alt > 0:
            if self.beta > 1.00001 * self.beta_alt:
                print("shock")
                print("ncond alt + neu")               
                print(n_cond_alt)
                print(n_cond)
                print("Beta alt + neu")               
                print(self.beta_alt)
                print(self.beta)
                xlimi = math.log(self.beta_alt/self.beta)/(self.beta_alt - self.beta) * alpha +  math.log(n_cond_alt/n_cond)/(self.beta_alt - self.beta)
                print("xlimi")
                print(xlimi)
                kf_sap1 = self.defKS(n_cond_alt,alpha,self.beta_alt) * self.momCorr(alpha,self.beta_alt,4,xlimi)
                kf_sap2 = self.defKS(n_cond,alpha,self.beta) * (self.momCorr(alpha,self.beta,4,self.qgamma(0.99,alpha,self.beta)) - self.momCorr(alpha,self.beta,4,xlimi))
                kf_sap = kf_sap1 + kf_sap2 
                print("teil ksaps")
                print(kf_sap1)
                print(kf_sap2)
                
        self.parameter["kf_sap"] = kf_sap    
        print(self.parameter["kf_sap"])
        # Define variables that are only required for specific Mortality
        # concepts
        super().setMortalityVariables(growth_concept_information)

        self.treeMaintenance()
        self.bgResources(1)
        self.agResources(aboveground_resources)
        self.growthResources()
        if self.grow > 0:
            self.treeGrowthWeights()
            self.treeGrowth()
        if self.grow < 0:
            print("scheiße")
        geometry["r_crown"] = self.r_crown
        geometry["h_crown"] = self.h_crown
        geometry["r_root"] = self.r_root
        geometry["h_root"] = self.h_root
        geometry["r_stem"] = self.r_stem
        geometry["h_stem"] = self.h_stem
        self.parameter["beta"] = self.beta
        growth_concept_information[
            "root_surface_resistance"] = self.root_surface_resistance
        growth_concept_information["xylem_resistance"] = self.xylem_resistance
        growth_concept_information["ag_resources"] = self.ag_resources
        growth_concept_information["bg_resources"] = self.bg_resources
        growth_concept_information["growth"] = self.grow
        growth_concept_information["available_resources"] = (
            self.available_resources)
        psi_zero = self.deltaPsi()
        growth_concept_information["psi_zero"] = psi_zero
        growth_concept_information["salinity"] = (
            (belowground_resources * psi_zero - psi_zero) / 85000000.)
        growth_concept_information["weight_girthgrowth"] = \
            self.weight_girthgrowth
        growth_concept_information["weight_stemgrowth"] = \
            self.weight_stemgrowth
        growth_concept_information["weight_crowngrowth"] = \
            self.weight_crowngrowth
        growth_concept_information["weight_rootgrowth"] = \
            self.weight_rootgrowth

        # Get Mortality-related variables
        super().getMortalityVariables(growth_concept_information)

        tree.setGeometry(geometry)
        tree.setGrowthConceptInformation(growth_concept_information)
        if self.survive == 1:
            tree.setSurvival(1)
        else:
            tree.setSurvival(0)

    def treeGrowth(self):
        """
        Update tree geometry.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'increase of allometric measures'.
        Sets:
            multiple float
        """
        inc_r_stem = (self.weight_girthgrowth * self.grow /
                      (2 * np.pi * self.r_stem * self.flow_length))
        self.r_stem += inc_r_stem
        inc_h_stem = (self.weight_stemgrowth * self.grow /
                      (np.pi * self.r_stem**2))
        self.h_stem += inc_h_stem
        inc_r_crown = (self.weight_crowngrowth * self.grow /
                       (2 * np.pi *
                        (self.h_crown * self.r_crown + self.r_stem**2)))
        self.r_crown += inc_r_crown
        inc_r_root = (self.weight_rootgrowth * self.grow /
                      (2 * np.pi * self.r_root * self.h_root +
                       0.5**0.5 * np.pi * self.r_stem**2))
        self.r_root += inc_r_root

    def treeGrowthWeights(self):
        """
        Calculate the growth weights for distributing biomass increment to the tree geometries.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'weights'.
        Sets:
            multiple float
        """
        self.weight_stemgrowth = (
            self.parameter["half_max_h_growth_weight"] /
            (1 + np.exp(-(self.r_crown - self.r_root) /
                        (self.r_crown + self.r_root) /
                        self.parameter["h_sigmo_slope"])))
        self.weight_crowngrowth = ((1 - self.weight_stemgrowth) / (1 + np.exp(
            (self.ag_resources - self.bg_resources) /
            (self.ag_resources + self.bg_resources) /
            self.parameter["sigmo_slope"])))

        self.weight_girthgrowth = (
            (1 - self.weight_stemgrowth - self.weight_crowngrowth) /
            (1 + np.exp(
                (self.root_surface_resistance - self.xylem_resistance) /
                (self.root_surface_resistance + self.xylem_resistance) /
                self.parameter["sigmo_slope"])))

        self.weight_rootgrowth = (1 - self.weight_stemgrowth -
                                  self.weight_crowngrowth -
                                  self.weight_girthgrowth)

    def treeMaintenance(self):
        """
        Calculate the resource demand for biomass maintenance.

        For parameter reference, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 2.5.
        Sets:
            float
        """
        self.maint = self.volume * self.parameter["maint_factor"] * self.time

    def flowLength(self):
        """
        Calculate the flow length from fine roots to leaves.
        Sets:
            float
        """
        self.flow_length = (2 * self.r_crown + self.h_stem +
                            0.5**0.5 * self.r_root)

    ## This function calculates the total tree volume.
    def treeVolume(self):
        """
        Calculate the total tree volume.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'volume of plant components'.
        Sets:
            float
        """
        self.volume = (self.h_root * np.pi * self.r_root**2 +
                       self.flow_length * np.pi * self.r_stem**2 * self.alive +
                       self.h_crown * np.pi * self.r_crown**2)

    def agResources(self, aboveground_resources):
        """
        Calculate the available aboveground resources (intercepted light measured equivalent to respective water uptake).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            aboveground_resources (float): aboveground resource growth reduction factor
        Sets:
            float
        """
        self.ag_resources = aboveground_resources * (
            np.pi * self.r_crown**2 * self.parameter["sun_c"] * self.time)

    def bgResources(self, belowground_resources):
        """
        Calculate the available belowground resources (m³ water per time step).

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Args:
            belowground_resources (float): belowground resource growth reduction factor
        Sets:
            float
        """
        self.rootSurfaceResistance()
        self.xylemResistance()
        self.bg_resources = belowground_resources * (
            (-self.time * self.deltaPsi() /
             (self.root_surface_resistance + self.xylem_resistance) / np.pi))

    def rootSurfaceResistance(self):
        """
        Calculate the root surface resistance.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Sets:
            float
        """
        self.root_surface_resistance = (1 / self.parameter["lp"] /
                                        self.parameter["k_geom"] / np.pi /
                                        self.r_root**2 / self.h_root)

    def xylemResistance(self):
        """
        Calculate the xylem resistance.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resistances'.
        Sets:
            float
        """
        self.xylem_resistance = (self.flow_length / self.parameter["kf_sap"] /
                                 np.pi / self.r_stem**2 / self.alive)

    def deltaPsi(self):
        """
        Calculate the water potential gradient with soil water potential = 0.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Returns:
            float
        """
        return (self.parameter["d_psi"] +
                (2 * self.r_crown + self.h_stem) * 9810)

    def growthResources(self):
        """
        Calculate the available resources and the biomass increment.

        For equation formulation, see Peters, Olagoke and Berger
        ([2018](https://doi.org/10.1016/j.ecolmodel.2018.10.005)), Appendix B (Bettina ODD), section 7.2,
        heading 'resources'.
        Sets:
            multiple float
        """
        self.available_resources = min(self.ag_resources, self.bg_resources)
        self.grow = (self.parameter["growth_factor"] *
                     (self.available_resources - self.maint))
        # Check if trees survive based on selected mortality concepts
        super().setTreeKiller()

        
    def qgamma(self,p,shape,rate=1):
        """
        Calculates the cumulative of the Gamma-distribution
        """
        from scipy.stats import gamma
        result=(1/rate)*gamma.ppf(q=p,a=shape,loc=0,scale=1)
        return result
        
    def pgamma(self,q,shape,rate=1):
        """
        Calculates the cumulative of the Gamma-distribution
        """
        from scipy.stats import gamma
        result=gamma.cdf(x=rate*q,a=shape,loc=0,scale=1)
        return result
 
    def defKS(self,n_cond,alpha,beta,ceff=0.1,mu=0.001):
        return np.pi*ceff/8/mu * n_cond/beta**4 * (3+alpha) * (2+alpha) * (1+alpha) * alpha

       
    def NCond(self,alpha,beta,dcond=0.1):
        return dcond/np.pi/(1+alpha)/alpha*beta**2
       
    def momCorr(self,alpha,beta,n,qu):
        return self.pgamma(qu,alpha + n,beta)     

    def getSalinityFromBGR(self,belowground_resources):
        _psi0 = self.parameter["leaf_water_potential"] + (2*self.r_crown + self.h_stem) * 9810
        return ((belowground_resources-1) * _psi0 / 85e6)

    def calcBeta(self,alpha,salinity):
        from scipy.stats import gamma
        self.beta = self.qgamma(p=0.99,shape=alpha,rate=1)/(self.parameter["a_perc99"]+self.parameter["b_perc99"]*salinity*1000)

