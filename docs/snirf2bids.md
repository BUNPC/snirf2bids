<!-- markdownlint-disable -->

<a href="..\snirf2bids\snirf2bids.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `snirf2bids`
Module for converting snirf file into bids format 

Maintained by the Boston University Neurophotonics Center 


---

<a href="..\snirf2bids\snirf2bids.py#L1088"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `snirf_to_bids`

```python
snirf_to_bids(inputpath: str, outputpath: str, participants: dict = None)
```

Creates a BIDS-compliant folder structure (right now, just the metadata files) from a SNIRF file 



**Args:**
 
 - <b>`inputpath`</b>:  The file path to the reference SNIRF file 
 - <b>`outputpath`</b>:  The file path/directory for the created BIDS metadata files 
 - <b>`participants`</b>:  A dictionary with participant information  Example = 
 - <b>`{participant_id`</b>:  'sub-01', 
 - <b>`age`</b>:  34, 
 - <b>`sex`</b>:  'M'} 
 - <b>`scans`</b>:  A dictionary with SNIRF/run information and its acquisition time 


---

<a href="..\snirf2bids\snirf2bids.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Field`
Class which encapsulates fields inside a Metadata class 



**Attributes:**
 
 - <b>`_value`</b>:  The value of the field 

<a href="..\snirf2bids\snirf2bids.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(val)
```

Generic constructor for a Field class 

It stores a specific value declared in the class initialization in _value 


---

#### <kbd>property</kbd> value

Value Getter for Field class 




---

<a href="..\snirf2bids\snirf2bids.py#L270"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `String`
Subclass which encapsulates fields with string values inside a Metadata class 



**Attributes:**
 
 - <b>`_value`</b>:  The value of the field 
 - <b>`type`</b>:  Data type of the field - in this case, it's "str" 

<a href="..\snirf2bids\snirf2bids.py#L278"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(val)
```

Generic constructor for a String Field class inherited from the Field class 

Additionally, it stores the datatype which in this case, it is string 


---

#### <kbd>property</kbd> value

Value Getter for Field class 



---

<a href="..\snirf2bids\snirf2bids.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_type`

```python
get_type()
```

Datatype getter for the String class 

---

<a href="..\snirf2bids\snirf2bids.py#L286"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `validate`

```python
validate(val)
```

Datatype Validation function for String class 


---

<a href="..\snirf2bids\snirf2bids.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Number`
Subclass which encapsulates fields with numerical values inside a Metadata class 



**Attributes:**
 
 - <b>`_value`</b>:  The value of the field 
 - <b>`type`</b>:  Data type of the field - in this case, it's "int" 

<a href="..\snirf2bids\snirf2bids.py#L305"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(val)
```

Generic constructor for a Number Field class inherited from the Field class 

Additionally, it stores the datatype which in this case, it is integer 


---

#### <kbd>property</kbd> value

Value Getter for Field class 



---

<a href="..\snirf2bids\snirf2bids.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_type`

```python
get_type()
```

Datatype getter for the Number class 

---

<a href="..\snirf2bids\snirf2bids.py#L313"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `validate`

```python
validate(val)
```

Datatype Validation function for Number class 


---

<a href="..\snirf2bids\snirf2bids.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Metadata`
Metadata File Class 

Class object that encapsulates the JSON and TSV Metadata File Class 



**Attributes:**
 
 - <b>`_fields`</b>:  A dictionary of the fields and the values contained in it for a specific Metadata class 
 - <b>`_source_snirf`</b>:  The filepath to the reference SNIRF file to create the specific Metadata class 

<a href="..\snirf2bids\snirf2bids.py#L334"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Generic constructor for a Metadata class 

Most importantly, it constructs the default fields with empty values within _fields in a dictionary format 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 


---

<a href="..\snirf2bids\snirf2bids.py#L488"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JSON`
JSON Class 

Class object that encapsulates subclasses that create and contain BIDS JSON files 

<a href="..\snirf2bids\snirf2bids.py#L495"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Generic constructor for JSON class - uses the one inherited from the Metadata class 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_json`

```python
load_from_json(fpath)
```

Create the JSON metadata class from a JSON file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference JSON file 



**Raises:**
 
 - <b>`TypeError`</b>:  Incorrect data type for a specific field based on data loaded from the JSON file 

---

<a href="..\snirf2bids\snirf2bids.py#L522"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_json`

```python
save_to_json(info, fpath)
```

Save a JSON inherited class into an output JSON file with a BIDS-compliant name in the file directory  designated by the user 



**Args:**
 
 - <b>`info`</b>:  Subject info field from the Subject class 
 - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata JSON file with a BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L546"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TSV`
TSV Class 

Class object that encapsulates subclasses that create and contain BIDS TSV files 



**Attributes:**
 
 - <b>`_sidecar`</b>:  Contains the field names and descriptions for each field for the Sidecar JSON file 

<a href="..\snirf2bids\snirf2bids.py#L555"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```

Generic Constructor for TSV class - uses the one inherited from the Metadata class 

Additionally, added the sidecar property for the Sidecar JSON files 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `export_sidecar`

```python
export_sidecar(info, fpath)
```

Exports sidecar as a json file 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L599"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_tsv`

```python
load_from_tsv(fpath)
```

Create the TSV metadata class from a TSV file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference TSV file 

---

<a href="..\snirf2bids\snirf2bids.py#L624"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `make_sidecar`

```python
make_sidecar()
```

Makes a dictionary with the default description noted in BIDS specification into the Sidecar dictionary 



**Returns:**
  Dictionary with correct fields(that have values) with description of each field within TSV file filled out 

---

<a href="..\snirf2bids\snirf2bids.py#L563"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_tsv`

```python
save_to_tsv(info, fpath)
```

Save a TSV inherited class into an output TSV file with a BIDS-compliant name in the file directory designated by the user 



**Args:**
 
     - <b>`info`</b>:  Subject info field from the Subject class 
     - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata TSV file with BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L647"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Coordsystem`
Coordinate System Metadata Class 

Class object that mimics and contains the data for the coordsystem.JSON metadata file 

<a href="..\snirf2bids\snirf2bids.py#L653"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(fpath=None)
```

Inherited constructor for the Coordsystem class 



**Args:**
 
 - <b>`fpath`</b>:  The file path to a reference SNIRF file 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L666"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_SNIRF`

```python
load_from_SNIRF(fpath)
```

Creates the Coordsystem class based on information from a reference SNIRF file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 

---

<a href="..\snirf2bids\snirf2bids.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_json`

```python
load_from_json(fpath)
```

Create the JSON metadata class from a JSON file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference JSON file 



**Raises:**
 
 - <b>`TypeError`</b>:  Incorrect data type for a specific field based on data loaded from the JSON file 

---

<a href="..\snirf2bids\snirf2bids.py#L522"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_json`

```python
save_to_json(info, fpath)
```

Save a JSON inherited class into an output JSON file with a BIDS-compliant name in the file directory  designated by the user 



**Args:**
 
 - <b>`info`</b>:  Subject info field from the Subject class 
 - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata JSON file with a BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L678"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Optodes`
Optodes Metadata Class 

Class object that mimics and contains the data for the optodes.tsv metadata file 

<a href="..\snirf2bids\snirf2bids.py#L684"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(fpath=None)
```

Inherited constructor for the Optodes class 



**Args:**
 
 - <b>`fpath`</b>:  The file path to a reference SNIRF file 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `export_sidecar`

```python
export_sidecar(info, fpath)
```

Exports sidecar as a json file 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L697"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_SNIRF`

```python
load_from_SNIRF(fpath)
```

Creates the Optodes class based on information from a reference SNIRF file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 

---

<a href="..\snirf2bids\snirf2bids.py#L599"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_tsv`

```python
load_from_tsv(fpath)
```

Create the TSV metadata class from a TSV file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference TSV file 

---

<a href="..\snirf2bids\snirf2bids.py#L624"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `make_sidecar`

```python
make_sidecar()
```

Makes a dictionary with the default description noted in BIDS specification into the Sidecar dictionary 



**Returns:**
  Dictionary with correct fields(that have values) with description of each field within TSV file filled out 

---

<a href="..\snirf2bids\snirf2bids.py#L563"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_tsv`

```python
save_to_tsv(info, fpath)
```

Save a TSV inherited class into an output TSV file with a BIDS-compliant name in the file directory designated by the user 



**Args:**
 
     - <b>`info`</b>:  Subject info field from the Subject class 
     - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata TSV file with BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L727"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Channels`
Channels Metadata Class 

Class object that mimics and contains the data for the channels.tsv metadata file 

<a href="..\snirf2bids\snirf2bids.py#L733"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(fpath=None)
```

Inherited constructor for the Channels class 



**Args:**
 
 - <b>`fpath`</b>:  The file path to a reference SNIRF file 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `export_sidecar`

```python
export_sidecar(info, fpath)
```

Exports sidecar as a json file 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L746"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_SNIRF`

```python
load_from_SNIRF(fpath)
```

Creates the Channels class based on information from a reference SNIRF file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 

---

<a href="..\snirf2bids\snirf2bids.py#L599"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_tsv`

```python
load_from_tsv(fpath)
```

Create the TSV metadata class from a TSV file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference TSV file 

---

<a href="..\snirf2bids\snirf2bids.py#L624"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `make_sidecar`

```python
make_sidecar()
```

Makes a dictionary with the default description noted in BIDS specification into the Sidecar dictionary 



**Returns:**
  Dictionary with correct fields(that have values) with description of each field within TSV file filled out 

---

<a href="..\snirf2bids\snirf2bids.py#L563"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_tsv`

```python
save_to_tsv(info, fpath)
```

Save a TSV inherited class into an output TSV file with a BIDS-compliant name in the file directory designated by the user 



**Args:**
 
     - <b>`info`</b>:  Subject info field from the Subject class 
     - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata TSV file with BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L817"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Events`
Channels Metadata Class 

Class object that mimics and contains the data for the events.tsv metadata file 

<a href="..\snirf2bids\snirf2bids.py#L823"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(fpath=None)
```

Inherited constructor for the Events class 



**Args:**
 
 - <b>`fpath`</b>:  The file path to a reference SNIRF file 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L638"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `export_sidecar`

```python
export_sidecar(info, fpath)
```

Exports sidecar as a json file 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L836"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_SNIRF`

```python
load_from_SNIRF(fpath)
```

Creates the Events class based on information from a reference SNIRF file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 

---

<a href="..\snirf2bids\snirf2bids.py#L599"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_tsv`

```python
load_from_tsv(fpath)
```

Create the TSV metadata class from a TSV file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference TSV file 

---

<a href="..\snirf2bids\snirf2bids.py#L624"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `make_sidecar`

```python
make_sidecar()
```

Makes a dictionary with the default description noted in BIDS specification into the Sidecar dictionary 



**Returns:**
  Dictionary with correct fields(that have values) with description of each field within TSV file filled out 

---

<a href="..\snirf2bids\snirf2bids.py#L563"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_tsv`

```python
save_to_tsv(info, fpath)
```

Save a TSV inherited class into an output TSV file with a BIDS-compliant name in the file directory designated by the user 



**Args:**
 
     - <b>`info`</b>:  Subject info field from the Subject class 
     - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata TSV file with BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L865"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Sidecar`
NIRS Sidecar(_nirs.JSON) Metadata Class 

Class object that mimics and contains the data for the _nirs.JSON metadata file 

<a href="..\snirf2bids\snirf2bids.py#L871"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(fpath=None)
```

Inherited constructor for the Sidecar class 



**Args:**
 
 - <b>`fpath`</b>:  The file path to a reference SNIRF file 




---

<a href="..\snirf2bids\snirf2bids.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `change_type`

```python
change_type(name)
```

Change the data type restriction for a field (from a String class to a Number class or vice versa) 



**Args:**
 
 - <b>`name`</b>:  The field name 



**Raises:**
 
 - <b>`TypeError`</b>:  If it's an invalid/undeclared field 

---

<a href="..\snirf2bids\snirf2bids.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `default_fields`

```python
default_fields()
```

Obtain the default fields and their data type for a specific metadata file/class 



**Returns:**
  The list of default fields for a specific metadata class and the data type 
 - <b>`default_list`</b>:  List of default field names for a specific metadata class 
 - <b>`default_type`</b>:  List of default field data types for a specific metadata class 

---

<a href="..\snirf2bids\snirf2bids.py#L454"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_class_name`

```python
get_class_name()
```

Obtains the name of the specific metadata class 



**Returns:**
  The name of the (specific metadata) class 

---

<a href="..\snirf2bids\snirf2bids.py#L463"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column`

```python
get_column(name)
```

Obtains the value of a specified field/'column' of a Metadata class 



**Args:**
 
 - <b>`name`</b>:  Name of the field/'column' 



**Returns:**
 The value of a specified field/'column' - similar to __getattr__ 

---

<a href="..\snirf2bids\snirf2bids.py#L474"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_column_names`

```python
get_column_names()
```

Get the names of the field in a specific metadata class/file that has a value(s) 



**Returns:**
 A list of field names that have a value in a specific metadata file 

---

<a href="..\snirf2bids\snirf2bids.py#L883"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_SNIRF`

```python
load_from_SNIRF(fpath)
```

Creates the Sidecar class based on information from a reference SNIRF file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 

---

<a href="..\snirf2bids\snirf2bids.py#L499"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_json`

```python
load_from_json(fpath)
```

Create the JSON metadata class from a JSON file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference JSON file 



**Raises:**
 
 - <b>`TypeError`</b>:  Incorrect data type for a specific field based on data loaded from the JSON file 

---

<a href="..\snirf2bids\snirf2bids.py#L522"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `save_to_json`

```python
save_to_json(info, fpath)
```

Save a JSON inherited class into an output JSON file with a BIDS-compliant name in the file directory  designated by the user 



**Args:**
 
 - <b>`info`</b>:  Subject info field from the Subject class 
 - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata file in 



**Returns:**
 Outputs a metadata JSON file with a BIDS-compliant name in the specified file path 


---

<a href="..\snirf2bids\snirf2bids.py#L906"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Subject`
'Subject' Class 

Class object that encapsulates a single 'run' (for now) with fields containing the metadata and 'subject'/run information 



**Attributes:**
 
 - <b>`coordsystem`</b>:  Contains a Coordsystem class object for a specific 'subject'/run 
 - <b>`optodes`</b>:  Contains an Optodes class object for a specific 'subject'/run 
 - <b>`channel`</b>:  Contains a Channels class object for a specific 'subject'/run 
 - <b>`sidecar`</b>:  Contains a Sidecar (_nirs.JSON) class object for a specific 'subject'/run 
 - <b>`events`</b>:  Contains an Events class object for a specific 'subject'/run 
 - <b>`subinfo`</b>:  Contains the 'subject'/run information related to the data stored in a 'Subject' object 
 - <b>`participants`</b>:  Contains the metadata related to the participants.tsv file 

<a href="..\snirf2bids\snirf2bids.py#L923"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(fpath=None)
```

Constructor for the 'Subject' class 




---

<a href="..\snirf2bids\snirf2bids.py#L1050"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `export`

```python
export(outputFormat: str = 'Folder', fpath: str = None)
```

Exports/creates the BIDS-compliant metadata files based on information stored in the 'subject' class object 



**Args:**
 
 - <b>`outputFormat`</b>:  The target destination and indirectly, the output format of the metadata file  The default value is 'Folder', which outputs the metadata file to a specific file directory  specified by the user  The other option is 'Text', which outputs the files and data as a string (JSON-like format) 
 - <b>`fpath`</b>:  The file path that points to the folder where we intend to save the metadata files in 



**Returns:**
 A string containing the metadata file names and its content if the user chose the 'Text' output format or a set of metadata files in a specified folder if the user chose the default or 'Folder' output format 

---

<a href="..\snirf2bids\snirf2bids.py#L1038"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ses`

```python
get_ses()
```

Obtains the session ID/number for a particular 'subject'/run 



**Returns:**
  The session ID/number (returns an empty string if there is no information) 

---

<a href="..\snirf2bids\snirf2bids.py#L1026"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_subj`

```python
get_subj()
```

Obtains the subject ID/number for a particular 'subject'/run 



**Returns:**
  The subject ID/number (returns an empty string if there is no information) 

---

<a href="..\snirf2bids\snirf2bids.py#L1014"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `load_from_snirf`

```python
load_from_snirf(fpath)
```

Loads the metadata from a reference SNIRF file 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 

---

<a href="..\snirf2bids\snirf2bids.py#L969"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pull_fnames`

```python
pull_fnames()
```

Check directory for files (not folders) 



**Returns:**
  A dictionary of file names for specific metadata files based on the existence of a session label  (different nomenclature) that are split into subject-level and session-level metadata files 


 - <b>`subj_fnames`</b>:  Contains a dictionary of metadata filenames that are on the subject level 
 - <b>`ses_fnames`</b>:  Contains a dictionary of metadata filenames that are on the session level 



**Notes:**

> Have to figure out how to do this based on the database structure In the case of the test snirf file, there is no presence of: 1. session number 2. run number 

---

<a href="..\snirf2bids\snirf2bids.py#L954"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `pull_task`

```python
pull_task(fpath=None)
```

Pull the Task label from either the SNIRF file name or from the Sidecar class (if available) 



**Args:**
 
 - <b>`fpath`</b>:  The file path to the reference SNIRF file 



**Returns:**
 The task label/name 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
