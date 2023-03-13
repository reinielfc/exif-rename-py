# Exif Rename

This Python script is designed to rename media files by appending exif metadata to their filename. It provides an easy-to-use command-line interface with several options for customizing the renaming process.

## Installation

To use this script, you must have Python 3 installed on your system. You can download Python from the [official website](https://www.python.org/downloads).

In addition, you must install several dependencies, which can be installed using pip:

```sh
pip install exiftool colorama prettytable caseconverter pytz
```

## Usage

The `exif_rename.py` script takes several command-line arguments, which are described below.

### Required Arguments

- `FILES`: One or more files to rename. You can specify as many files as you want, separated by spaces.
- `-t TAG, --tag TAG`: The exif tag to add to the filename.

### Optional Arguments

- `-p, --prepend`: Prepend the tag to the filename.
- `-r, --replace`: Replace the current filename with the tag.
- `-m MAPPING [MAPPING ...], --mapping MAPPING [MAPPING ...]`: Apply a mapping function to transform the tag string. You can specify as many mapping functions as you want, separated by spaces. Available mapping functions are:
  - change case: 
    - simple: `capitalize`, `title`, `fold`, `lower`, `swap`, `upper`
    - standard: `camel`, `cobol`, `flat`, `kebab`, `macro`, `pascal`, `snake`
  - `detox`: replace special characters with underscore
  - date functions:
    - `date <format>`: convert with given format to iso format, default: `"%Y:%m:%d %H:%M:%S"`
    - `tz <timezone>`: add timezone, default `"US/Eastern"` (requires iso format)
    - `epoch`: convert date to epoch (requires iso format)
  - `int` convert to integer
  - `prefix <string>`: prefix tag with `string`
  - `suffix <string>`: suffix tag with `string`
  - `replace <old> <new> <count>`: replace ocurrences of `old` in tag with `new` `count` times
    - `<count>` default is -1 (all occurrences)
- `-n, --dry-run`: Do not rename files. Instead, print a list of the changes that would be made.

### Example Usage

To append the "DateTimeOriginal" exif tag to the end of the filename:

```sh
python exif_rename.py -t DateTimeOriginal my_file.jpg
```

To prepend the "DateTimeOriginal" exif tag to the beginning of the filename:

```sh
python exif_rename.py -t DateTimeOriginal -p my_file.jpg
```

To replace the filename with the "DateTimeOriginal" exif tag:

```
python exif_rename.py -t DateTimeOriginal -r my_file.jpg
```

To apply multiple mapping functions to the tag:

```sh
python exif_rename.py -t DateTimeOriginal -m date -m epoch -- my_file.jpg
```

To see what changes would be made without actually renaming the files:

```sh
python exif_rename.py -t DateTimeOriginal -n my_file.jpg
```
