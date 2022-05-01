[![snirf2bids](https://img.shields.io/pypi/v/snirf2bids?color=blue&label=snirf2bids&style=flat-square)](https://pypi.org/project/snirf2bids/0.1.7/)
[![pysnirf2](https://img.shields.io/pypi/v/pysnirf2?color=blue&label=pysnirf2&style=flat-square)](https://pypi.org/project/pysnirf2/)
![tests](https://img.shields.io/badge/tests-passing-green?style=flat-square&logo=github)
![python](https://img.shields.io/pypi/pyversions/snirf2bids?color=green&style=flat-square)
# Table of Contents
- [Introduction](#snirf2bids)
- [Features](#features)
  - [Create BIDS Compliant Structures](#create-bids-compliant-structures)
  - [Create BIDS-compliant Metadata Directory](#create-bids-compliant-metadata-directory)
  - [Create BIDS-compliant Metadata Files in JSON Format](#create-bids-compliant-metadata-files-in-json-format)

- [Code Generation](#code-generation)
- [Maintainers](#maintainers)
- [Contributors](#contributors)

 

# snirf2BIDS
Conveniently generate BIDS structure from `.snirf` files.  
Developed by BU BME Senior Design Group 3 (2022): Christian Arthur, Jeonghoon Choi, Jiazhen Liu, Juncheng Zhang.   
Will be maintained by [Boston University Neurophotonics Center(BUNPC)](https://github.com/BUNPC).  
[snirf2BIDS](https://pypi.org/project/snirf2bids/) requires [Python](https://www.python.org/downloads/) >3 and [h5py](https://www.h5py.org/) >3.6.

# Features

## Create BIDS-compliant Structures
`def snirf2bids(inputpath: str, outputpath: str = None):` creates a BIDS structure from a SNIRF file.   
Inputpath: The file path to the reference SNIRF file   
Outputpath: The file path/directory for the created BIDS metadata files   
Participants: A dictionary with participant information   
```python
def snirf2bids(inputpath: str, outputpath: str = None):
     if os.path.isfile(inputpath):
        subj = Subject(inputpath)
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

    subj.directory_export(outputpath)

    # re-create source snirf file
    snirfoutput = os.path.join(outputpath,os.path.basename(inputpath))
    if not os.path.isfile(snirfoutput):
        subj.SNIRF.save(snirfoutput)

    # This will probably work only with a single SNIRF file for now
    fname = outputpath + '/participants.tsv'
    with open(fname, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(subj.participants.keys()), delimiter="\t", quotechar='"')
        writer.writeheader()
        writer.writerow(subj.participants)
    f.close()

    # scans.tsv output, same thing as participants for scans
    fname = outputpath + '/scans.tsv'
    with open(fname, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(subj.scans.keys()), delimiter="\t", quotechar='"')
        writer.writeheader()
        writer.writerow(subj.scans)
    f.close()
 ```
 ## Create BIDS-compliant Metadata Directory
 ` def directory_export(self, fpath: str):` creats BIDS-compliant metadata files based on information stored in `subject` class.
 

```python
        def directory_export(self, fpath: str):

        self.coordsystem.save_to_json(self.subinfo, fpath)
        self.optodes.save_to_tsv(self.subinfo, fpath)
        self.optodes.export_sidecar(self.subinfo, fpath)
        self.channels.save_to_tsv(self.subinfo, fpath)
        self.channels.export_sidecar(self.subinfo, fpath)
        self.sidecar.save_to_json(self.subinfo, fpath)
        self.events.save_to_tsv(self.subinfo, fpath)
        self.events.export_sidecar(self.subinfo, fpath)

``` 
## Create BiDS-compliant Metadata Files in JSON Format
` def json_export(self):` creats BIDS-compliant metadata files in JSON format. Returns a string containing the metadata file names and its content.

```python
       def json_export(self):
        subj = self.subinfo
        subjnames= self.pull_fnames()

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

``` 
# Code Generation

The fields and descriptions in JSON files are generated based on the latest [Brain Imaging Data Structure v1.7.1-dev](https://bids-specification--802.org.readthedocs.build/en/stable/04-modality-specific-files/11-functional-near-infrared-spectroscopy.html#channels-description-_channelstsv) 
and [SNIRF specification](https://github.com/fNIRS/snirf).

# Maintainers
[@Christian Arthur :melon:](https://github.com/chrsthur)<br>
[@Juncheng Zhang :tangerine:](https://github.com/andyzjc)<br>
[@Jeonghoon Choi :pineapple:](https://github.com/jeonghoonchoi)<br>
[@Jiazhen Liu :grapes:](https://github.com/ELISALJZ)<br>
[Boston University Neurophotonics Center(BUNPC)](https://github.com/BUNPC)<br>

# Contributors
This project exsists thanks to all people who contribute. <br>
<center class= "half">
<a href="https://github.com/sstucker">
<img src="https://github.com/sstucker.png" width="50" height="50">
</a>

<a href="https://github.com/rob-luke">
<img src="https://github.com/rob-luke.png" width="50" height="50">
</a>

<a href="https://github.com/chrsthur">
<img src="https://github.com/chrsthur.png" width="50" height="50">
</a>

<a href="https://github.com/andyzjc">
<img src="https://github.com/andyzjc.png" width="50" height="50">
</a>

<a href="https://github.com/jeonghoonchoi">
<img src="https://github.com/jeonghoonchoi.png" width="50" height="50">
</a>

<a href="https://github.com/ELISALJZ">
<img src="https://github.com/ELISALJZ.png" width="50" height="50">
</a>
  
<a href="https://github.com/dboas">
<img src="https://github.com/dboas.png" width="50" height="50">
</a>
                                                     </center>
