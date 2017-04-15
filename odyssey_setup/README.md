# Setup mpi and pymc3 for Odyssey

The setup directory contains a slurm script which will create a custom conda environment (cs205project) and install mpi4py and pymc3. The setup script takes about 20 minutes to run.

You can switch to the custom environment with the following command:
````
source activate cs205project
````

The mpi4py_test directory contains the demo mpi4py application from
[fasrc](https://www.rc.fas.harvard.edu/resources/documentation/software-development-on-odyssey/mpi-for-python-mpi4py-on-odyssey/). Note that version 2.7.6 of python has mpi4py preinstalled, so you actually don't need any setup to run this.

The pymc3_mpi_test directory contains a parallel sampler with mpi4py and pymc3. This code requires first creating the cs205project environment.

A known issue is that theano only supports 1 compilation for the cache at a time, so you get a get a bunch of locking warnings in the output if a model is not yet in the cache.