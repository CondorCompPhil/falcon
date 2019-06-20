# Collazione

This repository contains data and scripts for a collation processing workflow, and it's evaluation.


- `lemm_coll`: Python code;
- `data`: contains pre-processed data (sources in txt or xml), input data, and manually annotated validation data for comparison.


## Installing

```bash
# Recommended steps (use virtualenv)
virtualenv env -p python3
source env/bin/activate
# end recommended steps, begin install
# install everything needed for linguistic annotation of the texts using Pie and for collation
# installation requirements for medieval Spanish are listed below
pip install -r requirements.txt
```


## Sample usage

```bash
# Lemmatise raw (txt) files for ulterior collation
python3 main.py data/preproc/chevLyon/sources --lemmatise
# Collate annotated files in XML containing (possibly human-corrected) linguistic information
# This step requires a XML folder at the same level of the 'sources' folder
python3 main.py data/input/chevLyon/xml --collate
# Or, alternatively, do it all in one row
python3 main.py data/preproc/chevLyon/sources --lemmatise --collate
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




<span id="freeling"></span>
## Freeling installation for this pipeline

The following instructions are based on a Linux distribution, but instructions for other systems are available following the links to the Freeling documentation.

- Install SWIG, as indicated here https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/calling-freeling-library-from-languages-other-than-c++/apis-linux#apis-requirements

- Install freeling from sources (needed for API), as indicated here https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/installation-source Attention: add argument for Python3 to `cmake ..`
```bash
cmake .. -DPYTHON3_API=ON`
```
- Test freeling (https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/using-freeling/test-linux):

```bash
/usr/local/bin/analyze -f en.cfg < Desktop/mytext.txt
/usr/local/bin/analyze -f en.cfg < Desktop/mytext.txt --output xml
```

- Fix and test medieval Spanish 'es-old' configuration file

Change in /usr/local/share/freeling/es/es-old/dicc.src --> lines 1 to 5 become
```xml
<IndexType>
DB_MAP
<\IndexType>
<Entries>
&cetera etcétera Fs etcétera NCMS000
```
Change in es-old.cfg --> line 77, path was mistaken --> ProbabilityFile=$FREELINGSHARE/es/es-old/probabilitats.dat

Change in es-old/probabilitats.dat --> line 13, path was mistaken --> ../tagset.dat

Change in es-old/constr_gram.dat -->	find and replace '\t\*' > '\tXX\*' ; and find and replace ' \*\);' > ' XX\*\);'

Change in es-old/tagger.dat --> line 2, path was mistaken --> ../tagset.dat

<b>Test</b>
```bash
/usr/local/bin/analyze -f es-old.cfg < Desktop/ms6376.txt
```

- Test the Python api, as indicated here

https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/calling-freeling-library-from-languages-other-than-c++/apis-linux#python

Text for test should be at list one sentence for the program to be able to detect language. Default lang is spanish.
	
```bash
set FREELINGDIR=/usr/local
cd /usr/local/share/freeling/APIs/python3
python sample.py < mytext.txt > mytextOUTPUT.txt
```


