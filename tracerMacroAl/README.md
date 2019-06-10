
#Test of macro alignment with [Tracer](https://www.etrap.eu/research/tracer/).


Macro-alignment is useful to identify corresponding sections to collate.

## This repo
- `reorderTracerTable4collation.py` takes Tracer output table and reorder it, moving all aligned sections to the same row
- 'roudTracer.csv' is an example of Tracer output table
- 'roudTracer_onlyRelevantData.csv' and 'roudTracer_onlyRelevantData_reordered.csv' are created by the script. The final result is the second. The cell of each row correspond to the witnesses and can be collated.


## Steps
1. Run Tracer and output results in tabular format, see [Tracer manual](https://gfranzini.gitbooks.io/tracer/content/beta/results-as-csv.html). For preparing the data for Tracer follow the manual; some [Python scripts](https://github.com/mikekestemont/potter/blob/master/harry/intertextuality/intertextuality.ipynb) and [R scripts](https://github.com/editio/tracer-scripts) are also available
2. Deduplicate results. For example with `sort -u myfile.csv -o myfile.csv`
3. Run `reorderTracerTable4collation.py` on results

## For testing
Go to step 3 above: run `reorderTracerTable4collation.py` on the csv provided 'roudTracer.csv'.


## Is this useful?
Test with *Alexis* lemmatized with Pyrrha: shuffle two verses and give to Tracer to identify --> only one identified; best parameters: results score 0.2, frequency 0.8. Probably better on longer units, such as paragraphs! Test further ...

