# ICRP Dosimetry Simulation

ICRP Adult Female Phantom dosimetry simulation using opengate 10 (Tc99m kidney)

## Overview
Monte Carlo simulation of Tc-99m kidney dosimetry using the ICRP Publication 110 
Adult Female reference computational phantom and opengate 10.

## Pipeline
1. ICRP AF phantom loading (Analyze format)
2. Kidney source mask generation
3. Monte Carlo simulation (Tc99m, 140 keV)
4. Dose distribution visualization

## Requirements
- opengate 10
- SimpleITK
- matplotlib
- scipy

## Usage
```bash
python make_kidney_source.py   # generate kidney source mask
python simulation.py           # run simulation
python visualize.py            # visualize results
```

## Results
Dose distribution in ICRP AF phantom with Tc99m kidney source.

![Dose Map](output/dose_map.png)
