# SMD pads for kicad
A footprint library to bind standard connectors to smd pads of various shapes. 
Useful to solder wires on.
![img.png](img/photo1.png)
![img.png](img/photo2.png)

# Naming convention
Pads are named as follows:
```
smdpad_<numpinX>x<numpinY>_<witdth_mm>_<height_mm>_<spacing_mm>
```

# Generation
All footprints are generated using a python3.7+ script `generate.py`
Install the dependencies in requirements.txt and run the script, you're done.