# GT IEEE Robotics: Simulator 2020
A simulator for the IEEE SoutheastCon 2020 Competition. It is to be used by the other subteams to test their code before a working robot is made.

## How to Run

If you don't have a conda environment, first install miniconda, then:
```
$ conda create --name southeastcon2020 PYTHON=3.7.1
$ conda activate southeastcon2020
$ pip install -e .
```
Note, the last line should run in the `Simulator2020/` folder.

Remember to activate the env with: `conda activate southeastcon2020`. Now visit the `examples\` to run any of the samples.


## How to Test

```
$ pytest tests
```


## How to Develop

Loop at `sim.py` to see the functions exposed to outside packages.
