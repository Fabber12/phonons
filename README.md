Have you ever dreamed about computing phonons spectra using Neural Network potentials? Me neither, but here we are.

## Installation of the basic components

Prerequisites:
- GCC (tested for `GCC Version: 12.2.0`)
- MPI (tested for `(Open MPI) 4.1.2`)
- CUDA (tested for `CUDA Version: 12.6`)


Building all the software needed for this project is quite tricky. Let's go step by step:

1. After cloning/downloading, create a conda/mamba environment by running `conda env create -f environment.yml` and activate it by running `conda activate phonon`.
2. Download LibTorch to store locally from [https://pytorch.org/](https://pytorch.org/). It could look something like: `wget https://download.pytorch.org/libtorch/cu126/libtorch-shared-with-deps-2.6.0%2Bcu126.zip` . Unzip the file (you should get a folder called `libtorch`).
3. Clone/download MACE-compatible LAMMPS from: [https://github.com/ACEsuit/lammps](https://github.com/ACEsuit/lammps).
4. Build LAMMPS by running `build-lammps.sh`. Have a look at the file but do **not** change the CMake options, except for `KOKKOS_ARCH_` options to be consistent with your GPU architecture! Feel free to reduce the number of processes of `make` (the `-j` flag).
5. Create a modulefile. An example is provided in `phonons-modulefile`.
6. Load your modulefile and check that everything is working correctely by running `mpirun -np 2 python check-sanity.py`.


You should be good to go!

A few remarks:
- The script to build LAMMPS+Python+MACE is based on [https://mace-docs.readthedocs.io/en/latest/guide/lammps.html](https://mace-docs.readthedocs.io/en/latest/guide/lammps.html) and on my research project. Feel free to modify it, at your own risk!
- It seems to be **very** important to install `mpi4py` **before** installing LAMMPS Python API, otherwise it may not recognize the correct MPI backend, which will most surely lead to errors/bugs; `mpi4py` is in the conda environment, so there's should be no problem if you follow the instructions step-by-step.
- If for some reason you want to build LAMMPS+MACE for CPU (no GPU), make sure to download the correct LibTorch library and modify `build-lammps.sh` removing all the GPU stuff.

## Extras

### MACE

In order to use a MACE NNP potential in LAMMPS, one has first to convert a MACE 'pickled' `.model` model file into a Torch-readable `.pt` file, to then provide to LAMMPS `pair_style` command. You can do that by following the instructions here: [https://mace-docs.readthedocs.io/en/latest/guide/lammps.html](https://mace-docs.readthedocs.io/en/latest/guide/lammps.html). However, I would suggest **against** installing `mace-torch` and doing the convertion inside the same environment. You should build a separate environment where to install MACE and PyTorch (just make sure PyTorch is consistent, i.e. it's the same version for the same CUDA backend). Have a look at my other two repositories: [https://github.com/MicPellegrino/workflow-hea](https://github.com/MicPellegrino/workflow-hea), [https://github.com/MicPellegrino/benchmark-mace](https://github.com/MicPellegrino/benchmark-mace). **NB** unfortunately neither MACE nor PyTorch support conda installation, you can either use `pip` or clone the github/download the shared library.
