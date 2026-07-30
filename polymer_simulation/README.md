Coarse-grained polymer simulations with DL_POLY

This folder contains the files required to run the coarse-grained DL_POLY simulations of the UDG N-terminal tail presented in Figure 2 of the associated article.

Folder contents
CONTROL: defines the DL_POLY simulation conditions and run parameters.
CONFIG: contains the initial configuration of the coarse-grained system, including the simulation box and particle coordinates.
FIELD: defines the coarse-grained particles and their interactions, including masses, charges, bonds, angles, and non-bonded potentials.
dist.f: small Fortran analysis program used to calculate the statistics of the quantities plotted in Figure 2.


Running the simulations
Place CONTROL, CONFIG, and FIELD in the DL_POLY working directory.
Run DL_POLY using these three input files.
Compile the dist.f program with a compatible Fortran compiler.
Use the compiled program to analyse the simulation output and calculate the statistics reported in Figure 2

The exact simulation parameters, initial coordinates, particle properties, and interaction potentials are defined directly in CONTROL, CONFIG, and FIELD.
