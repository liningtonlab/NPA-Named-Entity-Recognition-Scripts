from taxonerd import TaxoNERD
import json
import re

SOURCE_ORGANISM_REGEX = "[A-Z]{1}[a-z]+ {1}[a-z]+\.? ?[A-Z0-9-]+ ?[A-Z]?[a-zA-Z0-9-]+|[A-Z]{1}[a-z]+ {1}[a-z]+\.?"
# https://regexr.com/60t8c

ner = TaxoNERD(model="en_ner_eco_biobert", prefer_gpu=False,
                   with_abbrev=False)

'''def taxonerd_ner(abstract_text):
    """ Detect source organism entities within abstract text via TaxoNERD, results cleaned via Regex pattern
                :param abstract_text: raw string of abstract text
                :return: list of dictionaries, where each dict contains the match location and the source organism entity
                """
    ner = TaxoNERD(model="en_ner_eco_biobert", prefer_gpu=False,
                   with_abbrev=False)
    # Add with_linking="gbif_backbone" or with_linking="taxref" to activate entity linking

    taxon = ner.find_entities(abstract_text)
    entity = taxon.to_json(orient='records', lines=True)
    entities = entity.splitlines()

    proper_entity_list = []
    for ent in entities:
        string_dict_to_dictionary = json.loads(ent)
        if re.search(SOURCE_ORGANISM_REGEX, string_dict_to_dictionary["text"]):
            proper_entity_list.append(ent)

    return proper_entity_list'''


def main():
    with open("npatlas_origin_articles_for_NER_training.json", "r") as file:
        data = json.load(file)

        for item in data:
            abstract = item["reference"]["abstract"]
            actual_chemical_names = item["names"]

            if abstract:

                taxon = ner.find_entities(abstract)
                entity = taxon.to_json(orient='records', lines=True)
                entities = entity.splitlines()

                proper_entity_list = []
                for ent in entities:
                    string_dict_to_dictionary = json.loads(ent)
                    if re.search(SOURCE_ORGANISM_REGEX, string_dict_to_dictionary["text"]):
                        proper_entity_list.append(ent)
                print(proper_entity_list)

# TODO:
# Regex to check if Genus/species. - COMPLETE
# Add length requirement to first/second words - TO DO

# Higher taxonomy entries captured via list
# Things like phylum: plant, animal, microbes( go more depth like bacteria/fungi?)


if __name__ == "__main__":
    main()
