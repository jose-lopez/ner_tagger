We describe here the execution of some python scripts, related to the NER tagging of certain kind of entities in files written in Ancient Greek. The kind of entities tagged are: person, place, group and work. Provided a collection of files, another collection of tagged files is provided. The tagged files support the fine tuning of Language Modelling (LM) models based on Transformers.

Requirements:

python 3.9.

spaCy version 3 (https://spacy.io)

Installation and execution:

1. Clone the repository:

git clone https://github.com/jose-lopez/ner_tagger.git

2. Change directory to the ner_tagger folder.

3. Put the data files in the data/corpus folder.

4. The repository has two scripts of particular interest, ner_tagger.py and report_metrics.py. Ner_tagger.py is for the production of tagged files (saved in the tagged folder). The report_metrics.py script is for the report of some metrics produced according to the kind of entity selected (saved in the reports folder)

5. Options available:

----- Tagging a set of files------

$ python ./src/tagger/ner_tagger.py --model=<model> --patterns=<file_of_patterns> --corpus=<files_to_tag>

--model:  the name of the model to use to support the detection of entities.
 
--patterns:  the path to the file containing the patterns that describe the entities' to search for.
 
--corpus:  the path to the set of files (corpus) to tag.

For example:

$ python ./src/tagger/ner_tagger.py --model=grc_ud_proiel_lg --patterns=data/patterns2.1.jsonl --corpus=data/corpus

----- Producing a report -----

Different reports are available based on the kind of entity selected. Below the way we can run the code to get a report:

$ python ./src/tagger/report_metrics.py --sorted_by=<rate|index> --entity_type=<ALL|PERSON|PLACE|GROUP|WORK>

--sorted_by=<rate|index>: Defines the order of the tagged files from highest to lowest, either by rate or entity index.
 
--entity_type=<ALL|PERSON|PLACE|GROUP|WORK>: Defines the kind of entity to report. The 'ALL' option is for all kinds of entities.
 
For example:

$ python ./src/tagger/report_metrics.py --sorted_by=index --entity_type=ALL

-------------------

A detailed example follows:

1. Suppose the tagging of a corpus is ran as follows:

$ python ./src/tagger/ner_tagger.py --model=grc_ud_proiel_lg --patterns=data/patterns2.1.jsonl --corpus=data/corpus

The command above will produce a new tagged version of the corpus stored in the 'tagged' folder.

2. Suppose we request a report as follows:

$ python ./src/tagger/report_metrics.py --sorted_by=index --entity_type=ALL

The requested report is saved in reports/report_ALL_by_index.txt and it includes the global percentages of entities in the entire corpus, and the listing of the corpus' files' names sorted from highest to lowest, based on the index metric (explained below).

For example:

G_PERSON_P: 89.01098901098901 G_PLACE_P: 4.945054945054945 ....

In this example, the first value corresponds to the global percentage of the entity PERSON, meaning that 89.01% of the entities in the corpus correspond to that kind of entity. The percentages are indicated in a similar way for the rest of the entities.

Any report file also shows the name of the tagged files sorted by the related index or rate metric. The option index (named entity_index in the report), offers the average of entities per sentence in a file. Let's say the first file in the report has an entity_index of 2.40625; this means an average of entities in each sentence equal to 2.40625. Note that the average before does not distinguish the kind of entity. For a report about a particular kind of entity, run the command as follows:

$ python ./src/tagger/report_metrics.py --sorted_by=index --entity_type=PERSON

In this examples the tagged files are sorted by index but the category is PERSON. Thus, the value 2.40625 would indicate that there is an average of 2.40625 of the PERSON entity in the related file.

3. Suppose a report is requested as follows:

$ python ./src/tagger/report_metrics.py --sorted_by=rate --entity_type=ALL

In this example the option 'rate' requests the proportion of sentences in the file that have entities. Let's say that we have a file with ten sentences and that only two of them have entities, six entities each. The metrics would be:

entities_index = 12 / 10 = 1.2 (average of entities per sentence in the file).
 
entities_rate = 2 /10 = 0.2 (average of sentences that have entities in the file).

The entities_index talks about how present (on average) the entities are in the sentences of a file. In this example there is an average of 1.2 entities per sentence. On the other hand, the entities_rate talks about how distributed the entities are in the file; in other words, the proportion of sentences in the file that have entities.

4. The reports are saved in the ner_tagger/reports folder. The report's name indicates the kind of entity and the metric requested, for example: report_ALL_by_index.txt or report_PERSON_by_rate.txt.
