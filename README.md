## About Export shapes as SVG plug-in v0.3
Export save selected shapes on Vector Layer as each SVG files.
Tested with Krita v5.2.14(PyQt5 with Python 3.13)

* Export one SVG file per selected one shape
* The translate function of the shape transform attribute reset to 0 0
* The translate component in the matrix of transform attribute reset to 0 0
* SVG viewport create around the shape
* If extreme transform(shear or rotation) are applied, parts of the shape will extend outside the viewport.
* Support GroupShape
* Support Text shape


### Where the command find?
* The menu,Layer → Export → Save selected shapes as SVGs...


### How to Use

* Select shapes and use this command.
* File Selector opend,decide the file name and Choose Save Folder.
* Save SVG file with name with increment number and with .svg extension.
* Notification dialog will appear in center when all finished (disappears it soon)  
For example,set a named "file.svg",Then export a following

> file0.svg  
> file1.svg  
> file2.svg  
>   :  
>   :  

### Update histries
2025.10.19 v0.3
- Preliminary PyQt6 compatibility added Updated import logic to support PyQt6 for future Krita 6.x compatibility.
- Note: PyQt6 functionality has not been tested yet. This change is preparatory and not guaranteed to be stable.
2024.05.25 v0.2 First Release
