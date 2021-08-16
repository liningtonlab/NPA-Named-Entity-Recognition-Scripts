import re
import json
import compound_name_extractor


# Importing the list of class compounds from compound_name_extractor.py


def class_NER(abstract_text):
    """ Detects classes of compound from the abstract text using regex to also gather match object location. The tuple
    containing the match result and its match object is appended to the list of all match tuples.
        :param abstract_text: raw string of abstract text
        :return: List of tuples containing matches and their match object location
        """

    # List of class compounds imported from compound_name_extractor.py
    #
    for compound_class in compound_name_extractor.COMPOUND_CLASS:

        # Using regex to find iterable of matches using the list of compound classes from chemical name NER
        class_matches = re.finditer('((' + compound_class.lower() + ')[s]?|(' + compound_class.capitalize() + ')[s]?)',
                                    abstract_text)

        # New list of found matches
        found_matches = []

        # If a match is found, convert each match in the iterable into a tuple with the match object
        if class_matches:
            for match in class_matches:
                found_matches.append((match.group(), match.span()))

        if found_matches:
            return found_matches


def main():
    with open("json_files/npatlas_origin_articles_for_NER_training.json", "r") as file:
        data = json.load(file)

        for item in data:
            abstract = item["reference"]["abstract"]
            if abstract:
                if class_NER(abstract):
                    print(class_NER(abstract))


if __name__ == "__main__":
    main()
