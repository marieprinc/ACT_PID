# ACT-PID_analysis.py
# This script is used to open the WCTE merged files (production 1), read in the WCTEReadoutWindows ROOT files and use the tank data to select particles of a given type and use those to study the charge deposited in the downstream ACTs.

import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import uproot
import ACT_PID_module as ACT_mod

run_number = 1893

file_name = f"/eos/experiment/wcte/data/2025_commissioning/processed_offline_data/production_v1_0/{run_number}/WCTE_merged_production_R{run_number}.root"

# Make an instance of the ACT analysis class, defined in ACT-PID_moodule.py
ana = ACT_mod.ACTAnalysis(input_files=[file_name])

#print the run information for this run, obtained from the merged file
print(ana.get_run_info(run_number))

# Apply Sahar's ring-finding algorithm to produce for each trigger the charge deposited inside and outside the expected Cherenkov ring


# Apply a 2D cut on the charge deposited in the tank (inside and outside the ring) to make a muon sample


# Plot the charge depositied in ACT35 for events in the muon sample  


# Read in the default ACT02 and ACT35 cut lines and poton TOF cut line from the VME beam anlysis 


# Apply the ACT02 cut to the data to tag electrons and non-electrons


# Apply the proton TOF cut to remove protons from the sample 


# Plot the ACT35 distribution of the resulting sample of non-electrons, non-protons (i.e. muons and pions)


# Scale the ACT35 distribution obtained for the tank muon so that the muon peak is as high as its value in the non-electron sample (from the VME beam selection). Plot this.


# Substract the scaled muon distribution from the non-electron distribution to obtain the pion distribution. Plot this.


# Scale the pion distribution to the pion peak in the scaled muon-like sample (from the tank) adn subtract the scaled pion distribution from the tank muon one to get a pure distribution of muons. 

# Do the same for the electrons 

# Calculate the efficiency and purity of the muon/pion selection as a function of the cut on ACT35 

# Produce the likelihood distribution for each particle

##### Comapre with the VME analysis ##########

# Apply the default cut lines to the ACT charge distributions for all events to make the VME-based muon sample 


# Overlay the ACT35 charge for VME-tagged muons and tank-tagged muons    

#### Further validations #############