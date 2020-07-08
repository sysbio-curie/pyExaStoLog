![Python application](https://github.com/sysbio-curie/pyExaStoLog/workflows/Python%20application/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/sysbio-curie/pyExaStoLog/badge.svg?branch=master)](https://coveralls.io/github/sysbio-curie/pyExaStoLog?branch=master) [![PyPI version](https://badge.fury.io/py/exastolog.svg)](https://badge.fury.io/py/exastolog)

# pyExaStoLog : a python library for EXAct calculation of STOchastic LOGical models 

## Dependencies
[SuiteSparse](http://faculty.cse.tamu.edu/davis/suitesparse.html) and [SWIG](http://www.swig.org/) might be required to build the [scikit-umfpack](https://scikit-umfpack.github.io/scikit-umfpack/) python library.
    
To install them debian/ubuntu : 

    sudo apt install libsuitesparse-dev swig


## Install
#### From PyPi
    pip install exastolog
    
#### From your local clone
    git clone https://github.com/sysbio-curie/pyExaStoLog
    pip install pyExaStoLog

## Examples
- [Toy model](https://github.com/sysbio-curie/pyExaStoLog/blob/master/notebooks/Toy%20model.ipynb)
- [Toy model 2](https://github.com/sysbio-curie/pyExaStoLog/blob/master/notebooks/Toy2%20model.ipynb)
- [Toy model 3](https://github.com/sysbio-curie/pyExaStoLog/blob/master/notebooks/Toy3%20model.ipynb)
- [KRas 15 vars model](https://github.com/sysbio-curie/pyExaStoLog/blob/master/notebooks/KRas%20model.ipynb)
- [Cohen's model](https://github.com/sysbio-curie/pyExaStoLog/blob/master/notebooks/Cohen%20model.ipynb)
    
## Reference
Koltai, M., Noel, V., Zinovyev, A. et al. Exact solving and sensitivity analysis of stochastic continuous time Boolean models. BMC Bioinformatics 21, 241 (2020). https://doi.org/10.1186/s12859-020-03548-9

## License
    BSD 3-Clause License
