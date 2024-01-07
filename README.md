# New insights on the Stokes paradox 

This repo contains code used to generate the figures and results in [*New Insights on the Stokes Paradox for Flow in Unbounded Domains*]([https://arxiv.org/pdf/2301.00039.pdf](https://trebuchet.public.springernature.app/get_content/779d0e10-e068-464d-8230-0e72eadc58c4?utm_source=rct_congratemailt&utm_medium=email&utm_campaign=nonoa_20240106&utm_content=10.1140/epjp/s13360-023-04804-6)) by Ingeborg Gjerde and Ridgway Scott.

![image](https://github.com/IngeborgGjerde/stokes-paradox/assets/12695403/b89c0668-60be-4bc1-b92e-4f1daa179b0d)

For the results in Figure 1, we refer to the [repo](https://github.com/IngeborgGjerde/nitsche-method-for-navier-stokes-with-slip) on Nitsche's method for slip boundary conditions.

## Dependencies

Simulations were performed using `FEniCS`, with [`mshr`](https://bitbucket.org/fenics-project/mshr/) for meshing and `octave`/`matplotlib` for plotting.

## Install

To run the FEniCS scripts 
```
conda create -n fenicsproject -c conda-forge fenics mshr
source activate fenicsproject
```

## Usage

The simulations for Figure 4 were generated using `triparadok.py` for the no-slip boundary conditions,
and `navitripdok.py` for the slip boundary conditions. The results are collected and plotted in the octave scripts `tripara.m`, and`navitrip.m`, respectively.

Figure 5 was generated using `ploteffpee.m`. It requires an input "tol" which is an input to the code `effprimestopar.m` which computes the data for the individual curves in Figure 5. 
The other input to `effprimestopar.m` is the value "b" indicated in Figure 5. The input "tol" is used to control the number of data points in the plot.
