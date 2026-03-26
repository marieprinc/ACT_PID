#This is the anlaysis module containing the code necessary to perform the ACT PID checks using the WCTE tank data. 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot

from matplotlib.backends.backend_pdf import PdfPages


#This code should be cleaner than the WCTE beam anlaysis code, we want to keep it usable by everyone confidenty 
class ACTAnalysis:
    def __init__(self, input_files):
        self.input_files = input_files
        self.dataframes = []
        self.run_infos = []
        self.pdfs = {}
        self.load_data()
        

    def load_data(self):
        for input_file in self.input_files:
            with uproot.open(input_file) as f:
                tree = f["WCTEReadoutWindows"]
                #only select a few branches to speed up the loading
                branches = ["vme_evt_quality_bitmask","vme_digi_issues_bitmask", "vme_act_tagger","vme_act_eveto", "vme_mu_tag_l_charge"]    
                df = tree.arrays(branches, library="pd")
                self.dataframes.append(df)

        for input_file in self.input_files:
            with uproot.open(input_file) as f:
                run_info = f["vme_analysis_run_info"]
                run_info_df = run_info.arrays(library="pd")
                self.run_infos.append(run_info_df)


        #for each run store the plots in the pdf corresponding to that run, with the name "ACT_PID_run_{run_number}.pdf"
        for run_info in self.run_infos:
            run_number = run_info["run_number"].iloc[0]
            self.pdfs[run_number] = PdfPages(f"../output/ACT_PID_run_{run_number}.pdf")

    def get_run_info(self, run_number):
        for run_info in self.run_infos:
            if run_info["run_number"].iloc[0] == run_number:
                return run_info
        return None
        

    def apply_ring_finding_algorithm(self):
        # Placeholder for Sahar's ring-finding algorithm
        pass

    def select_muon_sample_tank(self):
        # Placeholder for 2D cut on charge deposited in the tank
        pass

    def plot_act35_charge(self):
        # Placeholder for plotting charge deposited in ACT35 for muon sample
        pass

    def read_cut_lines(self):
        # Placeholder for reading default cut lines from VME beam analysis
        pass

    def apply_cuts(self):
        # Placeholder for applying ACT02 and proton TOF cuts
        pass

    def plot_non_electron_non_proton_distribution(self):
        # Placeholder for plotting ACT35 distribution of non-electron, non-proton sample
        pass

    def scale_and_plot_distributions(self):
        # Placeholder for scaling and plotting distributions
        pass

    def calculate_efficiency_purity(self):
        # Placeholder for calculating efficiency and purity of muon/pion selection
        pass

    def produce_likelihood_distributions(self):
        # Placeholder for producing likelihood distributions for each particle type
        pass













# -----------------------------------------------------------
    def high_momentum_analysis_example(self):
        #This is a dirty copy-paste of Alie's high momentum analysis code to show and example approach of this analysis

         ############## Estimate the likelihood using the muon tagger cut distribution

            fig, ax = plt.subplots(figsize = (8, 6))
            bins = np.linspace(0, 80, 110)

            #make the event masks to identify events which pass the mu tag cut and are muons and pions
            if self.run_momentum > 300:
                mask_muons_pions = (self.df["is_electron"] == 0) & (self.df["tof"] < self.proton_tof_cut)
            else:
                mask_muons_pions = (self.df["is_electron"] == 0)
            mask_pass_mu_tag = (self.df["mu_tag_total"] > self.mu_tag_cut)
            #both (muons or pion) and passing muon tag 
            mask_both = mask_muons_pions & mask_pass_mu_tag


            h, _, _ = ax.hist(self.df["act_tagger"][mask_both],  histtype = "step", bins = bins, label = f"All Muon or pions above mu_tag cut ({sum(mask_both)}) events")
            h_all, _, _ = ax.hist(self.df["act_tagger"][mask_muons_pions],  histtype = "step", bins = bins, label = f"All Muon or pions: ({sum(mask_muons_pions)}) events")
            

            #Weight up the events passing the muon tagger cut so the maximas align (the muon peak)
            bin_centers = 0.5 * (bins[:-1] + bins[1:])
            x_min = 10
            x_max = 30
            mask = (bin_centers >= x_min) & (bin_centers <= x_max)
            # Find the bin index with the maximum count in that range
            max_index = np.argmax(h_all[mask])

            index = np.where(mask)[0]
            idx_muon_peak = index[max_index]
            muon_scale = h_all[idx_muon_peak]/h[idx_muon_peak]

            #create a new histogram of the distibution passing the muon tagger cut scaled up to the muon peak
            h_muon_scaled = h * muon_scale
            
            
                  
            # plot the scaled histogram 
            ax.step(bin_centers, h_muon_scaled, where='mid', label=f"Mu/pi above cut scaled to muon peak ({sum(h_muon_scaled):.1f}) events")
            
            ### look at electrons
            n_electrons = sum(self.df["is_electron"])
            h_electron, _, _ =  ax.hist(self.df["act_tagger"][self.df["is_electron"] == 1],  histtype = "step", bins = bins, label = f"Tagged electrons ({n_electrons:.1f}) events")
            
            
            #### here, get the difference between the all and the scaled one
            h_all_minus_h_scaled = h_all - h_muon_scaled
            
            
             #clip that difference to be positive
            h_all_minus_h_scaled = h_all_minus_h_scaled.clip(0)
            
            #split the leftovers into electron (after the mu peak) and pions (before the muon peak)
            h_all_minus_h_scaled_pion = np.where(bin_centers<bin_centers[idx_muon_peak], h_all_minus_h_scaled, 0)
            
            h_all_minus_h_scaled_electron = np.where(bin_centers>=bin_centers[idx_muon_peak], h_all_minus_h_scaled, 0)
            
            ax.step(bin_centers, h_all_minus_h_scaled_pion,  where = 'mid', label = f"Pion-like distribution")

            
            h_pion = h_all_minus_h_scaled_pion

            ax.set_yscale("log")
            # ax.set_xlim(0, 80)
            ax.set_xlabel("ACT35 charge (PE)")
            ax.set_ylabel("Number of triggers")
            ax.legend()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c)", fontsize = 20)
            ax.grid()
#             self.pdf_global.savefig(fig)
            plt.close()
#             return 0
            
            
            #################### Once we have the distribution, remove the pion contamination 
            fig, ax = plt.subplots(figsize = (8, 6))
            
            ax.step(bin_centers, h_muon_scaled, where='mid', color = "black", label=f"Mu/pi above cut scaled to muon peak", linewidth = 4)
            
            ax.step(bin_centers, h_pion, where = 'mid', color = "magenta", label = f"Pion-like distribution")
            
            
            
            pion_scalling = h_muon_scaled[0]/h_pion[0] 
            h_pion_scaled = h_pion * pion_scalling
            
            ax.step(bin_centers, h_pion_scaled, where='mid', label=f"Pion distr. scaled to Mu/pi above mutag cut bin 0")
            
            h_muon = h_muon_scaled - h_pion_scaled
            h_muon = h_muon.clip(0)
            
            ax.step(bin_centers, h_muon, where='mid', label=f"Mu/pi above mutag cut bin 0 minus scaled pion distr. => muon population")
            
            
            ax.set_yscale("log")
            # ax.set_xlim(0, 80)
            ax.set_xlabel("ACT35 charge (PE)")
            ax.set_ylabel("Number of triggers")
            ax.legend()
            ax.grid()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c)", fontsize = 20)
#             self.pdf_global.savefig(fig)
            plt.close()
            
            ###############################################################################
            ############ Calculate effiency and purity as a function of the cut line
            h_pion_tot = h_pion + h_pion_scaled
            h_muon_tot = h_muon
            
            fig, ax = plt.subplots(figsize = (8, 6))
            
            ax.step(bin_centers, h_pion_tot, where='mid', color = "magenta", label=f"Total number of pions")
            ax.step(bin_centers, h_muon_tot, where='mid', color = "green", label=f"Total number of muons")
            
            ax.set_yscale("log")
            ax.set_xlabel("ACT35 charge (PE)")
            ax.set_ylabel("Number of triggers")
            ax.legend()
            ax.grid()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c)", fontsize = 20)
            plt.close()
            
            ###### for my own sanity
            n_pions_left = [sum(h_pion_tot[:b]) for b in range(len(bin_centers))]
            n_muons_left = [sum(h_muon_tot[:b]) for b in range(len(bin_centers))]
            
            n_pions_right = [sum(h_pion_tot[b:]) for b in range(len(bin_centers))]
            n_muons_right = [sum(h_muon_tot[b:]) for b in range(len(bin_centers))]
            
            fig, ax = plt.subplots(figsize = (8, 6))
            ax.step(bin_centers, n_pions_left, where='mid', color = "magenta", label=f"Number of pions on the left of the cut line")
            ax.step(bin_centers, n_muons_left, where='mid', color = "green", label=f"Number of muons on the left of the cut line")
            
            ax.step(bin_centers, n_pions_right, where='mid', linestyle = "--", color = "magenta", label=f"Number of pions on the right of the cut line")
            ax.step(bin_centers, n_muons_right, where='mid', linestyle = "--", color = "green", label=f"Number of muons on the right of the cut line")
            
            ax.set_yscale("log")
            ax.set_xlabel("ACT35 charge (PE)", fontsize = 12)
            ax.set_ylabel("Number of triggers", fontsize = 12)
            ax.legend()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c)", fontsize = 20)
            ax.grid()
            plt.close()
            
            ##### rejection factors function of efficiency 
            n_pions_left = np.array([sum(h_pion_tot[:b]) for b in range(len(bin_centers))])
            n_muons_left = np.array([sum(h_muon_tot[:b]) for b in range(len(bin_centers))])
            
            n_pions_right = np.array([sum(h_pion_tot[b:]) for b in range(len(bin_centers))])
            n_muons_right = np.array([sum(h_muon_tot[b:]) for b in range(len(bin_centers))])
            
            pion_efficiency = n_pions_left/sum(h_pion_tot)
            muon_efficiency = n_muons_right/sum(h_muon_tot)
            
            #number of pions rejected per muon accepted in the pion selection (i.e. left)
            muon_rejection = n_muons_right/n_muons_left
            #number of muons rejected per pion accepted in the in muon selection (i.e. right)
            pion_rejection = n_pions_left/n_pions_right
            
            #Purity calculations
            pion_purity = n_pions_left/(n_pions_left+n_muons_left)
            muon_purity = n_muons_right/(n_pions_right+n_muons_right)
            
            
            fig, ax = plt.subplots(figsize = (8, 6))
            ax.plot(pion_efficiency, muon_rejection, marker = "x", color = "magenta")
            
            ax.set_yscale("log")
            ax.set_ylim(0.5, None)
            
            ax.set_xlabel("Pion selection efficiency", fontsize = 12)
            ax.set_ylabel("# mu rejected per mu in sample", fontsize = 12)
            ax.grid()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c)", fontsize = 20)
            plt.close()
            
            fig, ax = plt.subplots(figsize = (8, 6))
            ax.plot(muon_efficiency, pion_rejection, marker = "x", color = "green")
            
            ax.set_yscale("log")
            ax.set_ylim(0.5, None)
            ax.set_xlabel("Muon selection efficiency", fontsize = 12)
            ax.set_ylabel("# pi rejected per pi in sample", fontsize = 12)
            ax.grid()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c)", fontsize = 20)
            plt.close()
            
            
            fig, ax = plt.subplots(figsize = (8, 6))
            ax.step(bin_centers, pion_purity, where='mid', color = "blue", label = "pion purity")
            ax.step(bin_centers, pion_efficiency, where='mid', color = "red", label = "pion efficiency")
            
            ax.set_xlabel("Cut line in ACT35 (PE)", fontsize = 12)
            ax.set_ylabel("")
            ax.legend()
            ax.grid()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c) - Pions", fontsize = 20)
            plt.close()
            
            fig, ax = plt.subplots(figsize = (8, 6))
            ax.step(bin_centers, muon_purity, where='mid', color = "blue", label = "muon purity")
            ax.step(bin_centers, muon_efficiency, where='mid', color = "red", label = "muon efficiency")
            ax.grid()
            
            ax.set_xlabel("Cut line in ACT35 (PE)", fontsize = 12)
            ax.set_ylabel("")
            ax.legend()
            ax.grid()
            
            ax.set_title(f"Run {self.run_number} ({self.run_momentum} MeV/c) - Muons", fontsize = 20)
            plt.close()


