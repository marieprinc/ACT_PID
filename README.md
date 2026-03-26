# ACT_PID

Repository to study particle identification (PID) using ACT charge distributions and tank data from WCTE readout windows.

This repository is targeted at ACT PID taskforce members (Bruno, Marie, Viet, Alie) and provides a lightweight analysis prototype for:
- selecting muons/pions/electrons from WCTE merged ROOT files,
- comparing ACT and tank-based taggers,
- estimating efficiency/purity from ACT charge histograms,
- producing PDF summaries per run.

## Repository structure

- `python/ACT_PID_analysis.py`: driver script for one run; reads a ROOT file, instantiates `ACTAnalysis`, and prints run info.
- `python/ACT_PID_module.py`: core `ACTAnalysis` class; data loading + analysis method stubs + example high-momentum algorithm.
- `output/`: expected output location for per-run PDF plots (e.g. `ACT_PID_run_<run>.pdf`).

## Requirements

- Python 3.8+
- numpy
- pandas
- matplotlib
- uproot

Install with:

```bash
pip install numpy pandas matplotlib uproot
```
(should not be needed on the CERN clusters)

## Quick start

1. Set `run_number` in `python/ACT_PID_analysis.py`.
2. Confirm the ROOT path is valid (example path in the script):
   `/eos/experiment/wcte/data/2025_commissioning/processed_offline_data/production_v1_0/<run>/WCTE_merged_production_R<run>.root`
3. Create output directory if needed:

```bash
mkdir -p output
```

4. Run:

```bash
python3 python/ACT_PID_analysis.py
```

5. Expected output:
   - printed run info on console
   - currently placeholder for plots and save to `output/ACT_PID_run_<run>.pdf` from `ACTAnalysis.load_data()`.

## What the code does

### `python/ACT_PID_module.py`

`ACTAnalysis` class:

- `__init__(self, input_files)`: store input file names, init data structures, call `load_data()`.
- `load_data(self)`: for each input ROOT file:
  - read `WCTEReadoutWindows` tree with branches (temporary):
    - `vme_evt_quality_bitmask`
    - `vme_digi_issues_bitmask`
    - `vme_act_tagger`
    - `vme_act_eveto`
    - `vme_mu_tag_l_charge`
  - read `vme_analysis_run_info` tree into run metadata holding information about the run, the momentum and refractive index of the ACTs
  - open a `PdfPages` file `../output/ACT_PID_run_<run_number>.pdf` per run
- `get_run_info(self, run_number)`: return run metadata DataFrame matching run number.

Placeholder methods to implement:
- `apply_ring_finding_algorithm()`
- `select_muon_sample_tank()`
- `plot_act35_charge()`
- `read_cut_lines()`
- `apply_cuts()`
- `plot_non_electron_non_proton_distribution()`
- `scale_and_plot_distributions()`
- `calculate_efficiency_purity()`
- `produce_likelihood_distributions()`

`high_momentum_analysis_example(self)` implements an end-to-end histogram-based extraction of muon/pion components and efficiency/purity curves using ACT35 charge and muon tagger cuts. This is very dirty copy-paste from Alie's high momentum analysis, will have to be re-written cleanly.

### `python/ACT_PID_analysis.py`

- sets `run_number` and `file_name` for one run
- builds `ACTAnalysis(input_files=[file_name])`
- prints run metadata
- currently has comments describing desired analysis pipeline steps (ring finding, 2D cuts, ACT02/ACT35 + TOF cuts, distribution scaling, likelihood
  calculation, comparisons)

## Analysis workflow (suggested implementation)

1. Add ring finding code into `apply_ring_finding_algorithm()` using tank charge data.
2. Implement muon selection in `select_muon_sample_tank()` (2D tank inside/outside cut).
3. Implement ACT35 charge plotting and distribution extraction.
4. Load ACT02 / proton TOF cuts in `read_cut_lines()` using VME beam analysis lines.
5. Apply filtering cuts in `apply_cuts()`.
6. Compute separate distributions and scale in `scale_and_plot_distributions()`.
7. Calculate efficiency/purity and likelihoods in `calculate_efficiency_purity()` and `produce_likelihood_distributions()`.
8. Save all figures through `PdfPages` objects in `self.pdfs`.

## Notes

- Keep `output` relative path consistent with module code (`../output`). Running script from `ACT_PID/python` may create `ACT_PID/output` via relative path.
- The code is currently a skeleton with key algorithm in `high_momentum_analysis_example` and should be refactored into modular methods.
- Add unit tests or analysis notebooks as needed for reproducibility.

