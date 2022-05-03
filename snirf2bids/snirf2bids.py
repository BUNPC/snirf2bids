""" Module for converting snirf file into bids format

Maintained by the Boston University Neurophotonics Center
"""

import csv
import json
import os
from warnings import warn

import numpy as np
from importlib_resources import files
from pysnirf2 import Snirf

try:
    from snirf2bids.__version__ import __version__ as __version__
except Exception:
    warn('Failed to load snirf2bids library version')
    __version__ = '0.0.0'


def _getdefault(fpath, key):
    """Get the fields/keys and corresponding values/descriptions from a JSON file.

        Args:
            fpath: The filepath to the JSON file containing the list of default fields (in string)
            key: The specific Metadata file extension such as _nirs.json, _optodes.tsv, etc. or specific key/field
                 declared within the dictionary in the JSON file.

        Returns:
            The dictionary stored within the specific key/field.
            Example output for _coordsystem.json from BIDS_fNIRS_subject_folder.JSON:
                {'RequirementLevel': 'CONDITIONAL',
                 'NIRSCoordinateSystem': 'REQUIRED',
                 'NIRSCoordinateUnits': 'REQUIRED',
                 'NIRSCoordinateSystemDescription': 'CONDITIONAL',
                 'NIRSCoordinateProcessingDescription': 'RECOMMENDED',
                 ...
                 'FiducialsDescription': 'OPTIONAL'}
    """
    filepaths = files("defaults")
    file = open(filepaths / fpath)
    fields = json.load(file)
    
    file.close()
        
    return fields[key]


def _pull_label(fpath, field):
    """Pull information values from filename if it is BIDS compliant

        Args:
            fpath: The filepath to the SNIRF file of reference
            field: The specific participant information field inquired (subject/session/run/task)

        Returns:
            The label for the specified field or None if the specific field cannot be found in the filename
    """

    if fpath is None:
        return None
    fname = fpath.split('/')[-1]
    if field not in fname and field == 'sub-':
        raise ValueError('Subject label is REQUIRED in file name')
    elif field not in fname and field == 'task-':
        raise ValueError('Task label is REQUIRED in file name')
    else:
        # if it is mentioned in the filename
        info = fname.split('_')
        for i in info:
            if field in i:
                if np.size(i.split(field)) == 1:
                    return None
                else:
                    return i.split(field)[1]
                    # need to get rid of non-alphanumeric for task name


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
        filename = _make_filename(classname, info, sidecar)
        filedir = fpath + '/' + filename
    else:
        raise ValueError("No subject info for BIDS file naming reference")

    return filedir


def _make_filename(classname, info, parameter=None):
    """Make file names based on file info

        Args:
            classname: The specific metadata class name (coordsystem, optodes, etc.)
            info: Subject info field from the Subject class
            parameter: Enter 'sidecar' when creating a TSV-accompanying sidecar file

        Returns:
            A BIDS formatted file name for the specific metadata file (in string)
            Example: sub-01_task-tapping_nirs.json for a _nirs.json file
    """

    subject = 'sub-' + info['sub-']
    task = '_task-' + info['task-']

    if info['ses-'] is None:
        session = ''
    else:
        session = '_ses-' + info['ses-']

    if info['run-'] is None:
        run = ''
    else:
        run = '_run-' + info['run-']

    if classname == 'optodes' and parameter == 'sidecar':
        return subject + session + '_optodes.json'
    elif classname == 'optodes' and parameter is None:
        return subject + session + '_optodes.tsv'
    elif classname == 'coordsystem':
        return subject + session + '_coordsystem.json'
    elif classname == 'events' and parameter == 'sidecar':
        return subject + session + task + run + '_events.json'
    elif classname == 'events' and parameter is None:
        return subject + session + task + run + '_events.tsv'
    elif classname == 'sidecar':
        return subject + session + task + run + '_nirs.json'
    elif classname == 'channels' and parameter == 'sidecar':
        return subject + session + task + run + '_channels.json'
    elif classname == 'channels' and parameter is None:
        return subject + session + task + run + '_channels.tsv'
    elif classname == 'scans' and parameter == 'init':
        return subject + session + task + run


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


def _pull_scans(info, field, fpath=None):
    """Creates the scans.tsv file

        Only works for a single SNIRF file for now with a predefined set of fields

        Args:
            info: subject information field (Subject.subinfo)
            field: field within scans.tsv file (filename or acq_time)
            fpath: file path of snirf file to extract scans.tsv from. OPTIONAL

        Returns:
            the string of the requested field parameter extracted from the snirf in fpath
    """
    if fpath is None:
        return None
    else:
        if field == 'filename':
            return 'nirs/' + _make_filename('scans', info, 'init') + '.snirf'
        elif field == 'acq_time':
            with Snirf(fpath) as s:
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


def _compliancy_check(bids):
    """Checks the BIDS compliancy by checking the values of required field. Prints Warning of anything is missing.
    Args:
        bids: Subject class object that is trying to be exported
    """
    run_object = bids.__dict__.keys()
    for x in run_object:
        if x in ['channels', 'coordsystem', 'events', 'optodes', 'sidecar']:
            class_spec = bids.__dict__[x].default_fields()[0]
            for field in class_spec.keys():
                if class_spec[field] == 'REQUIRED' and bids.__dict__[x]._fields[field].value is None:
                    message = 'FATAL: The field ' + field + ' is REQUIRED in the ' + x.capitalize() + ' class'
                    warn(message)
        elif x in ['subinfo']:
            pass
        elif x in ['participants', 'scans']:
            class_spec = _getdefault('BIDS_fNIRS_subject_folder.json', x + '.tsv')
            for field in class_spec.keys():
                if class_spec[field] == 'REQUIRED' and field not in bids.__dict__[x]:
                    message = 'FATAL: The field ' + field + 'is REQUIRED in ' + x.capitalize()
                    warn(message)
        else:
            raise ValueError('There is an invalid field ' + x + ' within your BIDS object')


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
        return np.array([]), 0
    return ['D' + str(i + 1) for i in range(n_det)], n_det
    

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
        return np.array([]), 0
    return ['S' + str(i + 1) for i in range(n_src)], n_src


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
        if "sidecar" in self.get_class_name().lower():
            default_list = _getdefault('BIDS_fNIRS_subject_folder.json', "_nirs.json")
            default_type = _getdefault('BIDS_fNIRS_subject_folder_datatype.json', "_nirs.json")
        elif isinstance(self, JSON):
            default_list = _getdefault('BIDS_fNIRS_subject_folder.json', "_" + self.get_class_name().lower() + ".json")
            default_type = _getdefault('BIDS_fNIRS_subject_folder_datatype.json',
                                       "_" + self.get_class_name().lower() + ".json")
        elif isinstance(self, TSV):
            default_list = _getdefault('BIDS_fNIRS_subject_folder.json', "_" + self.get_class_name().lower() + ".tsv")
            default_type = _getdefault('BIDS_fNIRS_subject_folder_datatype.json',
                                       "_" + self.get_class_name().lower() + ".tsv")
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
        if 'RequirementLevel' in defaults:
            del defaults['RequirementLevel']
        if 'RequirementLevel' in fields:
            del fields['RequirementLevel']
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

    def save_to_tsv(self, info, fpath):
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
            writer = csv.writer(tsvfile, dialect='excel-tab')  # writer setup in tsv format
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
        fields = _getdefault('BIDS_fNIRS_sidecar_files.json', self.get_class_name().lower())
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

    def get_all_fields(self):
        # VARIABLE DECLARATION
        temp = ''
        fields = list(self._fields)[1:]  # extract all fields
        values = list(self._fields.values())[1:]  # extract all values
        values = [values[i].value for i in range(len(values))]  # organize all values

        # VARIABLE ORGANIZATION
        fieldnames = []  # filter out the fieldnames with empty fields, and organize into row structure
        for i in range(len(fields) - 1):
            if values[i] is not None:
                fieldnames = np.append(fieldnames, fields[i])
                name = fields[i] + '\t'
                temp = temp + name
        name = fields[len(fields) - 1] + '\n'
        temp = temp + name
        valfiltered = list(filter(None.__ne__, values))  # remove all None fields
        valfiltered = np.transpose(valfiltered)  # transpose into correct row structure

        for one in valfiltered:
            looptemp = ''
            for j in range(len(one) - 1):
                looptemp = str(one[j]) + '\t'
                temp = temp + looptemp
            looptemp = str(one[len(one) - 1]) + '\n'
            temp = temp + looptemp

        return fieldnames, valfiltered, temp


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
        with Snirf(fpath) as s:
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

        with Snirf(fpath) as s:
            src_labels, src_n = _get_source_labels(s)
            det_labels, det_n = _get_detector_labels(s)
            self._fields['name'].value = np.append(src_labels,
                                                   src_labels)
            self._fields['type'].value = np.append(['source'] * src_n,
                                                   ['detector'] * det_n)
            if s.nirs[0].probe.detectorPos2D is None and s.nirs[0].probe.sourcePos2D is None:
                self._fields['x'].value = np.append(s.nirs[0].probe.sourcePos3D[:, 0],
                                                    s.nirs[0].probe.detectorPos3D[:, 0])
                self._fields['y'].value = np.append(s.nirs[0].probe.sourcePos3D[:, 1],
                                                    s.nirs[0].probe.detectorPos3D[:, 1])
                self._fields['z'].value = np.append(s.nirs[0].probe.sourcePos3D[:, 2],
                                                    s.nirs[0].probe.detectorPos3D[:, 2])
            elif s.nirs[0].probe.detectorPos3D is None and s.nirs[0].probe.sourcePos3D is None:
                self._fields['x'].value = np.append(s.nirs[0].probe.sourcePos2D[:, 0],
                                                    s.nirs[0].probe.detectorPos2D[:, 0])
                self._fields['y'].value = np.append(s.nirs[0].probe.sourcePos2D[:, 1],
                                                    s.nirs[0].probe.detectorPos2D[:, 1])


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

    def load_from_SNIRF(self, fpath):
        """Creates the channels class based on information from a reference SNIRF file

            Args:
                fpath: The file path to the reference SNIRF file
        """
        self._source_snirf = fpath

        with Snirf(fpath) as s:
            src_labels, n_src = _get_source_labels(s)
            det_labels, n_det = _get_detector_labels(s)
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
                    index = s.nirs[0].data[0].measurementList[i].dataType
                else:
                    index = s.nirs[0].data[0].measurementList[i].dataTypeLabel
                try:
                    temp = _getdefault('BIDS_fNIRS_measurement_type.json', str(index))
                except TypeError:
                    TypeError('Invalid dataTypeLabel in measurementList' + str(i))
                except KeyError:
                    temp = 'MISC'
                ctype.append(temp)

                source_list.append(src_labels[source_index - 1])
                detector_list.append(det_labels[detector_index - 1])
                wavelength_nominal[i] = wavelength[wavelength_index - 1]

            if len(s.nirs[0].aux) > 0:
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

        with Snirf(fpath) as s:
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

        with Snirf(fpath) as s:
            self._fields['SamplingFrequency'].value = np.mean(np.diff(np.array(s.nirs[0].data[0].time)))
            self._fields['NIRSChannelCount'].value = len(s.nirs[0].data[0].measurementList)
            self._fields['TaskName'].value = _pull_label(fpath, 'task-')
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
        subinfo: Contains the `Run`/run information related to the data stored in a `Run` object
        participants: Contains the metadata related to the participants.tsv file

    """

    def __init__(self, fpath=None):
        """Constructor for the `Run` class"""
        self.SNIRF = Snirf(fpath)

        self.coordsystem = Coordsystem(fpath=fpath)
        self.optodes = Optodes(fpath=fpath)
        self.channels = Channels(fpath=fpath)
        self.sidecar = Sidecar(fpath=fpath)
        self.events = Events(fpath=fpath)
        self.subinfo = {
            'sub-': _pull_label(fpath, 'sub-'),
            'ses-': _pull_label(fpath, 'ses-'),
            'task-': self.pull_task(fpath),
            'run-': _pull_label(fpath, 'run-')
        }
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
            'filename': _pull_scans(self.subinfo, 'filename', fpath=fpath),
            'acq_time': _pull_scans(self.subinfo, 'acq_time', fpath=fpath)
        }

    def pull_task(self, fpath=None):
        """Pull the Task label from either the SNIRF file name or from the Sidecar class (if available)

            Args:
                fpath: The file path to the reference SNIRF file

            Returns:
                The task label/name
        """

        if self.sidecar.TaskName is None:
            return _pull_label(fpath, 'task-')
        else:
            return self.sidecar.TaskName

    def pull_fnames(self):
        """Check directory for files (not folders)

        Returns:
             A dictionary of file names for specific metadata files based on the existence of a session label
             (different nomenclature) that are split into subject-level and session-level metadata files

             subj_fnames: Contains a dictionary of metadata filenames that are on the subject level
             ses_fnames: Contains a dictionary of metadata filenames that are on the session level

        Notes:
            Have to figure out how to do this based on the database structure
            In the case of the test snirf file, there is no presence of:
                1. session number
                2. run number
       """
        subj_fnames = None
        ses_fnames = None
        # Case of No SESSION OR RUN NUMBER
        if self.subinfo['ses-'] is None and self.subinfo['run-'] is None:
            fields = ['optodes', 'coordsystem', 'sidecar', 'events', 'channels']
            subj_fnames = {field: None for field in fields}
            keylist = list(subj_fnames.keys())
            for key in keylist:
                subj_fnames[key] = _make_filename(key, self.subinfo)

            ses_fnames = None

        # CASE OF SESSION EXISTING
        if self.subinfo['ses-'] is not None and self.subinfo['run-'] is None:
            subj_fields = ['optodes', 'coordsystem']
            ses_fields = ['sidecar', 'events', 'channels']

            subj_fnames = {field: None for field in subj_fields}
            keylist = list(subj_fnames.keys())
            for key in keylist:
                subj_fnames[key] = _make_filename(key, self.subinfo)

            ses_fnames = {field: None for field in ses_fields}
            keylist = list(ses_fnames.keys())
            for key in keylist:
                ses_fnames[key] = _make_filename(key, self.subinfo)

        if ses_fnames is None:
            return subj_fnames
        else:
            return subj_fnames | ses_fnames

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

        if self.subinfo['sub-'] is None:
            return ''
        else:
            return self.subinfo['sub-']

    def get_ses(self):
        """Obtains the session ID/number for a particular `Run`/run

            Returns:
                The session ID/number (returns an empty string if there is no information)
        """
        if self.subinfo['ses-'] is None:
            return None
        else:
            # Pull out the sessions here with a function
            return self.subinfo['ses-']

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

        self.coordsystem.save_to_json(self.subinfo, fpath)
        self.optodes.save_to_tsv(self.subinfo, fpath)
        self.optodes.export_sidecar(self.subinfo, fpath)
        self.channels.save_to_tsv(self.subinfo, fpath)
        self.channels.export_sidecar(self.subinfo, fpath)
        self.sidecar.save_to_json(self.subinfo, fpath)
        self.events.save_to_tsv(self.subinfo, fpath)
        self.events.export_sidecar(self.subinfo, fpath)

    def json_export(self):
        subj = self.subinfo
        subjnames = self.pull_fnames()

        # coordsystem.json
        name = 'coordsystem'
        temp = self.coordsystem.get_all_fields()
        subj[subjnames[name]] = temp

        # optodes.tsv + json sidecar
        name = 'optodes'
        fieldnames, valfiltered, temp = self.optodes.get_all_fields()
        subj[subjnames[name]] = temp

        sidecarname = _make_filename(name, subj, 'sidecar')
        subj[sidecarname] = self.optodes._sidecar

        # channels.tsv + json sidecar
        name = 'channels'
        fieldnames, valfiltered, temp = self.channels.get_all_fields()
        subj[subjnames[name]] = temp

        sidecarname = _make_filename(name, subj, 'sidecar')
        subj[sidecarname] = self.channels._sidecar

        # nirs sidecar
        name = 'sidecar'
        temp = self.sidecar.get_all_fields()
        subj[subjnames[name]] = temp

        # event.tsv + json sidecar
        name = 'events'
        fieldnames, valfiltered, temp = self.events.get_all_fields()
        subj[subjnames[name]] = temp

        sidecarname = _make_filename(name, subj, 'sidecar')
        subj[sidecarname] = self.events._sidecar

        # participant.tsv
        fields = self.participants
        text = _tsv_to_json(fields)
        subj['participants.tsv'] = text

        # scans.tsv
        fields = self.scans
        text = _tsv_to_json(fields)
        subj['scans.tsv'] = text

        text = json.dumps(subj)
        return text


def snirf2bids(inputpath: str, outputpath: str = None) -> str:
    """Creates BIDS metadata text files from a SNIRF file

        Args:
            inputpath: The file path to the reference SNIRF file
            outputpath: The file path/directory for the created BIDS metadata files
            participant: A dictionary with participant information
                Example =
                    {participant_id: 'sub-01',
                     age: 34,
                     sex: 'M'}
            scans: A dictionary with SNIRF/run information and its acquisition time
    """
    # checking directory
    if os.path.isfile(inputpath):
        run = SnirfRun(inputpath)
    else:
        return ValueError('Invalid directory to SNIRF file.')

    if outputpath is None:  # if output directory is not specified, it will be same as input
        outputpath = os.path.dirname(inputpath)

    if os.path.isdir(outputpath):
        subjpath = 'sub' + str(subj.subinfo['sub-'])
        outputpath = os.path.join(outputpath, subjpath)
        if not os.path.exists(outputpath):
            os.mkdir(outputpath)

        if subj.subinfo['ses-'] is not None:
            sespath = 'ses' + str(subj.subinfo['ses-'])
            outputpath = os.path.join(outputpath, sespath)
            if not os.path.exists(outputpath):
                os.mkdir(outputpath)

        outputpath = os.path.join(outputpath, 'nirs')
        if not os.path.exists(outputpath):
            os.mkdir(outputpath)
    else:
        return ValueError('Invalid directory to build BIDS folder.')

    run.directory_export(outputpath)

    # re-create source snirf file
    snirfoutput = os.path.join(outputpath, os.path.basename(inputpath))
    if not os.path.isfile(snirfoutput):
        run.SNIRF.save(snirfoutput)

    # This will probably work only with a single SNIRF file for now
    fname = outputpath + '/participants.tsv'
    with open(fname, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(run.participants.keys()), delimiter="\t", quotechar='"')
        writer.writeheader()
        writer.writerow(run.participants)

    # scans.tsv output, same thing as participants for scans
    fname = outputpath + '/scans.tsv'
    with open(fname, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(run.scans.keys()), delimiter="\t", quotechar='"')
        writer.writeheader()
        writer.writerow(run.scans)

    return run.json_export()


def snirf2json(path_to_snirf: str) -> str:
    run = SnirfRun(fpath=path_to_snirf)
    return run.json_export()

