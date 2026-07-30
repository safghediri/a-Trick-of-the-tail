# A trick of the tail: electrostatic localization of UDG on nucleosomes

This repository contains the computational data, structural models, input files, scripts, and calculation protocols associated with the study:

S. Ghediri, G. Brysbaert, F. Cleri and R. Blossey, “A trick of the tail: how electrostatics helps a DNA repair enzyme to localize on nucleosomes.”

The study investigates whether the positively charged RKR motif in the N-terminal tail of human uracil-DNA glycosylase (UDG) may interact with the negatively charged acidic patch of the nucleosome.

The repository is divided into four sections. Each folder contains a separate README with more detailed information.

MassiveFold and AlphaFold3

The MassiveFold_AlphaFold3 folder contains the files related to the structural predictions performed with AlphaFold3 through MassiveFold.

These calculations include predictions of the nucleosome with the RKR-containing UDG peptide and predictions of the full UDG–nucleosome complex. The folder contains the available input files, predicted structures, ranking information, and analysis procedures.

Electrostatic analysis

The electrostatics folder contains the structural models and protocols used to analyse the charge distribution and electrostatic potential of UDG and its N-terminal tail.

The folder includes the PDB2PQR structure-preparation procedure, APBS and DelPhi calculation protocols, EMBOSS/CIDER tail-charge analysis, and the Chimera visualization procedure.

Peptide scoring

The peptide_scoring folder contains the files used to compare the RKR-containing region of the UDG tail with candidate acidic-patch-binding peptides.

The scoring procedure combines sequence similarity, the presence of a central basic motif, peptide charge, and serine/proline enrichment. The folder contains the scoring protocol, input peptide data, analysis script, and available results.

Coarse-grained polymer simulations

The polymer_simulation folder contains the DL_POLY files used for the coarse-grained simulations of the UDG N-terminal tail.

The simulations examine the effect of dielectric permittivity on the conformation and radius of gyration of the tail, as well as the interaction between its positively charged RKR region and a negatively charged nucleosome-like sphere.
