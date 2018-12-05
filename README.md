# Attack-Resilient Supervisory Control of Discrete Event Systems
This repository includes the implementation of supervisors for discrete event systems againt several types of attacks.
## Installation
### Dependencies
 - ```Python``` (=2.7)
 - ```OpenFst```(>=1.6.1) with ```pywrapfst``` module
 
The examples in this repository also require the following libraries for visualization.
 - ```Jupyter``` (>=1.0)
 - ```Graphviz```(>=2.36)
### Ubuntu 18.04
You can install the ```OpenFst``` and ```Graphviz``` libraries from the Ubuntu repository:
```
sudo apt install libfst-dev graphviz
```
and you can install ```Jupyter``` and the Python wrapper for ```OpenFst``` using ```pip```. The version ```openfst==1.6.1``` is currently the only version compatible with ```libfst-dev```.
```
pip install jupyter openfst==1.6.1
```
### Other Operating Systems
You need to compile the ```OpenFst``` library with ```--enable-python``` option. Visit the website http://www.openfst.org for details.
