# MarOMarker
This is the code for the software MarOMarker (Marine Organism Marker).
It provides options to annotate marine organisms on photos with the optional help of a 
neural network.
It was developed within the scope of Yvonne Jenniges' Master Thesis
[Semiautomatic Detection and Measurement of Marine Life on Underwater Stereoscopic Photographs Using a CNN (2021)](https://www.informatik.uni-bremen.de/agebv2/downloads/published/jenniges_thesis_21.pdf).


## Documentation
The software documentation was done with Sphinx using the numpydoc docstring
format. It is located in the folder **documentation**. For opening the main page,
open **documentation/build/index.html**.
If you change code, please maintain the comments in the code and update the 
documentation. 
For building the docs, navigate to the documentation directory and run (possibly first 
**make clean** to clean up old build, then)
**make html**.


## MarOMarker Installation Guide
The software comes along with an **MarOMarker.exe** file for Windows computers that I can 
provide on request. 
An installer is not yet provided. To run the software, run the file
**MarOMarker/src/build/dist/MarOMarker.exe**. 

*Remark:* 
Due to DLL dependencies of tensorflow, a redistributable of Visual Studio 
2015, 2017 and 2019 needs to be installed. Simply download and install a redistributable from
https://support.microsoft.com/de-de/help/2977003/the-latest-supported-visual-c-downloads

*For developers:*
The software runs on Python 3.11+ (tested with 3.13). Set up an
environment and install the package (editable, so code changes take
effect immediately):

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

The neural network training code lives in a separate repository:
https://github.com/y-jenniges/fish_detection


## General Remarks For MarOMarker Software Usage 
Sometimes patience is required. Since threading and progress bars are not 
implemented yet, feedback about the expected waiting time is missing. Longer
waiting times will occur in the following cases:
	- Loading a neural network
	- Predicting images with the neural network
	- Rectifying images and matching animals
	- If a network is loaded, the program is closed and then restarted 
	(when restarting, the network will be reloaded too)

Please make sure that you select a date AND and output directory when starting
a session. There is no error message yet preventing from usage if one of the 
settings is not set. This might cause a program crash.

As neural network, you can use one of the highRes networks.


### Example Usage 
The folder **MarOMarker/example_usage** contains the files used for the final 
usability test. Here, you find example images, an output directory, a neural 
network and a camera configuration. All necessary files to experimentally test the 
software are provided there. 


## Camera Configuration
The CSV camera configuration file, that is loadable and manipulable within the software,
is up until now only a dummy for being loaded into the program. 
The actual calculations are carried out with the **config.json** file. 


## Logo
The MarOMarker logo is taken from PowerPoint. It is available for free usage. 