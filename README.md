# NPA Named-Entity-Recognition Scripts

Goal: The goal of these scripts is to extract entities to determine Named-Entity relationships.

1. Chemical Compound NER : compound_name_extractor.py
    - Extraction of Chemical compound named entities. An updated version of NPAtlas script for extracting chemical 
entities, where regex matches ranges of compounds (Exampleamide A-C) or if it's before a number (1).


2. Class of Compound NER: class_of_compound_NER.py
    - Extraction of class of chemical compound entities. Uses large list of potential classes of natural products and 
regex to match and identify classes.


3. Source Organism NER: Source_organism_NER.py
    - Extraction of source organism entities. Makes use of TaxoNERD to match genera and species, regex pattern for 
genera and species filters out improper matches.


# Misc. Scripts used in tasks related to NER
- Generation of Higher taxonomy lists of genera: higher_taxonomy_lists.py
    - Generation of lists of genera for higher taxonomy to distinguish plant, animal and microbe. Mostly from ITIS,
    but some from NPAtlas
    
- Unit Testing: unit_test.py
    - Unit tests for testing and development of NPA Named entity recognition 
  
- Functions used in Chemical compound NER that are basic in nature and placed here for organization: miscellaneous_functions.py
    - Scripts used in Chemical entity extraction to: sort lists by string length, check if brackets are matched and
  remove improper parentheses




