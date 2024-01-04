# New insights on the Stokes paradox 

This repo contains code used to generate the figures and results in the manuscript [New Insights on the Stokes Paradox for Flow in Unbounded Domains](https://arxiv.org/pdf/2301.00039.pdf) by Ingeborg Gjerde and Ridgway Scott.


![image](https://github.com/IngeborgGjerde/stokes-paradox/assets/12695403/b89c0668-60be-4bc1-b92e-4f1daa179b0d)


The two octave codes plot codes
- `tripara.m`
- `navitrip.m`
in Figure 4.
The data in these files was generated using the dolfin python codes
- `triparadok.py`
- `navitripdok.py`
respectively.

The code
- `ploteffpee.m`
plots Figure 5. It requires an input "tol" which is an input to the code effprimestopar.m which computes the data for the individual curves in Figure 5. 
The other input to `effprimestopar.m` is the value "b" indicated in Figure 5. The input "tol" is used to control the number of data points in the plot.
