# GT IEEE Robotics: Simulator 2020
A simulator for the IEEE SoutheastCon 2020 Competition. It is to be used by the other teams to test their code before a working robot is made. Because of its design goal, this project will frequently reference the official SoutheastCon 2020 GitHub: [github.com/ncgadgetry/southeastcon2020](https://github.com/ncgadgetry/southeastcon2020).

## How to Run

```
$ conda activate sim2020
$ python main.py
```

If you don't have a conda environment, first install miniconda, then:
```
$ conda create --name hardware_sim PYTHON=3.7.1
$ conda activate sim2020
$ pip install numpy pybullet
```

## How to Run Tests

```
$ pytest tests
```

## Directory
 * /simulator
   * Buttons - The Buttons class maintains the state of pressable buttons on the left wall
   * Field - The Field class maintains the state of the simulated elements within the field
   * Game - Maintains and coordinates the game loop
   * Utilies - Utility class to convert between units of measure
 * /test
   * test_buttons

## Components
This project has no functional components for now.

## To Do
* A `Util` class for unit and baisis conversions
* A `PlayField` class to model the field
* A `ButtonControl` class to model the button pushes based on the Arduino code
