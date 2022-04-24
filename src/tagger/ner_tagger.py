# -*- coding: utf-8 -*-

'''
Created on 17 mar. 2022

@author: jose-lopez
'''
from pathlib import Path
import json
import sys

from spacy.matcher import Matcher
from spacy.tokens import Span, DocBin
import spacy


def load_jsonl(path):

    data = []

    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            if not line == "\n":
                # lines += 1
                # print(lines)
                data.append(json.loads(line))
    return data


def setting_patterns(patterns, matcher):

    current_line = 1

    labels = ["PERSON", "PLACE", "GROUP", "WORK"]

    for name_pattern in patterns:

        if name_pattern["label"] in labels:
            matcher.add(name_pattern["label"], [name_pattern["pattern"]])
            current_line += 1
        else:
            print("There is an error on label value at line: {}".format(
                current_line))
            sys.exit()


def token_from_span_in(spans, current_span):

    already_present = False

    current_span_tokens = [t.i for t in current_span]

    for span in spans:

        span_tokens = [t.i for t in span]

        for token_index in span_tokens:
            if token_index in current_span_tokens:
                already_present = True

        if already_present is True:
            break

    return already_present


def tagging_file_sentences(file_n, sentences, matcher, measures, nlp):

    FILE_PATH = "tagged/" + file_n + ".jsonl"

    sentences_to_report = []
    len_sentences = len(sentences)
    no_entities_sentences = 0

    file_measures = {"file": file_n,
                     "len_file": len_sentences,
                     "PERSON": 0,
                     "PLACE": 0,
                     "GROUP": 0,
                     "WORK": 0,
                     "matches": 0,
                     "sentences_person": 0,
                     "sentences_place": 0,
                     "sentences_group": 0,
                     "sentences_work": 0}

    file = open(
        FILE_PATH, 'w', encoding="utf8")

    for doc in nlp.pipe(sentences):

        matches = matcher(doc)
        doc.ents = []
        spans = []
        contains_person = False
        contains_place = False
        contains_group = False
        contains_work = False

        for match_id, start, end in matches:

            label_ = nlp.vocab.strings[match_id]

            current_span = Span(
                doc, start, end, label=label_)

            if not token_from_span_in(spans, current_span):
                spans.append(current_span)

                if label_ == "PERSON":
                    file_measures["PERSON"] += 1
                    if not contains_person:
                        file_measures["sentences_person"] += 1
                        contains_person = True
                elif label_ == "PLACE":
                    file_measures["PLACE"] += 1
                    if not contains_place:
                        file_measures["sentences_place"] += 1
                        contains_place = True
                elif label_ == "GROUP":
                    file_measures["GROUP"] += 1
                    if not contains_group:
                        file_measures["sentences_group"] += 1
                        contains_group = True
                elif label_ == "WORK":
                    file_measures["WORK"] += 1
                    if not contains_work:
                        file_measures["sentences_work"] += 1
                        contains_group = True
                else:
                    print(
                        f'The label {label_} is not part of the set of entities to report.')
                    sys.exit(1)

        # print([(ent.text, ent.label_) for ent in doc.ents])

        doc.ents = spans

        file_measures["matches"] += len(doc.ents)

        ents_counter = 1
        spans_ = ""
        spans = []

        for ent in doc.ents:
            s_text = doc[0:ent.end].text
            t_len = doc[ent.start].__len__()
            start = len(s_text) - t_len
            end = start + t_len
            spans.append([start, end, ent.label_])

        for span in spans:

            label = span[2].replace("'", '"')
            # print(label)

            """print(
                f'{{"start":{span[0]},"end":{span[1]},"label":"{label}"}}')
            """

            if len(doc.ents) > ents_counter:
                spans_ = spans_ + \
                    f'{{"start":{span[0]},"end":{span[1]},"label":"{label}"}},'
                ents_counter += 1
            else:
                spans_ = spans_ + \
                    f'{{"start":{span[0]},"end":{span[1]},"label":"{label}"}}'

        if not doc.ents:
            spans_ = ""
            no_entities_sentences += 1

        sentences_to_report.append(
            f'{{"text":"{doc.text}", "spans":[{spans_}]}}')

    to_report = '\n'.join(s for s in sentences_to_report)

    file.write(''.join(to_report))

    file.close()

    file_measures["person_rate_local"] = file_measures["sentences_person"] / len_sentences
    file_measures["place_rate_local"] = file_measures["sentences_place"] / len_sentences
    file_measures["group_rate_local"] = file_measures["sentences_group"] / len_sentences
    file_measures["work_rate_local"] = file_measures["sentences_work"] / len_sentences
    file_measures["matches_rate_local"] = (
        len_sentences - no_entities_sentences) / len_sentences
    file_measures["person_index_local"] = file_measures["PERSON"] / len_sentences
    file_measures["place_index_local"] = file_measures["PLACE"] / len_sentences
    file_measures["group_index_local"] = file_measures["GROUP"] / len_sentences
    file_measures["work_index_local"] = file_measures["WORK"] / len_sentences
    file_measures["matches_index_local"] = file_measures["matches"] / len_sentences

    measures.append(file_measures)

    return measures


def from_corpus(CORPUS_PATH):

    corpus_length = 0

    files_ = [str(x) for x in Path(CORPUS_PATH).glob("**/*.txt")]

    if files_:

        for file_path_ in files_:
            with open(file_path_, 'r', encoding="utf8") as f:
                sentences = list(f.readlines())

            corpus_length += len(sentences)

    else:
        print(f'Not files at {CORPUS_PATH}')
        sys.exit()

    return corpus_length, files_


def export_measures(measures):

    path_measures = "reports/measures.jsonl"
    measures_to_report = []

    with open(path_measures, 'w', encoding="utf8") as fd:

        for measure in measures:

            measures_to_report.append(str(measure).replace("'", '"'))

        to_report = '\n'.join(m for m in measures_to_report)

        fd.write(''.join(to_report))


if __name__ == '__main__':

    if len(sys.argv) == 4:
        args = sys.argv[1:]
        MODEL = args[0].split("=")[1]
        PATTERNS_PATH = args[1].split("=")[1]
        CORPUS_PATH = args[2].split("=")[1]
    else:
        print("Please check the arguments at the command line")
        sys.exit()

    print("\n" + ">>>>>>> Starting the entities tagging..........." + "\n")

    print(f'Loading the model ({MODEL})....')
    nlp = spacy.load(MODEL)
    print(".. done" + "\n")

    print(f'Loading the patterns ({PATTERNS_PATH})....')
    matcher = Matcher(nlp.vocab)
    patterns = load_jsonl(PATTERNS_PATH)
    setting_patterns(patterns, matcher)
    print(".. done" + "\n")

    print(f'Processing the corpus ({CORPUS_PATH})....')

    # Total of sentences in the corpus and the its list of files
    corpus_length, files = from_corpus(CORPUS_PATH)

    FILE_ON_PROCESS = 1

    measures = []

    if not len(files) == 0:

        for file_path in files:

            file_name = file_path.split("/")[2]

            with open(file_path, 'r', encoding="utf8") as fl:
                SENTENCES = [line.strip() for line in fl.readlines()]

            print(
                f'..tagging entities for -> {file_name}: {FILE_ON_PROCESS} | {len(files)}')

            measures = tagging_file_sentences(file_name, SENTENCES,
                                              matcher, measures, nlp)

            FILE_ON_PROCESS += 1
        print(".... done")

        print("\n" +
              "Exporting the metrics for each file (reports/measures.jsonl)")
        export_measures(measures)
        print(".... done")

    else:

        print("No files to tag. Please check the contents in the data/corpus folder" + "\n")
        sys.exit()

    print("\n" + ">>>>>>> Entities tagging finished...........")
