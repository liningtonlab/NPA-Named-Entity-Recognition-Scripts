import csv
import json

import compound_name_extractor


def sort_list(unsorted_list):
    """ Function to sort a list based on the length of the string.
                        :param unsorted_list: list to be sorted
                        :return: sorted list"""
    sorted_list = sorted(unsorted_list, key=len, reverse=True)
    return sorted_list


def add_to_compound_classes(list_of_additions):
    """ Function to sort a list based on the length of the string.
                        :param list_of_additions: list of classes of compound to be added to growing list of classes.
                        :return: new list of compound classes containing new additions"""
    for item in list_of_additions:
        new_item = item[:-1].upper()
        if new_item not in compound_name_extractor.COMPOUND_CLASS:
            compound_name_extractor.COMPOUND_CLASS.append(item[:-1].upper())


def bracket_matched(string):
    """ Function to check if brackets are matched; For every open bracket, there should be a matching closed bracket.
                    :param string: string to be checked
                    :return: count if == 0, else returns false"""
    count = 0
    for i in string:
        if i in ["(", "[", "{", "<"]:
            count += 1
        elif i in [")", "]", "}", ">"]:
            count -= 1
        if count < 0:
            return False
    return count == 0


# Python3 program to remove invalid parenthesis using modified code from: https://www.geeksforgeeks.org/remove-invalid-parentheses/
def is_parentheses(c):
    """ Method checks if character is parenthesis(open or closed)
            :param c: character
            :return: if it is open/closed parentheses
            """
    return (c == '(') or (c == ')')


def remove_invalid_parentheses(string):
    """ Method to remove invalid parenthesis
                    :param string: string
                    :return: False if open bracket otherwise 0 when valid parentheses
                    """
    if len(string) == 0:
        return

    # visit set to ignore already visited
    visit = set()

    # queue to maintain BFS
    q = []
    temp = 0
    level = 0

    # pushing given as starting node into queue
    q.append(string)
    visit.add(string)
    while len(q):
        string = q[0]
        q.pop()

        if bracket_matched(string):
            level = True  # If answer is found, make level true; so that valid of only that level are processes
            return string

        if level:
            continue
        for i in range(len(string)):
            if not is_parentheses(string[i]):
                continue

            # Removing parenthesis from str and pushing into queue,if not visited already
            temp = string[0:i] + string[i + 1:]
            if temp not in visit:
                q.append(temp)
                visit.add(temp)


def json_csv(input_file, output_file):
    """ Method to extract the chemical named-entities from json file and append data to csv file.
                        :param output_file: file where output data is written.
                        :param input_file: json file containing abstracts and other information from NPAtlas.
                        :return: None
                        """
    with open(input_file, "r") as file:
        data = json.load(file)
        with open(output_file, "w", encoding="utf-8") as filer:
            headers = ['doi', 'abstract', 'detected_compounds', 'detection_number',
                       'actual_compound', 'actual_compnum']
            writer = csv.DictWriter(filer, fieldnames=headers)
            writer.writeheader()
            for item in data:
                abstract = item["reference"]["abstract"]
                doi = item["reference"]["doi"]
                actual_chemical_names = item["names"]
                if abstract and type(abstract) == str:
                    abstract_clone = abstract
                    chemical_detection_list = compound_name_extractor.clean_detected_items(abstract)
                    chemical_detection_list_no_open_parentheses = compound_name_extractor.improper_parentheses_capture(
                        chemical_detection_list)
                    length_chems = len(chemical_detection_list_no_open_parentheses)

                    abs_dict = {"doi": doi, "abstract": abstract_clone, "actual_compound": actual_chemical_names,
                                "actual_compnum": len(actual_chemical_names),
                                "detected_compounds": chemical_detection_list_no_open_parentheses,
                                "detection_number": length_chems}
                    writer.writerow(abs_dict)

                else:
                    continue
