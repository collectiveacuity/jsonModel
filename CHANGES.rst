ChangeLog
=========

2.4 (2016.09.29)
----------------
* **FEATURE ADDED** object_title added to validate method argument for error handling
* Bug fix for non-json valid object added to model and validate input data
* Bug fix for dictionaries with non-string values for key names
* Bug fix for ingestion of items outside scope of json datatypes

2.2 (2016.07.10)
----------------
* Bug fix for ingestion of dictionaries inside lists
* Updates to unittests

2.1 (2016.07.09)
----------------
* Bug fix for ingestion of keywords with non-matching datatypes
* Updates to unittests

2.0 (2016.06.30)
----------------
* **UPGRADE** Query method added to class to validate criteria and evaluate records
* **UPGRADE** Overhaul of internal class organization to ensure json valid reporting
* **FEATURE ADDED** 'min_value' and 'max_value' extended to string fields
* **FEATURE ADDED** 'excluded_values' added to component conditionals
* **FEATURE ADDED** 'greater_than' and 'less_than' added to component conditionals
* **DEPRECATED** 'integer_only' conditional has been replaced by 'integer_data'
* Fixed bug with init check of schema key names for item designator patterns
* Added missing validation for correct 'contains_either' syntax in model init
* Updates to documentation and unittests

1.6 (2016.05.17)
----------------
* **FEATURE ADDED** 'field_title' added to component criteria
* Updates to documentation and unittests

1.5 (2016.03.26)
----------------
* **FEATURE ADDED** 'metadata' and 'description' added to top-level model declaration
* Metadata dictionary allows developer to inject arbitrary object metadata into model
* Description string allows developer to add a description to the model itself
* Additional documentation and unittest improvements

1.4 (2016.03.23)
----------------
* **FEATURE ADDED** 'field_metadata' added to list of field conditional options
* Dictionary for metadata about a field which is ignored during validation checks
* Additional documentation and unittest improvements

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
* Toggle to add all the criteria defaults for a key type in the keyMap
* Sort dictionary keys alphabetically prior to evaluation
* Allow validation of null datatype declarations
* Allow declaration of multiple datatypes for key values
* Validate size of data object inputs
* Allow declaration of a lambda function for further validation
* Allow validation of path to file or folder