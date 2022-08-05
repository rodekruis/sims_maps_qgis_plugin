## SIMS Maps QGIS plugin

This plugin will make life easier for those who need to make RCRC SIMS maps. It will help getting the layout done in
a fast and consistent way. The plugin will run in QGIS3 versions from 3.4.0 and up.

## Installing the plugin

The plugin is not available in the standard QGIS plugin repository for safety reasons. (Not everyone should be able to simply make a Red Cross map.)

* Download the latest .zip file from the release directory: https://github.com/rodekruis/sims_maps_qgis_plugin/tree/master/releases
* Then open the Plugin Manager in QGIS and choose "Install from zip"
* Choose your local .zip and Install
* An extra button will appear in your QGIS toolbar: ![button icin](https://github.com/rodekruis/sims_maps_qgis_plugin/blob/master/sims_maps/create_layout_crystal.svg "button icon")  

## User Guide

* The plugin add the SIMS colors to the standard QGIS color picker, for use
anywhere in QGIS.

* The plugin adds the OCHA 2012 and 2018 icons for use in an SVG symbology.

* The "Create SIMS Map Layout" button in the QGIS toolbar generates and opens a
layout based on chosen template. You can choose the NS logo, the plugin name and
the language.

* The "Edit Layout" button in the layout window allows you to easily change
label settings like title, date and project codes.

---
**IMPORTANT NOTICE! This plugin is designed to function on single machines only!**

So, saving a project with SIMS layouts and reopening it on another machine will
probably result in broken links to layers and images, even if the plugin has been
installed on the other machine. A QGIS update could also result in problems on
the same machine, because the install path contains the version name.

We are currently working on an improvement that addresses the above, but the problem stems from QGIS itself and how it handles dataset file paths in the project file.
Thus it will need a change in the QGIS source code itself.

## Set up development environment

If you would like to contribute to this plugin you can set up the environment on your local device. This has only been tested on Linux.

* Clone this git repository
* Clone IFRC icon git repository in same directory: https://github.com/IFRCGo/IFRC-Icons
* Clone NS logos git repository in same directory: https://github.com/raymondnijssen/logos

```
path/to/git/
|--sims_maps_qgis_plugin/
|--IFRC-Icons/
|--logos/

```

* To create or update the .ts translation files based on the source code, run the generate_ts script. This will add newly added translatable strings to the .ts files for all languages. It will not clear already translated strings.
```python3 generate_ts.py```
New languages can be added by adding the country code to the languages list somewhere high up in the script:
```languages = ['nl', 'en', 'fr']```

* To create or update the .qm translation files based on every .ts file, run the generate_qm script.
```python3 generate_qm.py```

* Run the generate_plugin script which will by default generate a directory with all the plugin content.
```python3 generate_plugin.py```

* Either copy this directory to your qgis3 plugin directory or create a symbolic link in your plugin directory:

    ```bash
    cd /home/USER/.local/share/QGIS/QGIS3/profiles/default/python/plugins
    ln -s ~/git/sims_maps_qgis_plugin/sims_maps_generated/ sims_maps_generated
    ```
    *NOTE: to prevent a [serious bug](https://github.com/rodekruis/sims_maps_qgis_plugin/issues/39) the symbolic link should have the same as plugin directory e.g: sims_maps_generated*

* Start or restart QGIS3. Reload the plugin with the experimental "Plugin Reloader" plugin.


## License

Licensed under the terms of GNU GPL 2

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
