# This is an unofficial tool that is in no way affiliated with CoronaCheck.nl or the Ministry of VWS. You have been warned!

# coronacheck-tools
coronacheck-tools is a python package and cli tool that allows you to dump the contents of the qr code generated at https://coronacheck.nl either through the app or the website or on paper. This allows others to get some insight into the data stored in these QR Codes.

# Installation


# Interpolation
Interpolation of the mask between slices is currently unsupported. Send us an algorithm or a pull requests and we'll happly add it.

# Input file format
The DICOM and RT-Struct inputs need to be unzipped in a directory. Currently this is the only way to read the input files.

# CLI Tool
```
# install using pip and show tool help
pip install dcmrtstruct2nii
dcmrtstruct2nii --help

# list structures in DICOM RT Struct
dcmrtstruct2nii list -r /path/to/rtstruct/file

# convert help output
dcmrtstruct2nii convert --help

# convert DICOM RT Structs to .nii.gz masks
dcmrtstruct2nii convert -r /path/to/rtstruct/file.dcm -d /path/to/original/extracted/dicom -o /output/path
```

# Python API
```
# install using pip and show tool help
pip install dcmrtstruct2nii
```

```
# lets test it
from dcmrtstruct2nii import dcmrtstruct2nii, list_rt_structs

print(list_rt_structs('/path/to/dicom/rtstruct/file.dcm'))

dcmrtstruct2nii('/path/to/dicom/rtstruct/file.dcm', '/path/to/original/extracted/dicom/files', '/output/path')
```

# License and academic use

The program is licensed [Apache license 2.0](https://github.com/Sikerdebaard/dcmrtstruct2nii/blob/master/LICENSE).

For academic use, use a presistent copy from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4037865.svg)](https://doi.org/10.5281/zenodo.4037865). 

Please cite:

```Phil, T. (2020). Sikerdebaard/dcmrtstruct2nii: v1.0.19 (v1.0.19) [Computer software]. Zenodo. https://doi.org/10.5281/ZENODO.4037865```
