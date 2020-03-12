from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "simulator2020",
    version = "1.0.0",
    author = "GT IEEE Robotics",
    author_email = "ieee_president@gmail.com",
    description = ("The simulation environment for the 2020 SoutheastCon robotics competition."),
    url = "https://github.com/GT-IEEE-Robotics/Simulator2020",
    py_modules=['sim'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    install_requires=['numpy',
                      'pybullet>=2.6.6']
)