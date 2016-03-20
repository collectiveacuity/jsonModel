ChangeLog
=========

1.3 (2016.03.20)
----------------
* **FEATURE ADDED** jsonModel.ingest(**kwargs)
* Method to construct a model valid output from arbitrary keyword args
* Keywords which do not validate against top-level keys in schema are ignored
* Ignored keywords receive default values (if declared) or empty values from model
* **DEPRECATED** jsonModel.component has been removed
* Validate individual components using jsonModel.validate(input_data, path_to_root='')
* input_dict arg has been changed to input_data in validate positional arguments
* Additional documentation and unittest improvements

1.2 (2016.03.18)
----------------
* **FEATURE ADDED** jsonModel.component(input, path_to_root)
* Method to validate input against a specific component in keyMap
* Helper method to reconstruct a schema endpoint from the path to root
* Additional documentation and unittest improvements
* Home brew path conjunction in jsonLoader replaced by path.join

1.1 (2016.03.06)
----------------
* Bug fix for index out of range error created from empty list input
* Tweaks to documentation

1.0 (2016.01.27)
----------------
* Upload of package

TODO
----
* Allow validation of null datatype declarations
* Allow declaration of multiple datatypes for key values in maps
* Validate size of data object inputs
* Allow declaration of a lambda function for further validation
* Allow validation of path to file or folder