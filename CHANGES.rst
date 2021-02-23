ChangeLog
=========

TODO
----
* Add "contains_all" to criteria for lists to cover multiple items
* Add "=", ">", "<", "<=", ">=" as criteria shortcuts
* Add "in" as criteria shortcut for "discrete_values"
* Change min_size/max_size in map fields to measure key size
* Change custom error argument to accept .format syntax
* Add support for mongo/mango query operator syntax;
* Consider adding validation for HTTP methods of a RESTful API
* Sort dictionary keys alphabetically prior to evaluation (currents inherits json file order)
* Allow declaration of multiple datatypes for key values
* Allow declaration of a lambda function for further validation
* Allow validation of path to file or folder

3.3 (2021.02.23)
----------------
* **FEATURE ADDED** validation of any valid datatype for null declarations
* **FEATURE ADDED** ingestion of any valid datatype for null declarations

3.2 (2020.05.13)
----------------
* Bug fix to remove unused optional argument in explain method
  
3.1 (2020.05.11)
----------------
* **FEATURE ADDED** custom error messages added for regex pattern criteria
* **FEATURE ADDED** explain method added to InputValidationError
* **DEPRECATED** full path of keys added to extra fields error report
* dataModel property added as deepcopy of data_model argument

3.0 (2018.03.28)
-----------------
* **UPGRADE** extensions package with add-on methods for json model objects
* **FEATURE ADDED** tabulate method to extensions to create a table from json model criteria 
* **FEATURE ADDED** min_size & max_size conditionals added to map fields
* **DEPRECATED** max_size field in top-level json model schema declaration
* Bug fix for reporting correct javascript dot_path syntax on query errors

2.9 (2018.03.21)
----------------
* **FEATURE ADDED** 'default_value' conditional added to list fields
* **FEATURE ADDED** integer fields in schema are automatically declared as integer_data
* Updated required field default to False for list fields with empty items
* Updated component and query validation to parse javascript dot_path syntax
* Updated query criteria to map number, string and boolean declarations to equal_to qualifier

2.8 (2017.12.12)
----------------
* **FEATURE ADDED** 'equal_to' conditional to validation and query criteria
* Changed query logic for list items to match any rather than all records
* Bug fix for finding values in walk of nested keys
* Bug fix for post-hoc redefinitions of schema dict causing key errors

2.7 (2016.12.12)
----------------
* Fixed bug in error checking model validation of null fields with component criteria
* Added pass to type checking of input value declarations for null fields

2.6 (2016.12.08)
----------------
* **FEATURE ADDED** field_position added to component criteria for ordered position handling
* Bug fix for non-integer values of max size, min size, max length and min length criteria

2.5 (2016.10.25)
----------------
* Fixed missing declared value criteria for empty strings, number and boolean declarations
* Updates to MANIFEST and setup process to exclude IDE file types
* Updates to unittests

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

