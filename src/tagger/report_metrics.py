'''
Created on 8 abr. 2022

@author: jose-lopez
'''
import json
import sys


def load_jsonl(path):

    data = []

    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            if not line == "\n":
                # lines += 1
                # print(lines)
                data.append(json.loads(line))
    return data


def report(measures, arguments):

    global_measures = {
        "PERSON": 0,
        "PLACE": 0,
        "GROUP": 0,
        "WORK": 0,
        "global_person_rate": 0,
        "global_place_rate": 0,
        "global_group_rate": 0,
        "global_work_rate": 0,
        "global_entities": 0
    }

    for record in measures:
        global_measures["PERSON"] += record["PERSON"]
        global_measures["PLACE"] += record["PLACE"]
        global_measures["GROUP"] += record["GROUP"]
        global_measures["WORK"] += record["WORK"]
        global_measures["global_entities"] += record["matches"]

    global_items = global_measures.items()
    for key, value in global_items:
        if key == "PERSON":
            global_measures["global_person_rate"] = (value /
                                                     global_measures["global_entities"]) * 100
        if key == "PLACE":
            global_measures["global_place_rate"] = (value /
                                                    global_measures["global_entities"]) * 100
        if key == "GROUP":
            global_measures["global_group_rate"] = (value /
                                                    global_measures["global_entities"]) * 100
        if key == "WORK":
            global_measures["global_work_rate"] = (value /
                                                   global_measures["global_entities"]) * 100

    sorted_by = arguments[0].split("=")[1]
    entitiy_type = arguments[1].split("=")[1]

    if sorted_by == "index":
        if entitiy_type == "ALL":
            order_by = "matches_index_local"
        elif entitiy_type == "PERSON":
            order_by = "person_index_local"
        elif entitiy_type == "PLACE":
            order_by = "place_index_local"
        elif entitiy_type == "GROUP":
            order_by = "group_index_local"
        elif entitiy_type == "WORK":
            order_by = "work_index_local"
        else:
            print(
                f'Please check the argument <{entitiy_type}> at the command line interface')

    elif sorted_by == "rate":
        if entitiy_type == "ALL":
            order_by = "matches_rate_local"
        elif entitiy_type == "PERSON":
            order_by = "person_rate_local"
        elif entitiy_type == "PLACE":
            order_by = "place_rate_local"
        elif entitiy_type == "GROUP":
            order_by = "group_rate_local"
        elif entitiy_type == "WORK":
            order_by = "work_rate_local"
        else:
            print(
                f'Please check the argument <{entitiy_type}> at the command line interface')
    else:
        print(
            f'Please check the argument <{sorted_by}> at the command line interface')

    measures.sort(key=lambda x: x[order_by], reverse=True)

    path_ = "reports/report_" + entitiy_type + "_by_" + sorted_by + "_.txt"

    g_person_p = global_measures["global_person_rate"]
    g_place_p = global_measures["global_place_rate"]
    g_group_p = global_measures["global_group_rate"]
    g_work_p = global_measures["global_work_rate"]

    with open(path_, 'w', encoding="utf8") as fd:

        print(
            "\n" + f'Reporting the list of files sorted by {sorted_by}: entity type --> {entitiy_type}' + "\n" + "\n")
        fd.write(
            "\n" + f'Reporting the list of files sorted by {sorted_by}: entity type --> {entitiy_type}' + "\n" + "\n")

        print(f'Global percentages for each entity type in the corpus:' + "\n")
        fd.write(f'Global percentages for each entity type in the corpus:' + "\n")
        print(
            f'G_PERSON_P: {g_person_p}    G_PLACE_P: {g_place_p}    G_GROUP_P: {g_group_p}    G_WORK_P: {g_work_p}' + "\n" + "\n")
        fd.write(
            f'G_PERSON_P: {g_person_p}    G_PLACE_P: {g_place_p}    G_GROUP_P: {g_group_p}    G_WORK_P: {g_work_p}' + "\n" + "\n")

        print("Files:" + "\t" + "\t" + "\t" + "\t" +
              "Sorted by: " + sorted_by + "\n")
        fd.write("Files:" + "\t" + "\t" + "\t" + "\t" +
                 "Sorted by: " + sorted_by + "\n")

        for measure in measures:
            print(measure["file"] + "\t" + "\t" +
                  "\t" + str(measure[order_by]) + "\n")
            fd.write(measure["file"] + "\t" + "\t" +
                     "\t" + str(measure[order_by]) + "\n")


if __name__ == '__main__':

    PATH_MEASURES = "reports/measures.jsonl"

    measures = load_jsonl(PATH_MEASURES)

    report(measures, sys.argv[1:])
