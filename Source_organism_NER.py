from taxonerd import TaxoNERD
import json
from pandas import DataFrame

SOURCE_ORGANISM_REGEX = "[A-Z]{1}[a-z]+ {1}[a-z]+\.? ?[A-Z0-9-]+ ?[A-Z]?[a-zA-Z0-9-]+|[A-Z]{1}[a-z]+ {1}[a-z]+\.?"
# https://regexr.com/60t8c

ner = TaxoNERD(model="en_ner_eco_biobert", prefer_gpu=False,
               with_abbrev=False)  # Add with_linking="gbif_backbone" or with_linking="taxref" to activate entity linking
def main():

    with open("npatlas_origin_articles_for_NER_training.json", "r") as file:
        data = json.load(file)

        for item in data:
            abstract = item["reference"]["abstract"]
            actual_chemical_names = item["names"]

            taxon_entities = []
            if abstract:
                taxon = ner.find_entities(abstract)
                entity = taxon.to_json(orient='records', lines=True)
                entities = entity.splitlines()

                # TODO: Duplicate entry removal
                # print(entities)
                entities_list = []
                for string_dic in entities:
                    try:
                        obj = json.loads(string_dic)
                        entities_list.append(obj)
                    except:
                        continue
                print(entities_list)

            # 1. Make unique list; deduplicate - IN PROGRESS
            # Check if entry in list; remove substrings

        # 2. Regex to check if Genus/species. - COMPLETE
        # Add length requirement to first/second words - TO DO

        # Higher taxonomy entries captured via list
        # Things like phylum: plant, animal, microbes( go more depth like bacteria/fungi?)

if __name__  == "__main__":
    main()