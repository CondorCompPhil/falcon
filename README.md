# Collazione

This repository contains data and scripts for a collation processing workflow, and it's evaluation.


- `collazione`: Python code;
- `data`: contains both input data, and manually annotated validation data for comparison.


## Installing

```bash
# Recommended steps (use virtualenv)
virtualenv env -p python3
source env/bin/activate
# end recommended steps, begin install
pip install -r requirements.txt
```

## Sample usage:

```bash
# Lemmatise raw (txt) files for ulterior collation
python3 main.py data/preproc/chevLyon/txt --lemmatise
# Collate annotated files in XML containing linguistic information
python3 main.py data/input/chevLyon/xml --collate
```



![collazione](https://upload.wikimedia.org/wikipedia/commons/8/8a/Barista_Fair_Trade_Coffee%2C_Gotgatan_67%2C_cappucino_%284386813991%29.jpg "Due cappucini")

