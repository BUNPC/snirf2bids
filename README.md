![python](https://img.shields.io/pypi/pyversions/snirf2bids?color=green)
[![pypi](https://img.shields.io/pypi/v/snirf2bids?color=blue)](https://pypi.org/project/snirf2bids/)
[![tests](https://github.com/BUNPC/snirf2bids/actions/workflows/test.yml/badge.svg)](https://github.com/BUNPC/snirf2bids/actions/workflows/test.yml)

# Installation

`pip install snirf2bids`

# Table of Contents
- [Introduction](#snirf2bids)
- [Features](#features)
  - [Create BIDS Structures](#create-bids-compliant-structures)
  - [Create BIDS Metadata Directory](#create-bids-compliant-metadata-directory)
  - [Create BIDS Metadata Files in JSON Format](#create-bids-compliant-metadata-files-in-json-format)

- [BIDS implementation](#bids-implementation)
- [Contributors](#contributors)

# snirf2BIDS
Conveniently generate BIDS structures from [SNIRF files](https://github.com/fnirs/snirf).  

[snirf2BIDS](https://pypi.org/project/snirf2bids/) requires [Python](https://www.python.org/downloads/) >3 and [h5py](https://www.h5py.org/) >3.6.

# Installation

`pip install snirf2bids`

# Features
- Create BIDS text files from a SNIRF file
- Export BIDS text files in JSON Format

# BIDS implementation

The fields and descriptions in JSON files are based on the latest [Brain Imaging Data Structure v1.7.1-dev](https://bids-specification--802.org.readthedocs.build/en/stable/04-modality-specific-files/11-functional-near-infrared-spectroscopy.html#channels-description-_channelstsv) 
and [SNIRF specification](https://github.com/fNIRS/snirf).

# Contributors

Developed by BU BME Senior Design Group 3 (2022): Christian Arthur, Jeonghoon Choi, Jiazhen Liu, Juncheng Zhang and the [Boston University Neurophotonics Center](https://github.com/BUNPC).
[@Christian Arthur :melon:](https://github.com/chrsthur)<br>
[@Juncheng Zhang :tangerine:](https://github.com/andyzjc)<br>
[@Jeonghoon Choi :pineapple:](https://github.com/jeonghoonchoi)<br>
[@Jiazhen Liu :grapes:](https://github.com/ELISALJZ)<br>

This project exists thanks to: <br>
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
