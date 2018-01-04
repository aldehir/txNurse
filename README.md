# txnurse

Look up a registered nurse in Texas via license number.


## Installation

```
python setup.py install
```


## Usage

```
usage: txnurse [-h] [-o OUTPUT] license

positional arguments:
  license               license number

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file
```


## Example

Look up license number 1234,

```
$ txnurse 1234
```

Look up license number 1234, but output to `1234.json`

```
$ txnurse 1234 -o 1234.json
```


## Exit Codes

`txnurse` will exit with specific exit codes to denote the error that
occurred.

| Exit Code | Description                             |
| --------: | --------------------------------------- |
| 255       | Unknown error.                          |
| 10        | Unknown lookup error.                   |
| 11        | No content found on response page.      |
| 12        | No person found with the given license. |
