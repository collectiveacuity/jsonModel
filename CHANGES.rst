ChangeLog
=========

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
* Update loader to use join instead of home brew path method
* Allow declaration of multiple datatypes for key values in maps
* Validate size of data object inputs
* Allow declaration of a lambda function for further validation
* Allow validation of path to file or folder