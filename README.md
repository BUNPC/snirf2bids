![python](https://img.shields.io/pypi/pyversions/snirf2bids?color=green)
[![pypi](https://img.shields.io/pypi/v/snirf2bids?color=blue)](https://pypi.org/project/snirf2bids/)
[![tests](https://github.com/BUNPC/snirf2bids/actions/workflows/test.yml/badge.svg)](https://github.com/BUNPC/snirf2bids/actions/workflows/test.yml)

# snirf2BIDS
Conveniently generate [BIDS files](https://bids-specification--802.org.readthedocs.build/en/802/04-modality-specific-files/11-functional-near-infrared-spectroscopy.html) from [SNIRF files](https://github.com/fnirs/snirf).  

## Installation
### `pip install snirf2bids`

snirf2bids requires Python > 3.

## Usage
A SNIRF file with a [valid BIDS name](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#file-name-structure) can be converted into BIDS metadata text files.

For use with snirf2bids, a SNIRF file name must include at least the `sub-` and `task-` entitites and end in `_nirs.snirf`, i.e. `sub-01_task-tapping_nirs.snirf`.

### Create BIDS text files from a SNIRF file
```python
snirf2bids.snirf2bids('<path to snirf file>', '<folder to generate files in>')
```
### Export BIDS text files in JSON Format
```python
s = snirf2bids.snirf2json('<path to snirf file>')  # Returns serialized JSON in which keys are filenames and values are their contents
```

## Contributors

Developed by BU BME Senior Design Group 3 (2022): Christian Arthur, Jeonghoon Choi, Jiazhen Liu, Juncheng Zhang and the [Boston University Neurophotonics Center](https://github.com/BUNPC).

[@Christian Arthur :melon:](https://github.com/chrsthur)<br>
[@Juncheng Zhang :tangerine:](https://github.com/andyzjc)<br>
[@Jeonghoon Choi :pineapple:](https://github.com/jeonghoonchoi)<br>
[@Jiazhen Liu :grapes:](https://github.com/ELISALJZ)<br>

This project exists thanks to:
<br>
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
