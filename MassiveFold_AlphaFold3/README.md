# MassiveFold/AlphaFold3 predictions

Predictions computed with [AlphaFold3](https://github.com/google-deepmind/alphafold3) through [MassiveFold](https://github.com/GBLille/MassiveFold) 1.6.2.

## Data

All the data are available [here](https://nextcloud.univ-lille.fr/index.php/s/dig6T76WNsY7mpx). The folder contains 4 sets:
- `8VLR_UNG2_7-30.tar.gz`: the 8VLR nucleosome with 7-30 UDG peptides
- `8VLR_UNG2_7-30_AAA.tar.gz`: the 8VLR nucleosome with 7-30 UDG peptides, the RKR motif being mutated to AAA
- `8VLR_UNG2.tar.gz`: the 8VLR nucleosome with full UDG
- `8VLR_UNG2_AAA.tar.gz`: the 8VLR nucleosome with full UDG, the RKR motif being mutated to AAA

Each set contains 1000 predictions (200 seeds * 5 samples), confidences, light pickles as defined on the MassiveFold git repository, the plots of the PAE matrices of the 10 first ranked predictions (more can be computed with [this script](https://github.com/GBLille/MassiveFold/blob/main/src/massivefold/massivefold_plots.py)), JSON files used by AlphaFold3, templates used, alignments and a `ranking.csv` file which contains the main scores for each prediction.

## Scripts

This folder contains a script used to compute the RMSD between 1EMH and the predictions and two scripts to compute the number of times the arginine anchor (or AAA mutated residues) binds to the acidic patch, one for peptides and one for full UDG. These scripts have to be run on the folders listed before, that contain the predictions (cif files).

