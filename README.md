We describe here the execution of some python scripts, related to the NER tagging of certain types of entities in files written in Ancient Greek. The type of entities that are tagged are: person, place, group and work. Provided a collection of files, another collection of tagged files is generated. The aim here is to generate suitable files to support the fine tuning of models based on Transformers.

Requirements::

python 3.9.

spaCy version 3 (https://spacy.io)

Installation and execution:

1. First clone the repository:

git clone https://github.com/jose-lopez/ner_tagger.git

2. Change directory to the to the ner_tagger folder

3. Put the files of interest in the data/corpus folder.

4. The repository has two scripts of particular interest, ner_tagger.py and report_metrics.py. Ner_tagger.py is for the  generation of tagged files (saved in the tagged folder). The report_metrics.py script is for the report of some indicators generated according to the type of entity of interest (saved in the reports folder)

5. Located in the ner_tagger folder, two options can be used::

To tag a set of files:

$ python ./src/tagger/ner_tagger.py --model=<model> --patterns=<file_of_patterns> --corpus=<files_to_tag>

--model:  the name of the model to use.
--patterns:  the path to the patterns file
--corpus:  the path to the corpus to tag.

example:

$ python ./src/tagger/ner_tagger.py --model=grc_ud_proiel_lg --patterns=data/patterns2.1.jsonl --corpus=data/corpus

To generate a report:

$ python ./src/tagger/report_metrics.py --sorted_by=<rate|index> --entity_type=<ALL|PERSON|PLACE|GROUP|WORK>

--sorted_by=<rate|index>: Defines the order from highest to lowest of the tagged files, either by rate or entity index.
--entity_type=<ALL|PERSON|PLACE|GROUP|WORK>: Defines the type of entity to report. The 'ALL' option is for all kinds of entities.

 example:

$ python ./src/tagger/report_metrics.py --sorted_by=index --entity_type=ALL

An example follows:

1. Suppose the tagging is invoked as follows:

$ python ./src/tagger/ner_tagger.py --model=grc_ud_proiel_lg --patterns=data/patterns2.1.jsonl --corpus=data/corpus

Tagged files are saved in the 'tagged' folder. 

2. There are several types of reports depending on the kind of entity.

3. Suppose we request a report as follows:

$ python ./src/tagger/report_metrics.py --sorted_by=index --entity_type=ALL

The requested report is saved in reports/report_ALL_by_index.txt and lists the global percentages of entities in the entire corpus. For example:

G_PERSON_P: 89.01098901098901 G_PLACE_P: 4.945054945054945 ....

In this example, the first value corresponds to the global percentage of the entity PERSON.. In this case, 89.01% of the entities in the entire corpus correspond to that type of entity. The percentages are indicated in a similar way for the rest of the entities.

The report_ALL_by_index.txt file also shows the list of the corpus files ordered by index. The option index (named entity_index in the report), offers the average of entities per sentence in a file. Let's say the first file in the report has an entity_index of 2.40625. This means an average of entities for each sentence equal to 2.40625. Note that this average does not distinguish by type of entity. For a report about a particular kind of entity, run the following command:

$ python ./src/tagger/report_metrics.py --sorted_by=index --entity_type=PERSON

In this case the tagged files are sorted by index but the category is PERSON. Thus, the value 2.40625 would indicate that there is an average of 2.40625 for the PERSON kind of entity.

4. Suppose a report is now requested as follows:

$ python ./src/tagger/report_metrics.py --sorted_by=rate --entity_type=ALL

In this case the option 'rate' requests the proportion of sentences that have entities of any kind in the file. Let's say that we have a file with ten sentences and that only two of them have entities; each of the two sentences has six entities. The metrics would be:

entities_index = 12 / 10 = 1.2 (average number of entities per sentence in the file)
entities_rate = 2 /10 = 0.2 (average of sentences that have entities in the file)

In the example above the first value talks about the presence as follows

$ python ./src/tagger/report_metrics.py --sorted_by=rate --entity_type=ALL

In this case we speak of the proportion of sentences that have entities (of any type) in the file.

For example: Imagine that you have a file with 10 sentences, and only 2 of them have entities (each of the two sentences with 6 entities). So the metrics would be:

entities_index = 12 / 10 = 1.2 (average number of entities per sentence in the file)
entities_rate = 2 /10 = 0.2 (average sentences with entities relative to the total sentences in the file)

In the example above the first value talks about how present (on average) the entities are. In this case there is an average of 1.2 entities per sentence. The second value talks about how distributed the entities are in the sentences; that is, what is the proportion of sentences in the file that have entities.

5. The reports are saved in the ner_tagger/reports folder. The report name indicates the kind of entity and metric requested, for example: report_ALL_by_index.txt or report_PERSON_by_rate.txt.
