# -*- coding: utf-8 -*-

'''
Created on 17 mar. 2022

@author: jose-lopez
'''
from pathlib import Path
import json
import sys

from about_time import about_time
from alive_progress import alive_bar
from alive_progress import alive_it
from spacy.matcher import Matcher
from spacy.tokens import Span, DocBin
import spacy


def load_jsonl(path):
    data = []
    lines = 0
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            if not line == "\n":
                # lines += 1
                # print(lines)
                data.append(json.loads(line))
    return data


def setting_patterns(patterns, matcher):

    current_line = 1

    labels = ["GOD", "PERSON", "PLACE", "GROUP", "WORK"]

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


def tagging_file_sentences(file_name, sentences, matcher, measures, nlp):

    FILE_PATH = "tagged/" + file_name + ".jsonl"

    sentences_to_report = []

    file = open(
        FILE_PATH, 'w', encoding="utf8")

    for sentence in sentences:

        doc = nlp(sentence)

        matches = matcher(doc)
        doc.ents = []
        spans = []
        """print([(doc[start:end], nlp.vocab.strings[match_id])
               for match_id, start, end in matches])"""
        for match_id, start, end in matches:
            current_span = Span(
                doc, start, end, label=nlp.vocab.strings[match_id])
            if not token_from_span_in(spans, current_span):
                spans.append(current_span)

        doc.ents = spans
        # print([(ent.text, ent.label_) for ent in doc.ents])

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

        sentences_to_report.append(
            f'{{"text":"{doc.text}", "spans":[{spans_}]}}')

        to_report = '\n'.join(s for s in sentences_to_report)

    file.write(''.join(to_report))

    file.close()


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


if __name__ == '__main__':

    # CORPUS_PATH = "data/corpus_en"
    CORPUS_PATH = "data/corpus_gr"
    # CORPUS_PATH = "data/corpus"
    PATTERNS_PATH = "data/patterns2.1.jsonl"
    # PATTERNS_PATH = "data/names_patterns_en.jsonl"

    print("\n" + "\n")
    print(">>>>>>> Starting the entities tagging...........")
    print("\n" + "\n")

    print("Loading the model...")
    nlp = spacy.load("grc_ud_proiel_lg")
    # nlp = spacy.load("en_core_web_sm")
    print(".. done" + "\n")

    print("Loading the entities' patterns...")
    matcher = Matcher(nlp.vocab)
    patterns = load_jsonl(PATTERNS_PATH)
    setting_patterns(patterns, matcher)
    print(".. done" + "\n")

    print("Processing the corpus for NER tagging.......")
    # Total of sentences in the corpus and the proportion of sentences required

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

            tagging_file_sentences(file_name, SENTENCES,
                                   matcher, measures, nlp)

            FILE_ON_PROCESS += 1

    else:

        print("No files to tag. Please check the contents in the data/corpus folder" + "\n")

    """print(
        f'Reporting some measures for a total of {len(files)} files (reports/measures.jsonl)' + "\n")"""

    print("\n" + "\n" + ">>>>>>> Entities tagging finished...........")
