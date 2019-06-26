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

## Sample usage

```bash
# Lemmatise raw (txt) files for ulterior collation
python3 main.py data/preproc/chevLyon/txt --lemmatise
# Collate annotated files in XML 
# containing (possibly human-corrected) linguistic information
python3 main.py data/input/chevLyon/xml --collate
# Or, alternatively, do it all in one row
python3 main.py data/preproc/chevLyon/txt --lemmatise --collate
```

To evaluate the results:

```bash
python eval.py <path_to_gt> <path_to_results> [--print_diff]
# e.g., evaluate Alexis results
python eval.py data/eval/alexis/ALEXIS_gt.xml data/eval/alexis/ALEXIS_out.xml
```

## Format for XML annotated files

If you want to use directly XML annotated files,
they must be in TEI, and contain `<w>` tags,
with `@lemma`, and possibly `@pos` and `@msd` tags,

```xml
<w 
  lemma="mëisme" 
  pos="ADJind" 
  msd="NOMB.=s|GENRE=m|CAS=r"
>meisme</w>
```
Or, possibly, use an `@type`,

```xml
<w 
  lemma="mëisme"
  type="ADJind|NOMB.=s|GENRE=m|CAS=r"
>meisme</w>
```


![collazione](https://upload.wikimedia.org/wikipedia/commons/8/8a/Barista_Fair_Trade_Coffee%2C_Gotgatan_67%2C_cappucino_%284386813991%29.jpg "Due cappucini")

