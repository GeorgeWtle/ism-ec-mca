# Observational constraints on global climate projections: An original method applied to changes in Indian summer monsoon rainfall - Code Repository

Code accompanying: [*exact citation to be determined*]

Authors: George Whittle [1, 2], Hervé Douville [1], Pascal Terray [2]

Corresponding author: George Whittle, george.whittle@meteo.fr, george.whittle@locean.ipsl.fr

[1]: Centre National de Recherches Météorologiques, Université de Toulouse, CNRS, Météo-France, Toulouse, France

[2]: Laboratoire d’Océanographie et du Climat: Expérimentations et Approches Numériques, Institut Pierre-Simon Laplace, Sorbonne Université/CNRS/IRD/MNHN, Paris, France

## Overview
This repository gives all code that was used to produce figures found in the paper. Data used can be found here: https://doi.org/10.5281/zenodo.21276650. Data should be downloaded to reproduce the figures.

## Repository structure
- `src/`: Contains all code for producing figures as well as needed utilities.
- `figures/`: Figures as .pdf format. All figures are produced with the associated python file in `src/` folder.
- `requirements.txt`: Packages requirements for producing the figures.

## Data
Data can be download here: https://doi.org/10.5281/zenodo.21276650. Data **must** be stored at the root directory.

## Installation
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproducing the results
**Activate the virtual environment.** All `fig*.py` files can be computed independently from the root directory to produce associated figure.

## Citation

https://doi.org/10.5281/zenodo.21276455

## License
MIT License (see `LICENSE` file).

## Contact
George Whittle, george.whittle@meteo.fr, george.whittle@locean.ipsl.fr