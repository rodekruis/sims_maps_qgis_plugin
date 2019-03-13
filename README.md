## SIMS Maps QGIS plugin

This plugin will make life easier for those who need to make RCRC SIMS maps. It will help getting the layout done in
a fast and consistent way. The plugin will run in QGIS3 versions from 3.4.0 and up.

## Setup development environment

* Clone this git repository
* Clone IFRC icon git repository in same directory: https://github.com/IFRCGo/IFRC-Icons
* Clone NS logos git repository in same directory: https://github.com/raymondnijssen/logos

```
path/to/git/
|--sims_maps_qgis_plugin/
|--IFRC-Icons/
|--logos/

```

* Run the generate_plugin script which will by default generate a directory with all the plugin content.
```python3 generate_plugin.py```

* Either copy this directory to your qgis3 plugin directory or create a symbolic link in your plugin directory:

```
cd /home/USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins
ln -s ~/git/sims_maps_qgis_plugin/sims_maps_generated/ sims_maps
```

* Start or restart QGIS3. Reload the plugin with the experimental "Plugin Reloader" plugin.


## License

Licensed under the terms of GNU GPL 2

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

## Manual

* The plugin add the SIMS colors to the standard QGIS color picker, for use
anywhere in QGIS.

* The plugin adds the OCHA 2012 and 2018 icons for use in an SVG symbology.

* The "Create SIMS Map Layout" button in the QGIS toolbar generates and opens a
layout based on chosen template. You can choose the NS logo, the plugin name and
the language.

* The "Edit Layout" button in the layout window allows you to easily change
label settings like title, date and project codes.
