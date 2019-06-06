# Logic formula generator

## Install

Python 3.7 required


Additionally for generatring antrl4 parser install antlr4 executable and execute:

```bash
antlr4 -visitor -Dlanguage=Python3 tptp.g4
```

Do not edit files in `antrl` directory except grammar file `tptp.g4`. The rest is generated automatically by antlr

## Run

```sh
python main.py
```

Get help with `python main.py -h`

