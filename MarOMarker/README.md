# MarOMarker
This is the code for the software MarOMarker (Marine Organism Marker).
It provides options to annotate marine organisms on photos with the optional help of a 
neural network.
It was developed within the scope of Yvonne Jenniges' Master Thesis
[Semiautomatic Detection and Measurement of Marine Life on Underwater Stereoscopic Photographs Using a CNN (2021)](https://www.informatik.uni-bremen.de/agebv2/downloads/published/jenniges_thesis_21.pdf) and 
later refined. 

## Documentation (Sphinx)
For opening the main page, open **documentation/build/index.html**.
If you change code, please maintain the comments and numpydoc docstrings in the code and update the 
docs. 

For building the docs, navigate to the documentation directory and run (possibly first 
**make clean** to clean up old build, then)
**make html**.


## MarOMarker Installation Guide
The software comes along with an **MarOMarker.exe** file for Windows computers (provided on request). 
An installer is not yet provided. 
To run the software, run the file
**MarOMarker/src/build/dist/MarOMarker.exe**. 

*Remark:* 
Due to DLL dependencies of tensorflow, a redistributable of Visual Studio needs to be installed. Simply download and install a v14 redistributable from
https://learn.microsoft.com/de-de/cpp/windows/latest-supported-vc-redist?view=msvc-170

*For developers:*
The software runs on Python 3.11+ (tested with 3.13). Set up an
environment and install the package:

```
python -m venv .venv
.venv\Scripts\pip install -e .
```

Then start the program in any of these equivalent ways:

```
maromarker
python -m maromarker
```

Run the tests with:

```
.venv\Scripts\pip install -e .[test]
.venv\Scripts\pytest
```

The neural network training code lives in a separate folder of this repository.


## General Remarks For MarOMarker Software Usage 
Sometimes patience is required. Longer
waiting times can occur in the following cases:

	- Loading a neural network
	- Predicting images with the neural network
	- Rectifying images and matching animals
	- If a network is loaded, the program is closed and then restarted 
	(when restarting, the network will be reloaded too)

Please make sure that you select a date AND and output directory when starting
a session. There is no error message yet preventing from usage if one of the 
settings is not set. This might cause a program crash.


### Example Usage 
The folder **MarOMarker/example_usage** contains all necessary files to test the software.
Here, you find example images, an output directory, a neural 
network and a camera configuration.


## Logo
The MarOMarker logo is taken from PowerPoint. It is available for free usage. 