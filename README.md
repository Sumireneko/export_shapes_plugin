## About Export shapes as SVG plug-in 
Export save selected shapes on Vector Layer as each SVG files.
This plug-in work on Krita 5.2.2

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

### Update hitroy
2024.05.25 v0.2 First Release
