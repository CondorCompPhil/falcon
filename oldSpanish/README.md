# Old Spanish automatic collation

This repository contains data and scripts for a collation processing workflow for Old Spanish, and it's evaluation.

1. **Input**. The text of each of the different witnesses should be put in a `.txt` file; all these text files should be collected inside a folder `data/yourText/txt`.
2. **Pre-processing** (linguistic annotation). Before the collation, the texts are annotated with linguistic information such as lemma and part of speech. This step is perfomed using Freeling (its Python API) for Old Spanish. For Old French we recommend the use of Pie/Pandora.
3. **Collation**. The collation itself is done using [CollateX](https://pypi.org/project/collatex/). For the alignment, the lemma of each token is used. The rest of the info attached to each token can be retrieved in any moment, for visualization and further processing. We use it for adding a category to the variant, such as substantial, formal, morphological, etc.

Please note that you can go directly to step 3 only if you provide a file xml with the necessary info and structure, as indicated [below](#xml).

## This repo

- `lemm_coll`: Python code.
- `data`: contains input and output data, and manually annotated validation data for comparison.


## Installing

For **step 2**, [Freeling](http://nlp.lsi.upc.edu/freeling/) is needed. Install it from source, as indicated [here](https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/installation-source). Detailed info, including some necessary fixes, are listed here [below](#freeling).

For **step 3**, follow this:

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
python3 mainOldSpanish.py data/lucanor --lemmatise

# Collate annotated files in XML 
# containing (possibly human-corrected) linguistic information
python3 mainOldSpanish.py data/lucanor --collate

# Or, alternatively, do it all in one row
python3 mainOldSpanish.py data/lucanor --lemmatise --collate
```

<span id="xml"></span>
## Format for XML annotated files

If you want to use directly XML annotated files,
they must be in TEI, and contain `<w>` tags,
with `@lemma`, and possibly `@pos` and `@msd` tags,

```xml
<w
  lemma='mucho'
  pos='DI0FP0'
>muchas</w>
```
Or, possibly, use an `@type`,

```xml
<w 
  lemma="mucho"
  type="DI0FP0"
>muchas</w>
```


<span id="freeling"></span>
## Freeling installation for this pipeline

The following instructions are based on a Linux distribution, but instructions for other systems are available following the links to the Freeling documentation.

- Download release 4.1 or git clone https://github.com/TALP-UPC/FreeLing

- For using Freeling Python API, the development tools and FreeLing dependencies are needed, follow indications here: https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/installation-source/requirements-linux

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

- Fix and test old spanish 'es-old' configuration file

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

Change in es-old/constr_gram.dat -->	find and replace '\t\*' > '\tXX\*'
										find and replace ' \*\);' > ' XX\*\);'
Change in es-old/tagger.dat --> line 2, path was mistaken --> ../tagset.dat

<b>Test</b>
```bash
/usr/local/bin/analyze -f es-old.cfg < Desktop/ms6376.txt
```

- Test the Python api, as indicated here: https://talp-upc.gitbook.io/freeling-4-1-user-manual/installation/calling-freeling-library-from-languages-other-than-c++/apis-linux#python
Text for test should be at list one sentence for the program to be able to detect language. Default lang is spanish.
	
```bash
set FREELINGDIR=/usr/local
cd /usr/local/share/freeling/APIs/python3
python sample.py < mytext.txt > mytextOUTPUT.txt
```


