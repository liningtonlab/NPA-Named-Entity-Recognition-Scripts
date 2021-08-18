from taxonerd import TaxoNERD
import json
import re

SOURCE_ORGANISM_REGEX = "[A-Z]{1}\.?[a-z]+ {1}[a-z]+\.? ?[A-Z0-9-]+ ?[A-Z]?[a-zA-Z0-9-]+|[A-Z]{1}[a-z]+ {1}[a-z]+\.?|[A-Z]{1}\.? {1}[a-z]+\.? ?[A-Z0-9-]+ ?[A-Z]?[a-zA-Z0-9-]+"
# https://regexr.com/60t8c


def taxonerd_ner(abstract_text, ner):
    """ Detect source organism entities within abstract text via TaxoNERD, results cleaned via Regex pattern
                :param ner: TaxoNERD featureless instance required to run module
                :param abstract_text: raw string of abstract text
                :return: list of dictionaries, where each dict contains the match location and the source organism entity
                """

    taxon = ner.find_entities(abstract_text)
    entity = taxon.to_json(orient='records', lines=True)
    entities = entity.splitlines()

    proper_entity_list = []
    for ent in entities:
        string_dict_to_dictionary = json.loads(ent)
        #print(string_dict_to_dictionary)
        if re.search(SOURCE_ORGANISM_REGEX, string_dict_to_dictionary["text"]):
            proper_entity_list.append(ent)

    return proper_entity_list


def main():
    taxonerd = TaxoNERD(model="en_ner_eco_biobert", prefer_gpu=False,
                        with_abbrev=False)
    # Add with_linking="gbif_backbone" or with_linking="taxref" to activate entity linking

    with open("json_files/npatlas_origin_articles_for_NER_training.json", "r") as file:
        data = json.load(file)

        for item in data:
            abstract = item["reference"]["abstract"]
            actual_chemical_names = item["names"]

            if abstract:
                taxon = taxonerd_ner(abstract, taxonerd)
                print(taxon)

# TODO:
# Add length requirement to first/second words?


if __name__ == "__main__":
    main()
