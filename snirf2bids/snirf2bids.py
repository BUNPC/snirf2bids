""" Module for converting snirf file into bids format

Maintained by the Boston University Neurophotonics Center
"""
import io
import csv
import json
import os
from warnings import warn

import numpy as np
import importlib_resources
from pysnirf2 import Snirf, SnirfFormatError

try:
    from snirf2bids.__version__ import __version__ as __version__
except Exception:
    warn('Failed to load snirf2bids library version')
    __version__ = '0.0.0'

try:
    with open(importlib_resources.files("schema") / 'schema.json') as f:
        __SCHEMA__ = json.load(f)
    with open(importlib_resources.files("schema") / 'channel_types.json') as f:
        __CHANNEL_TYPES__= json.load(f)
    with open(importlib_resources.files("schema") / 'time_units.json') as f:
        __TIME_UNITS__= json.load(f)
except Exception as e:
    print(e)
    raise ImportError('Could not import snirf2bids. Failed to load BIDS schema from ' + str(importlib_resources.files("schema") / 'schema.json'))


def _get_time_unit(key: str):
    try:
        return float(__TIME_UNITS__[str(key)])
    except KeyError:
        warn('TimeUnit {} not understood. Falling back to interpretation as seconds.')
        return 1.0


def _get_channel_type(key: str):
    try:
        return str(__CHANNEL_TYPES__[str(key)])
    except KeyError:
        return "MISC"


def _get_requirement_levels(key: str):
    return {key: value["__RequirementLevel__"] for (key, value) in __SCHEMA__[key].items() if type(value) is dict and "__RequirementLevel__" in value}


def _get_datatypes(key: str):
    return {key: value["__Type__"] for (key, value) in __SCHEMA__[key].items() if type(value) is dict and "__Type__" in value}


def _get_descriptions(key: str):
    return {key: value["__Description__"] for (key, value) in __SCHEMA__[key].items() if type(value) is dict and "__Description__" in value}


def _extract_entities_from_filename(fname: str):
    """
    Args:
        fname (str): BIDS-compliant filename
    Returns
        (dict): dictionary of entities and their values
    """
    ev_pairs = [ev for ev in os.path.split(fname)[-1].split('.')[0].split('_') if '-' in ev]
    return {ev.split('-')[0]: ev.split('-')[1] for ev in ev_pairs}
    

def _pull_entity_value(fname: str, entity_name: str):
    return _extract_entities_from_filename(fname)[entity_name]


def _makefiledir(info, classname, fpath, sidecar=None):
    """Create the file directory for specific Metadata files

        Args:
            info: Subject info field from the Subject class
            classname: The specific metadata class name (coordsystem, optodes, etc.)
            fpath: The file path that points to the folder where we intend to save the metadata file in

        Returns:
            The full directory path for the specific metadata file (in string)

        Raises:
            ValueError: If there are no subject information
    """

    if info is not None:
        filename = _make_filename_prefix(info)
        filedir = fpath + '/' + filename
    else:
        raise ValueError("No subject info for BIDS file naming reference")

    return filedir


def _make_filename_prefix(entities_dict: dict):
    """Compose a file prefix from a dict of entities

        Args:
            entities (dict): The name entities i.e. `sub-`, `ses-`, `task-`
        Returns:
            (str) An ordered file prefix
    """
    entities = list(entities_dict.keys())
    name = 'sub-' + entities_dict['sub']
    if 'ses' in entities:
        name += '_ses-' + entities_dict['ses']
    if 'task' in entities:
        name += '_task-' + entities_dict['task']
    # Misc entities
    for entity in [entity for entity in entities if entity not in ['sub', 'ses', 'task', 'run']]:
        name += '_' + entity + entities_dict[entity]
    if 'run' in entities:
        name += '_run-' + entities_dict['run']
    return name


def _pull_participant(field, fpath=None):
    """Obtains the value for specific fields in the participants.tsv file (minimum functionality)

        Only works for a single SNIRF file for now with a predefined set of fields

        Args:
            field: The specific field/column name in the participants.tsv file
            fpath: The file path that points to the folder where we intend to save the metadata file in

        Returns:
            The value for the specific field/column specified in string
    """

    if fpath is not None:
        with Snirf(fpath, 'r') as s:
            if s.nirs[0].metaDataTags.__contains__(field):
                # make sure the field exists, and then pull
                value = s.nirs[0].metaDataTags.__getattribute__(field)
            else:
                value = None
    else:
        value = None
    if field == 'sex' and value == '1':
        value = 'M'
    elif field == 'sex' and value == '2':
        value = 'F'
    elif field == 'species' and value is None:
        value = 'homo sapiens'

    return value


def _pull_scans(entities, field, fpath=None):
    """Creates the scans.tsv file

        Only works for a single SNIRF file for now with a predefined set of fields

        Args:
            entities: subject information field (SnirfRun.entities)
            field: field within scans.tsv file (filename or acq_time)
            fpath: file path of snirf file to extract scans.tsv from. OPTIONAL

        Returns:
            the string of the requested field parameter extracted from the snirf in fpath
    """
    if fpath is None:
        return None
    else:
        if field == 'filename':
            return 'nirs/' + _make_filename_prefix(entities) + '.snirf'
        elif field == 'acq_time':
            with Snirf(fpath, 'r') as s:
                date = s.nirs[0].metaDataTags.MeasurementDate
                time = s.nirs[0].metaDataTags.MeasurementTime
                hour_minute_second = time[:8]
                decimal = ''
                zone = ''
                if '.' in time:
                    for x in time[8:]:
                        if x.isdigit() or x == '.':
                            pass
                        else:
                            position = time.find(x)
                            zone = '[' + time[position::] + ']'
                            decimal = '[' + time[8:position] + ']'
                            break
                else:
                    for x in time[8:]:
                        if x.isdigit():
                            pass
                        else:
                            position = time.find(x)
                            zone = '[' + time[position::] + ']'
                            decimal = ''
                            break

            return date + 'T' + hour_minute_second + decimal + zone


def _tsv_to_json(tsv_dict):
    fields = list(tsv_dict.keys())
    values = list(tsv_dict.values())
    field_temp = ''
    value_temp = ''

    for i in range(len(fields) - 1):
        field_name = fields[i] + '\t'
        if values[i] is None:
            value_name = '\t'
        else:
            value_name = values[i] + '\t'
        field_temp = field_temp + field_name
        value_temp = value_temp + value_name

    field_temp = field_temp + fields[len(fields) - 1] + '\n'
    if values[len(values) - 1] is None:
        value_temp = value_temp + '\n'
    else:
        value_temp = value_temp + values[len(values) - 1] + '\n'

    return field_temp + value_temp


def _get_detector_labels(s: Snirf):
    """
    Gets the detector labels from a SNIRF file or generate them if they do not exist
    """
    if s.nirs[0].probe.detectorLabels is not None:
        return s.nirs[0].probe.detectorLabels
    if s.nirs[0].probe.detectorPos2D is not None:
        n_det = np.shape(s.nirs[0].probe.detectorPos2D)[0]
    elif s.nirs[0].probe.detectorPos2D is not None:
        n_det = np.shape(s.nirs[0].probe.detectorPos3D)[0]
    else:
        return np.array([])
    return np.array(['D' + str(i + 1) for i in range(n_det)], dtype='O')
    

def _get_source_labels(s: Snirf):
    """
    Gets the source labels from a SNIRF file or generate them if they do not exist
    """
    if s.nirs[0].probe.sourceLabels is not None:
        return s.nirs[0].probe.sourceLabels
    if s.nirs[0].probe.sourcePos2D is not None:
        n_src = np.shape(s.nirs[0].probe.sourcePos2D)[0]
    elif s.nirs[0].probe.sourcePos2D is not None:
        n_src = np.shape(s.nirs[0].probe.sourcePos3D)[0]
    else:
        return np.array([])
    return np.array(['S' + str(i + 1) for i in range(n_src)], dtype='O')


class Field:
    """Class which encapsulates fields inside a Metadata class

        Attributes:
            _value: The value of the field
    """

    def __init__(self, val):
        """Generic constructor for a Field class

        It stores a specific value declared in the class initialization in _value
        """
        self._value = val

    @property
    def value(self):
        """Value Getter for Field class"""
        return self._value

    @value.setter
    def value(self, val):
        """Value Setter for Field class"""
        self._value = val


class String(Field):
    """Subclass which encapsulates fields with string values inside a Metadata class

        Attributes:
            _value: The value of the field
            type: Data type of the field - in this case, it's "str"
    """

    def __init__(self, val):
        """Generic constructor for a String Field class inherited from the Field class

            Additionally, it stores the datatype which in this case, it is string
        """
        super().__init__(val)
        self.type = str

    @staticmethod
    def validate(val):
        """Datatype Validation function for String class"""
        if type(val) is str or val is None:
            return True

    def get_type(self):
        """Datatype getter for the String class"""
        return self.type


class Number(Field):
    """Subclass which encapsulates fields with numerical values inside a Metadata class

        Attributes:
            _value: The value of the field
            type: Data type of the field - in this case, it's "int"
    """

    def __init__(self, val):
        """Generic constructor for a Number Field class inherited from the Field class

            Additionally, it stores the datatype which in this case, it is integer
        """
        super().__init__(val)
        self.type = int

    @staticmethod
    def validate(val):
        """Datatype Validation function for Number class"""
        if type(val) is not str or val is None:
            return True

    def get_type(self):
        """Datatype getter for the Number class"""
        return self.type


class NumberArray(Field):
    """Subclass which encapsulates fields with multiple numerical values inside a Metadata class

        Attributes:
            _value: The value of the field
            type: Data type of the field - in this case, it's "int"
    """

    def __init__(self, val):
        super().__init__(np.array(val).astype(float))
        self.type = int

    @staticmethod
    def validate(val):
        """Datatype Validation function for Number class"""
        if type(val) is not str or val is None:
            return True

    def get_type(self):
        """Datatype getter for the Number class"""
        return self.type


class StringArray(Field):

    def __init__(self, val):
        """Generic constructor for a Number Field class inherited from the Field class

            Additionally, it stores the datatype which in this case, it is integer
        """
        super().__init__(np.array(val).astype(object))
        self.type = str

    @staticmethod
    def validate(val):
        """Datatype Validation function for Number class"""
        try:
            for item in val:
                if not type(item) is str:
                    return False
        except TypeError:
            return False

    def get_type(self):
        return self.type


class Metadata:
    """ Metadata File Class

    Class object that encapsulates the JSON and TSV Metadata File Class

    Attributes:
        _fields: A dictionary of the fields and the values contained in it for a specific Metadata class
        _source_snirf: The filepath to the reference SNIRF file to create the specific Metadata class
    """

    def __init__(self):
        """Generic constructor for a Metadata class

        Most importantly, it constructs the default fields with empty values within _fields in a dictionary format
        """
        default_list, default_type = self.default_fields()
        # default = {'path2origin': String(None)}
        default = {}
        for name in default_list:
            # assume they are all string now
            if default_type[name] == 'String':
                default[name] = String(None)
            elif default_type[name] == 'Number':
                default[name] = Number(None)

        self._fields = default
        self._source_snirf = None

    def __setattr__(self, name, val):
        """Overwrites the attribute setter default function

            Args:
                name: Name of the field
                val: The new value to be set for the specified field

            Raises:
                ValueError: If the data type is incorrect or the input is invalid
        """
        if name.startswith('_'):
            super().__setattr__(name, val)

        elif name in self._fields.keys():
            if self._fields[name].validate(val):
                self._fields[name].value = val
            else:
                raise ValueError("Incorrect data type")

        elif name not in self._fields.keys():
            if name == 'sidecar':
                self._sidecar = None
            elif String.validate(val):  # Use our static method to validate a guy of this type before creating it
                self._fields[name] = String(val)
            elif Number.validate(val):
                self._fields[name] = Number(val)
            else:
                raise ValueError('invalid input')

    def __getattr__(self, name):
        """Overwrites the attribute getter default function

            Args:
                name: The field name

            Returns:
                The value contained in the specified field
        """

        if name in self._fields.keys():
            return self._fields[name].value  # Use the property of the Guy in our managed collection
        else:
            return super().__getattribute__(name)

    def __delattr__(self, name):
        """Overwrites the attribute deleter default function

            Args:
                name: The field name

            Raises:
                TypeError: If the field is considered a default field
        """

        default_list, default_type = self.default_fields()
        if name not in default_list.keys():
            del self._fields[name]
        else:
            raise TypeError("Cannot remove a default field!")

    def change_type(self, name):
        """Change the data type restriction for a field (from a String class to a Number class or vice versa)

            Args:
                name: The field name

            Raises:
                TypeError: If it's an invalid/undeclared field
        """

        if self._fields[name].get_type() is str:
            self._fields[name] = Number(None)

        elif self._fields[name].get_type() is int:
            self._fields[name] = String(None)

        else:
            raise TypeError("Invalid field!")

    def default_fields(self):
        """Obtain the default fields and their data type for a specific metadata file/class

            Returns:
                The list of default fields for a specific metadata class and the data type
                default_list: List of default field names for a specific metadata class
                default_type: List of default field data types for a specific metadata class
        """

        default_list = None
        default_type = None
        if isinstance(self, Sidecar):
            default_list = _get_requirement_levels("*_nirs.json")
            default_type = _get_datatypes("*_nirs.json")
        elif isinstance(self, JSON):
            default_list = _get_requirement_levels("*_" + self.get_class_name().lower() + ".json")
            default_type = _get_datatypes("*_" + self.get_class_name().lower() + ".json")
        elif isinstance(self, TSV):
            default_list = _get_requirement_levels("*_" + self.get_class_name().lower() + ".tsv")
            default_type = _get_datatypes("*_" + self.get_class_name().lower() + ".tsv")
        return default_list, default_type

    def get_class_name(self):
        """Obtains the name of the specific metadata class

            Returns:
                The name of the (specific metadata) class
        """

        return self.__class__.__name__

    def get_column(self, name):
        """Obtains the value of a specified field/'column' of a Metadata class

            Args:
                name: Name of the field/'column'

            Returns:
                The value of a specified field/'column' - similar to __getattr__
        """
        return self.__getattr__(name)

    def get_column_names(self):
        """Get the names of the field in a specific metadata class/file that has a value(s)

            Returns:
            A list of field names that have a value in a specific metadata file
        """

        fieldnames = []  # filter out the fieldnames with empty fields, and organize into row structure
        for name in self._fields.keys():
            if self._fields[name].value is not None:
                fieldnames = np.append(fieldnames, name)
        return fieldnames


class JSON(Metadata):
    """ JSON Class

    Class object that encapsulates subclasses that create and contain BIDS JSON files

    """

    def __init__(self):
        """Generic constructor for JSON class - uses the one inherited from the Metadata class"""
        super().__init__()

    def load_from_json(self, fpath):
        """Create the JSON metadata class from a JSON file

            Args:
                fpath: The file path to the reference JSON file

            Raises:
                TypeError: Incorrect data type for a specific field based on data loaded from the JSON file
        """
        with open(fpath) as file:
            fields = json.load(file)

        new = {}
        for name in fields:
            # assume they are all string now
            if String.validate(fields[name]):
                new[name] = String(fields[name])
            elif Number.validate(fields[name]):
                new[name] = Number(fields[name])
            else:
                raise TypeError("Incorrect Datatype")

        self._fields = new

    def save_to_json(self, info, fpath):
        """Save a JSON inherited class into an output JSON file with a BIDS-compliant name in the file directory
                designated by the user

        Args:
            info: Subject info field from the Subject class
            fpath: The file path that points to the folder where we intend to save the metadata file in

        Returns:
            Outputs a metadata JSON file with a BIDS-compliant name in the specified file path
        """

        classname = self.get_class_name().lower()
        filedir = _makefiledir(info, classname, fpath)

        fields = {}
        for name in self._fields.keys():
            if self._fields[name].value is not None:
                fields[name] = self._fields[name].value
        with open(filedir, 'w') as file:
            json.dump(fields, file, indent=4)
        # self._fields['path2origin'].value = filedir
            
    def get_all_fields(self):
        temp = {}
        fields = self._fields
        defaults = self.default_fields()[0]
        for one in fields:
            value = getattr(self, one)
            if value is not None:
                temp[one] = value
            elif value is None and defaults[one] == 'REQUIRED':  # this will include all empty required fields
                temp[one] = ''
        return temp


class TSV(Metadata):
    """ TSV Class

        Class object that encapsulates subclasses that create and contain BIDS TSV files

        Attributes:
            _sidecar: Contains the field names and descriptions for each field for the Sidecar JSON file
    """

    def __init__(self):
        """Generic Constructor for TSV class - uses the one inherited from the Metadata class

        Additionally, added the sidecar property for the Sidecar JSON files
        """
        super().__init__()
        self._sidecar = None

    def save_to_tsv(self, info, fpath, header=True):
        """Save a TSV inherited class into an output TSV file with a BIDS-compliant name in the file directory
        designated by the user

            Args:
                info: Subject info field from the Subject class
                fpath: The file path that points to the folder where we intend to save the metadata file in

            Returns:
                Outputs a metadata TSV file with BIDS-compliant name in the specified file path
        """

        classname = self.get_class_name().lower()
        filedir = _makefiledir(info, classname, fpath)

        fieldnames, valfiltered, jsontext = self.get_all_fields()

        # TSV FILE WRITING
        with open(filedir, 'w', newline='') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t', newline='')  # writer setup in tsv format
            if header:
                writer.writerow(fieldnames)  # write fieldnames
            writer.writerows(valfiltered)  # write rows

    def load_from_tsv(self, fpath):
        """Create the TSV metadata class from a TSV file

            Args:
                fpath: The file path to the reference TSV file
        """

        with open(fpath, encoding="utf8", errors='ignore') as file:
            csvreader = csv.reader(file)
            names = next(csvreader)

            temp = ''.join(name for name in names)
            if '\ufeff' in temp:
                temp = temp.split('\ufeff')[1]
            rows = temp.split('\t')

            for onerow in csvreader:
                row = ''.join(row for row in onerow)
                row = row.split('\t')
                rows = np.vstack((rows, row))

        for i in range(len(rows[0])):
            onename = rows[0][i]
            self._fields[onename].value = rows[1:, i]

    def make_sidecar(self):
        """Makes a dictionary with the default description noted in BIDS specification into the Sidecar dictionary

        Returns:
            Dictionary with correct fields(that have values) with description of each field within TSV file filled out
        """
        keylist = list(self.get_column_names())
        d = dict.fromkeys(keylist)
        fields = _get_descriptions('*_' + self.get_class_name().lower() + '.tsv')
        for x in keylist:
            if d[x] is None:
                d[x] = {'Description': fields[x]}
        return d

    def export_sidecar(self, info, fpath):
        """Exports sidecar as a json file"""
        classname = self.get_class_name().lower()
        sidecar = 'sidecar'
        filedir = _makefiledir(info, classname, fpath, sidecar)
        with open(filedir, 'w') as file:
            json.dump(self._sidecar, file, indent=4)

    def get_all_fields(self, header=True):
        fields = list(self._fields)
        values = list(self._fields.values())
        entries_by_col = [values[i].value for i in range(len(values))]
        
        mask = [val is not None for val in entries_by_col]
        columns = [entries_by_col[i] for i in range(len(mask)) if mask[i]] 
        headers = [fields[i] for i in range(len(mask)) if mask[i]] 
        
        assert len(columns) == len(headers), 'failed to parse TSV fields'
        
        if len(headers) > 0:
            formatted = io.StringIO('wb', newline='')
            writer = csv.writer(formatted, delimiter='\t')
            if header:
                writer.writerow(headers)
            for i in range(len(columns[0])):  # For each row
                writer.writerow([str(col[i]) for col in columns])

        return headers, columns, formatted.getvalue()
    
    @property
    def sidecar(self):
        return self._sidecar


class Coordsystem(JSON):
    """Coordinate System Metadata Class

    Class object that mimics and contains the data for the coordsystem.JSON metadata file
    """

    def __init__(self, fpath=None):
        """Inherited constructor for the Coordsystem class

        Args:
            fpath: The file path to a reference SNIRF file
        """

        if fpath is not None:
            Metadata.__init__(self)
            self.load_from_SNIRF(fpath)
        else:
            Metadata.__init__(self)

    def load_from_SNIRF(self, fpath):
        """Creates the Coordsystem class based on information from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
        """

        self._source_snirf = fpath
        with Snirf(fpath, 'r') as s:
            self._fields['NIRSCoordinateUnits'].value = s.nirs[0].metaDataTags.LengthUnit


class Optodes(TSV):
    """Optodes Metadata Class

    Class object that mimics and contains the data for the optodes.tsv metadata file
    """

    def __init__(self, fpath=None):
        """Inherited constructor for the Optodes class

            Args:
                fpath: The file path to a reference SNIRF file
        """
        if fpath is not None:
            super().__init__()
            self.load_from_SNIRF(fpath)
            self._sidecar = self.make_sidecar()
        else:
            super().__init__()
    
    def load_from_SNIRF(self, fpath):
        """Creates the Optodes class based on information from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
        """

        self._source_snirf = fpath

        with Snirf(fpath, 'r') as s:
            src_labels = _get_source_labels(s)
            det_labels = _get_detector_labels(s)
            src_n = len(src_labels)
            det_n = len(det_labels)
            self._fields['name'].value = np.append(src_labels,
                                                   det_labels)
            self._fields['type'].value = np.append(['source'] * src_n,
                                                   ['detector'] * det_n)
            if s.nirs[0].probe.detectorPos3D is not None and s.nirs[0].probe.sourcePos3D is not None:
                self._fields['x'].value = np.append(s.nirs[0].probe.sourcePos3D[:, 0],
                                                    s.nirs[0].probe.detectorPos3D[:, 0])
                self._fields['y'].value = np.append(s.nirs[0].probe.sourcePos3D[:, 1],
                                                    s.nirs[0].probe.detectorPos3D[:, 1])
                if np.max(np.append(s.nirs[0].probe.sourcePos3D[:, 2], s.nirs[0].probe.detectorPos3D[:, 2])) > 0:
                    self._fields['z'].value = np.append(s.nirs[0].probe.sourcePos3D[:, 2],
                                                        s.nirs[0].probe.detectorPos3D[:, 2])
            elif s.nirs[0].probe.detectorPos2D is not None and s.nirs[0].probe.sourcePos2D is not None:
                self._fields['x'].value = np.append(s.nirs[0].probe.sourcePos2D[:, 0],
                                                    s.nirs[0].probe.detectorPos2D[:, 0])
                self._fields['y'].value = np.append(s.nirs[0].probe.sourcePos2D[:, 1],
                                                    s.nirs[0].probe.detectorPos2D[:, 1])
            else:
                raise SnirfFormatError('Cannot import optodes information from ' + fpath + '!')


class PhysioBatch:
    """Generates batch of Physio files based on a SNIRF file."""
    
    def __init__(self, fpath: str=None):
        self._physio = []
        if fpath is not None:
            self.load_from_SNIRF(fpath)
        
    def load_from_SNIRF(self, fpath: str):
        self._physio = []
        with Snirf(fpath, 'r') as s:
            n_aux = len(s.nirs[0].aux)
        for i in range(n_aux):
            self._physio.append(Physio(fpath, i))
                
    def __getitem__(self, i):
        return self._physio[i]


class Physio(TSV):
    
    def __init__(self, fpath=None, aux_index=0):
        """Encapsulates single *_physio.tsv file.
            Args:
                fpath: The file path to a reference SNIRF file
        """
        super().__init__()
        self._name = None
        if fpath is not None:
            # Sidecar is produced in overridden load_from_SNIRF
            self.load_from_SNIRF(fpath, aux_index=aux_index)
        
    def load_from_SNIRF(self, fpath: str, aux_index: int = 0):
        self._source_snirf = fpath
        self._index = aux_index
        with Snirf(fpath, 'r') as s:
            name = s.nirs[0].aux[aux_index].name
            data = s.nirs[0].aux[aux_index].dataTimeSeries
            t = s.nirs[0].aux[aux_index].time
            time_unit = s.nirs[0].metaDataTags.TimeUnit
            data_unit = s.nirs[0].aux[aux_index].dataUnit
            offset = s.nirs[0].aux[aux_index].timeOffset
            if any([v is None for v in [name, data, t, time_unit]]):
                raise SnirfFormatError("Cannot load *_physio.tsv from invalid AuxElement {} in {}".format(aux_index, fpath))
        self._fields['data'] = NumberArray(data)
        sc = {}
        if data.ndim > 1 and np.shape(data)[1] > 1:
            sc['Columns'] = ['{}_{}'.format(name, i) for i in range(np.shape(data)[1])]
        else:
            sc['Columns'] = [name]
        sc['SamplingFrequency'] = str(1 / (np.mean(np.diff(t)) * _get_time_unit(s.nirs[0].metaDataTags.TimeUnit)))
        if offset is None:
            sc['StartTime'] = '0.0'  # Assume no offset if not defined in SNIRF (optional)
        else:
            sc['StartTime'] = str(offset * _get_time_unit(s.nirs[0].metaDataTags.TimeUnit))
        self._sidecar = sc
        # Compose filenames
        entities = _extract_entities_from_filename(fpath)
        entities['recording'] = name
        self._filename = ''.join(['{}-{}_'.format(key, val) for (key, val) in entities.items()]) + 'physio'
        
    def names(self):
        return self._filename + '.tsv', self._filename + '.json'
        
            
            
            
class Channels(TSV):
    """Channels Metadata Class

    Class object that mimics and contains the data for the channels.tsv metadata file
    """

    def __init__(self, fpath=None):
        """Inherited constructor for the channels class

            Args:
                fpath: The file path to a reference SNIRF file
        """
        if fpath is not None:
            super().__init__()
            self.load_from_SNIRF(fpath)
            self._sidecar = self.make_sidecar()
        else:
            super().__init__()

    def load_from_SNIRF(self, fpath, load_aux=False):
        """Creates the channels class based on information from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
                load_aux: Optional. If True, aux channels are added to the *_channels.tsv file. Default False.
        """
        self._source_snirf = fpath

        with Snirf(fpath, 'r') as s:
            src_labels = _get_source_labels(s)
            det_labels = _get_detector_labels(s)
            wavelength = s.nirs[0].probe.wavelengths
            name = []
            source_list = []
            detector_list = []
            ctype = []
            wavelength_nominal = np.zeros(len(s.nirs[0].data[0].measurementList))

            for i in range(len(s.nirs[0].data[0].measurementList)):
                source_index = s.nirs[0].data[0].measurementList[i].sourceIndex
                detector_index = s.nirs[0].data[0].measurementList[i].detectorIndex
                wavelength_index = s.nirs[0].data[0].measurementList[i].wavelengthIndex

                name.append(src_labels[source_index - 1] + '-' + det_labels[detector_index - 1] + '-' +
                            str(wavelength[wavelength_index - 1]))

                if s.nirs[0].data[0].measurementList[i].dataTypeLabel is None:
                    datatype = s.nirs[0].data[0].measurementList[i].dataType
                else:
                    datatype = s.nirs[0].data[0].measurementList[i].dataTypeLabel
                ctype.append(_get_channel_type(datatype))

                source_list.append(src_labels[source_index - 1])
                detector_list.append(det_labels[detector_index - 1])
                wavelength_nominal[i] = wavelength[wavelength_index - 1]

            if load_aux and len(s.nirs[0].aux) > 0:
                append_nominal = np.empty((1, len(s.nirs[0].aux)))
                append_nominal[:] = np.NaN
                for j in range(len(s.nirs[0].aux)):
                    temp = s.nirs[0].aux[j].name
                    name.append(temp)
                    if "ACCEL" in temp:
                        ctype.append("ACCEL")
                    elif "GYRO" in temp:
                        ctype.append("GYRO")
                    elif "MAGN" in temp:
                        ctype.append("MAGN")
                    else:
                        ctype.append("MISC")
                    source_list.append("NaN")
                    detector_list.append("NaN")
                self._fields['wavelength_nominal'].value = np.append(wavelength_nominal, append_nominal)
            else:
                self._fields['wavelength_nominal'].value = wavelength_nominal

            self._fields['name'].value = np.array(name)
            self._fields['type'].value = np.array(ctype)
            self._fields['source'].value = np.array(source_list)
            self._fields['detector'].value = np.array(detector_list)


class Events(TSV):
    """Events Metadata Class

    Class object that mimics and contains the data for the events.tsv metadata file
    """

    def __init__(self, fpath=None):
        """Inherited constructor for the Events class

            Args:
                fpath: The file path to a reference SNIRF file
        """
        if fpath is not None:
            super().__init__()
            self.load_from_SNIRF(fpath)
            self._sidecar = self.make_sidecar()
        else:
            super().__init__()

    def load_from_SNIRF(self, fpath):
        """Creates the Events class based on information from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
        """
        self._source_snirf = fpath
        temp = None

        with Snirf(fpath, 'r') as s:
            for nirs in s.nirs:
                for stim in nirs.stim:
                    if stim.data.ndim > 1 and np.shape(stim.data)[1] > 2:
                        if temp is None:
                            temp = stim.data
                            label = np.array([stim.name] * stim.data.shape[0])
                            temp = np.append(temp, np.reshape(label, (-1, 1)), 1)
                        else:
                            new = np.append(stim.data, np.reshape(np.array([stim.name] * stim.data.shape[0]), (-1, 1)), 1)
                            temp = np.append(temp, new, 0)

            temp = temp[np.argsort(temp[:, 0])]
            self._fields['onset'].value = temp[:, 0]
            self._fields['duration'].value = temp[:, 1]
            self._fields['value'].value = temp[:, 2]
            self._fields['trial_type'].value = temp[:, 3]
            # Note: Only works with these fields for now, have to adjust for varying fields, especially those that are
            # not specified in the BIDS documentation


class Sidecar(JSON):
    """NIRS Sidecar(_nirs.JSON) Metadata Class

    Class object that mimics and contains the data for the _nirs.JSON metadata file
    """

    def __init__(self, fpath=None):
        """Inherited constructor for the Sidecar class

            Args:
                fpath: The file path to a reference SNIRF file
        """
        if fpath is not None:
            super().__init__()
            self.load_from_SNIRF(fpath)
        else:
            super().__init__()

    def load_from_SNIRF(self, fpath):
        """Creates the Sidecar class based on information from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
        """

        self._source_snirf = fpath

        with Snirf(fpath, 'r') as s:
            self._fields['SamplingFrequency'].value = 1 / (np.mean(np.diff(np.array(s.nirs[0].data[0].time))) * _get_time_unit(s.nirs[0].metaDataTags.TimeUnit))
            self._fields['NIRSChannelCount'].value = len(s.nirs[0].data[0].measurementList)
            self._fields['TaskName'].value = _pull_entity_value(fpath, 'task')
            if s.nirs[0].probe.detectorPos2D is None \
                    and s.nirs[0].probe.sourcePos2D is None:
                self._fields['NIRSSourceOptodeCount'].value = len(s.nirs[0].probe.sourcePos3D)
                self._fields['NIRSDetectorOptodeCount'].value = len(s.nirs[0].probe.detectorPos3D)
            elif s.nirs[0].probe.detectorPos3D is None \
                    and s.nirs[0].probe.sourcePos3D is None:
                self._fields['NIRSSourceOptodeCount'].value = len(s.nirs[0].probe.sourcePos2D)
                self._fields['NIRSDetectorOptodeCount'].value = len(s.nirs[0].probe.detectorPos2D)


class SnirfRun(object):
    """Encapsulates a single SNIRF file 'run' with fields containing the metadata.

    Attributes:
        coordsystem: Contains a Coordsystem class object
        optodes: Contains an Optodes class object
        channels: Contains a channels class object
        sidecar: Contains a Sidecar (_nirs.JSON) class object
        events: Contains an Events class object
        entities: Contains the `Run`/run information related to the data stored in a `Run` object
        participants: Contains the metadata related to the participants.tsv file

    """

    def __init__(self, fpath: str):
        """Constructor for the `Run` class"""
        
        # Need to ensure we are opening an existing file
        assert fpath.endswith('.snirf') and os.path.exists(fpath), 'No such SNIRF file: ' + fpath

        self.coordsystem = Coordsystem(fpath=fpath)
        self.optodes = Optodes(fpath=fpath)
        self.channels = Channels(fpath=fpath)
        self.physio = PhysioBatch(fpath=fpath)
        self.sidecar = Sidecar(fpath=fpath)
        self.events = Events(fpath=fpath)
        self.entities = _extract_entities_from_filename(fpath)
        assert 'sub' in self.entities, "Required entity 'sub' not found in SNIRF file name " + fpath 
        assert 'task' in self.entities, "Required entity 'task' not found in SNIRF file name " + fpath
        self.participants = {
            # REQUIRED BY SNIRF SPECIFICATION #
            'participant_id': 'sub-' + self.get_subj(),

            # RECOMMENDED BY BIDS #
            'species': _pull_participant('species', fpath=fpath),  # default Homo sapiens based on BIDS
            'age': _pull_participant('age', fpath=fpath),
            'sex': _pull_participant('sex', fpath=fpath),  # 1 is male, 2 is female
            'handedness': _pull_participant('handedness', fpath=fpath),
            'strain': _pull_participant('strain', fpath=fpath),
            'strain_rrid': _pull_participant('strain_rrid', fpath=fpath)
        }
        self.scans = {
            'filename': _pull_scans(self.entities, 'filename', fpath=fpath),
            'acq_time': _pull_scans(self.entities, 'acq_time', fpath=fpath)
        }

    def pull_task(self, fpath=None):
        """Pull the Task label from either the SNIRF file name or from the Sidecar class (if available)

            Args:
                fpath: The file path to the reference SNIRF file

            Returns:
                The task label/name
        """

        if self.sidecar.TaskName is None:
            return _pull_entity_value(fpath, 'task')
        else:
            return self.sidecar.TaskName

    def pull_fnames(self):
        """Check directory for files (not folders)
        
        Returns:
        A dictionary of file names for specific metadata files
        """
        fnames = {
            'optodes': '{}_optodes.tsv',
            'coordsystem': '{}_coordsystem.json',
            'sidecar': '{}_nirs.json',
            'events': '{}_events.tsv',
            'channels': '{}_channels.tsv'
        }
        
        for key in fnames.keys():
            fnames[key] = fnames[key].format(_make_filename_prefix(self.entities))
        
        return fnames

    def load_from_snirf(self, fpath):
        """Loads the metadata from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
        """

        self.coordsystem.load_from_SNIRF(fpath)
        self.optodes.load_from_SNIRF(fpath)
        self.channels.load_from_SNIRF(fpath)
        self.sidecar.load_from_SNIRF(fpath)

    def get_subj(self):
        """Obtains the subject ID/number for a particular `Run`/run

            Returns:
                The subject ID/number (returns an empty string if there is no information)
        """

        if self.entities['sub'] is None:
            return ''
        else:
            return self.entities['sub']

    def get_ses(self):
        """Obtains the session ID/number for a particular `Run`/run

            Returns:
                The session ID/number (returns an empty string if there is no information)
        """
        if 'ses' not in self.entities.keys():
            return None
        else:
            return self.entities['ses']

    def directory_export(self, fpath: str):
        """Exports/creates the BIDS-compliant metadata files based on information stored in the `Run` class object

            Args:
                outputFormat: The target destination and indirectly, the output format of the metadata file
                    The default value is 'Folder', which outputs the metadata file to a specific file directory
                    specified by the user
                    The other option is 'Text', which outputs the files and data as a string (JSON-like format)
                fpath: The file path that points to the folder where we intend to save the metadata files in

            Returns:
                A string containing the metadata file names and its content if the user chose the 'Text' output format
                or a set of metadata files in a specified folder if the user chose the default or 'Folder' output format
        """

        self.coordsystem.save_to_json(self.entities, fpath)
        self.optodes.save_to_tsv(self.entities, fpath)
        self.optodes.export_sidecar(self.entities, fpath)
        self.channels.save_to_tsv(self.entities, fpath)
        self.channels.export_sidecar(self.entities, fpath)
        self.sidecar.save_to_json(self.entities, fpath)
        self.events.save_to_tsv(self.entities, fpath)
        self.events.export_sidecar(self.entities, fpath)

    def export_to_dict(self):
        export = {}  # This is a deep copy. We want to return the entities we parsed to the client
        fnames = self.pull_fnames()

        # coordsystem.json
        export[fnames['coordsystem']] = json.dumps(self.coordsystem.get_all_fields())

        # optodes.tsv + json sidecar
        fieldnames, valfiltered, temp = self.optodes.get_all_fields()
        export[fnames['optodes']] = temp

        sidecarname = fnames['optodes'].replace('.tsv', '.json')
        export[sidecarname] = json.dumps(self.optodes.sidecar)

        # channels.tsv + json sidecar
        fieldnames, valfiltered, temp = self.channels.get_all_fields()
        export[fnames['channels']] = temp

        # *_physio.tsv + *_physio.json batch
        for physio in self.physio:
            fieldnames, valfiltered, temp = physio.get_all_fields(header=False)
            tsv_name, json_name = physio.names()
            export[tsv_name] = temp
            export[json_name] = json.dumps(physio.sidecar)

        # nirs sidecar
        export[fnames['sidecar']] = json.dumps(self.sidecar.get_all_fields())

        # event.tsv + json sidecar
        fieldnames, valfiltered, temp = self.events.get_all_fields()
        export[fnames['events']] = temp

        sidecarname = fnames['events'].replace('.tsv', '.json')
        export[sidecarname] = json.dumps(self.events.sidecar)

        # participant.tsv
        fields = self.participants
        text = _tsv_to_json(fields)
        export[_make_filename_prefix(self.entities) + '_participants.tsv'] = text

        # scans.tsv
        fields = self.scans
        text = _tsv_to_json(fields)
        export[_make_filename_prefix(self.entities) + '_scans.tsv'] = text

        return export


def snirf2bids(path_to_snirf: str, outputpath: str = None) -> str:
    """Creates BIDS metadata text files from a SNIRF file

        Args:
            inputpath (str): The file path to the reference SNIRF file
            outputpath (str): (Optional) The file path/directory for the created BIDS metadata files
    """
    run = SnirfRun(fpath=path_to_snirf)
    s = SnirfRun(fpath=path_to_snirf).export_to_dict()
    if outputpath is None:
        outputpath = os.path.join(os.path.split(path_to_snirf)[0])  # If no output location provided, put files next to input SNIRF
    for item in list(s.keys()):
        if item.endswith('.json'):
            with open(os.path.join(outputpath, item), 'w', newline='') as f:
                f.write(s[item])
        elif item.endswith('.tsv'):
            with open(os.path.join(outputpath, item), 'w', newline='') as f:
                f.write(s[item])

def snirf2json(path_to_snirf: str) -> str:
    run = SnirfRun(fpath=path_to_snirf)
    return json.dumps(run.export_to_dict())
