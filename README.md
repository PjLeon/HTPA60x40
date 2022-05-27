
A plugin for DSF, that communicates with the HTPA, processes its output and implements a rudimentary control loop to counteract object overheating

# OLD README: 
## core.py
Main script

### Data types supported
* Call `SUPPORTED_EXTENSIONS` to see the list of currently supported types.
  * txt ⟵ currently the only extension that can copy file headers (the first line in Heimanns HTPA recordings)
  * csv
  * pickle (.pickle, .pkl, .p)

### Reading and writing files
* `read_tpa_file` reads files with supported extensions (deduced from filename extension given as argument)
* `write_tpa_file`  writes files with supported extensions (deduced from filename extension given as argument)

