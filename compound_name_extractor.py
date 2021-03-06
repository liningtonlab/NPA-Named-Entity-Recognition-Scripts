"""
Script to find compound names from abstract text and derive list of compounds
ISSUES
* Leading "-"
* Missing base names
"""
import re
import json
import csv

# regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
NAME_BASE = "(\'|′|\"|,|\+|\(|\)|\d|-|α|β|γ|δ|[A-Z]|[a-z]){4,200}"

# regex for the characters that separate ranges (e.g. A - H)
SEPARATORS = "[-~–−]"

# regex for the terminus if the search. helps to find compounds with suffixes that are at the end of sentances or next to punctuation
TERMINATORS = "[\s.,:;$\)]|$"

# regex to describe compound suffixes (e.g. compoundine B12)
SUFFIX_TYPE_LIST = ["[A-Z]\d{0,2}", "[IVX]{1,5}"]

# list of allowed termini for compound names that are more than one word (e.g. allegic acid C)
TWO_WORD_NAME_TERMINI = ['acid', 'ester', 'acetate', 'butyrate', 'anhydride',
                         'dimer', 'methyl', 'ethyl', 'aglycon', 'aglycone', 'peroxide']

# list of excluded names
# WHEREA = WHEREAS after s is stripped
EXCLUDED_NAMES = ["COMPOUND", "ALKALOID", "TERPENE", "POLYKETIDE", "MOIETY", "DEGREE", "STRUCTURE", "ANALOGUE",
                  "DERIVATIVE", "METABOLITE", "COENZYME", "TOPOISOMERASE", "COMPLEX", "DERIVATIVE", "REPORTED",
                  "AGAINST", "ALBICANS", "AERUGINOSA", "AUREUS", "COLI", "COMPONENT", "SYNTHASE", "COMPLEX",
                  "FACTOR", "WHEREA", "STIMULATION", "SYSTEM", "CYANOBACTERIA", "CANDIDUS", "ANALOG",
                  "FRACTION", "HEPATITIS", "HEPATITI", "EIGHTEEN", "CONGENER", "INHIBIT", "METHYL ESTER"]
# put diseases here
COMPOUND_CLASS = ['ABEOLUPANE TRITERPENOID', 'ABEOTAXANE DITERPENOID', 'ABIETANE DITERPENOID', 'ACETOGENIN',
                  'ACRIDONE ALKALOID', 'ACYCLIC MONOTERPENOID', 'ACYCLIC TRITERPENOID', 'ACYL PHLOROGLUCINOL',
                  'AGAROFURAN SESQUITERPENOID', 'ALKALOID', 'AMARYLIDACEAE ALKALOID', 'AMIDE ALKALOID',
                  'AMINO ACID GLYCOSIDE', 'AMINO ACID', 'AMINO CYCLITOL', 'AMINO FATTY ACID', 'AMINOGLYCOSIDE',
                  'AMINOSUGAR', 'ANDROSTANE STEROID', 'ANGUCYCLINE', 'ANTHOCYANIDIN', 'ANTHRACYCLINE',
                  'ANTHRANILIC ACID ALKALOID', 'ANTHRANILLIC ACID DERIVATIVE', 'ANTHRAQUINONE', 'ANTHRONE',
                  'APOCAROTENOID', 'APORPHINE ALKALOID', 'APOTIRUCALLANE TRITERPENOID', 'ARBORINANE TRITERPENOID',
                  'AROMATIC POLYKETIDE', 'ARYLBENZOFURAN', 'ARYLNAPHTHALENE LIGNANS', 'ARYLTETRALIN LIGNAN',
                  'ATISANE DITERPENOID', 'AZAPHILONE', 'BACCHARANE TRITERPENOID', 'BACTOPRENOL',
                  'BAUERANE TRITERPENOID', 'BENZOFURAN', 'BENZOPHENONE', 'BENZOQUINONE',
                  'BERGAMOTANE SESQUITERPENOID', 'BEYERANE DITERPENOID', 'BIARYL TYPE DIARYLHEPTANOID',
                  'BISABOLANE SESQUITERPENOID', 'BISNAPHTHALENE', 'BRANCHED FATTY ACID',
                  'BRASILANE SESQUITERPENOID', 'BREVIANE DITERPENOID', 'BUFADIENOLIDE', 'CADINANE SESQUITERPENOID',
                  'CAMPHANE MONOTERPENOID', 'CANNABINOID', 'CAPSAICINOID', 'CAPSAICIN', 'CARABRANE SESQUITERPENOID',
                  'CARBAZOLE ALKALOID', 'CARBOCYCLIC FATTY ACID', 'CARBOHYDRATE', 'CARBOLINE ALKALOID', 'CARDENOLIDE',
                  'CAROTENOID', 'CATECHOLAMINE', 'CATECHOL', 'CEMBRANE DITERPENOID', 'CERAMIDE', 'CHALCONE',
                  'CHEILANTHANE SESTERTERPENOID', 'CHOLANE STEROID', 'CHOLESTANE STEROID', 'CHROMANE', 'CHROMONE',
                  'CINNAMIC ACID AMIDE', 'CINNAMOYL PHENOL', 'CLERODANE DITERPENOID', 'COLENSANE DITERPENOID',
                  'COPACAMPHANE SESQUITERPENOID', 'COUMARINOLIGNAN', 'COUMARIN', 'COUMARONOCHROMONE', 'COUMESTAN',
                  'CUBEBANE SESQUITERPENOID', 'CUCURBITANE TRITERPENOID', 'CYANOGENIC GLYCOSIDE', 'CYCLIC PEPTIDE',
                  'CYCLIC POLYKETIDE', 'CYCLITOL', 'CYCLOARTANE TRITERPENOID', 'CYCLOEUDESMANE SESQUITERPENOID',
                  'CYCLOPHYTANE DITERPENOID', 'CYTOCHALASAN ALKALOID', 'DAUCANE SESQUITERPENOID', 'DEPSIDE',
                  'DEPSIDONE', 'DEPSIPEPTIDE', 'DIACYLGLYCEROL', 'DIARYLHEPTANOID', 'DIAZOTETRONIC ACID',
                  'DIBENZOCYCLOOCTADIENES LIGNAN', 'DIBENZYLBUTANE LIGNAN', 'DIBENZYLBUTYROLACTONE LIGNAN',
                  'DICARBOXYLIC ACID', 'DIHYDROFLAVONOL', 'DIHYDROISOCOUMARIN', 'DIMERIC PHLOROGLUCINOL', 'DIPEPTIDE',
                  'DEPSIPEPTIDES', 'DIPHENYL ETHER',
                  'DISACCHARIDE', 'DITERPENE', 'DITERPENOID', 'DOCOSANOID', 'DRIMANE SESQUITERPENOID', 'ECDYSTEROID',
                  'EICOSANOID', 'ELEMANE SESQUITERPENOID', 'ENDOCANNABINOID', 'EREMOPHILANE SESQUITERPENOID',
                  'ERGOSTANE STEROID', 'ERICAMYCIN', 'ERYTHROMYCIN', 'EUDESMANE SESQUITERPENOID',
                  'EUPHANE TRITERPENOID', 'FARNESANE SESQUITERPENOID', 'FATTY ACID CONJUGATE', 'FATTY ACID',
                  'FATTY ACYL GLYCOSIDE', 'FATTY ACYL', 'FATTY ALCOHOL', 'FATTY ALDEHYDE', 'FATTY AMIDE',
                  'FATTY ESTER', 'FATTY NITRILE', 'FERNANE TRITERPENOID', 'FLAVAN-3-OL', 'FLAVANDIOL',
                  'LEUCOANTHOCYANIDIN', 'FLAVANONE', 'FLAVAN', 'FLAVONE', 'FLAVONOID', 'FLAVONOLIGNAN',
                  'FLAVONOL', 'FRIEDELANE TRITERPENOID', 'FURANOID LIGNAN', 'FUROCOUMARIN', 'FUROFURANOID LIGNAN',
                  'FUROSTANE STEROID', 'FUSIDANE TRITERPENOID', 'GALLOTANNIN', 'GAMMACERANE TRITERPENOID',
                  'GERANYLATED PHLOROGLUCINOL', 'GERMACRANE SESQUITERPENOID', 'GLUCOSINOLATE', 'GLUTINANE TRITERPENOID',
                  'GLYCEROLIPID', 'GLYCEROPHOSPHATE', 'GLYCEROPHOSPHOLIPID', 'GLYCOSIDES OF MONO- AND DISACCHARIDE',
                  'GLYCOSYLMONOACYLGLYCEROL', 'GUAIANE SESQUITERPENOID', 'HALIMANE DITERPENOID',
                  'HALOGENATED HYDROCARBON', 'HASUBANAN ALKALOID', 'HETEROCYCLIC FATTY ACID', 'HISTIDINE ALKALOID',
                  'HOPANE TRITERPENOID', 'HYDROXY FATTY ACID', 'HYDROXY-HYDROPEROXYEICOSATETRAENOIC ACID',
                  'HYDROXY-HYDROPEROXYEICOSATRIENOIC ACID', 'ICETEXANE DITERPENOID', 'ILLUDALANE SESQUITERPENOID',
                  'ILLUDANE SESQUITERPENOID', 'IMIDAZOLE ALKALOID', 'INDOLE ALKALOID',
                  'INDOLE DIKETOPIPERAZINE ALKALOID', 'INDOLE-DITERPENOID ALKALOID', 'IRIDOID MONOTERPENOID',
                  'ISOCOUMARIN', 'ISOFLAVANONE', 'ISOFLAVONE', 'ISOFLAVONOID', 'ISOINDOLE ALKALOID',
                  'ISOPIMARANE DITERPENOID', 'ISOPROSTANE', 'ISOQUINOLINE ALKALOID', 'IVAXILLARANE SESQUITERPENOID',
                  'JASMONIC ACID', 'KAURANE DITERPENOID', 'KAVALACTONE', 'LABDANE DITERPENOID', 'LACTONE', 'LANOSTANE',
                  'LEUKOTRIENE', 'LIGNAN', 'LIMONOID', 'LIPOPEPTIDE', 'LIPOXIN', 'LONGIBORNANE SESQUITERPENOID',
                  'LUPANE TRITERPENOID', 'LYSINE ALKALOID', 'MACROLIDE LACTONE', 'MACROLIDE', 'MARESIN', 'MEGASTIGMANE',
                  'MENTHANE MONOTERPENOID', 'MEROHEMITERPENOID', 'MEROSESQUITERPENOID', 'MEROTERPENE', 'MEROTERPENOID',
                  'METHYL XANTHONE', 'MICROGININ', 'MINOR LIGNAN', 'MISCELLANEOUS POLYKETIDE', 'MONOACYLGLYCEROL',
                  'MONOCYCLIC MONOTERPENOID', 'MONOMERIC STILBENE', 'MONOSACCHARIDE', 'MONOTERPENE', 'MONOTERPENOID',
                  'MORETANE TRITERPENOID', 'MULTIFLORANE TRITERPENOID', 'MYRSINANE DITERPENOID', 'N-ACYL AMINE',
                  'N-ACYL ETHANOLAMINE', 'NAPHTHALENE', 'NAPHTHALENONE', 'NAPHTHOQUINONE', 'NEOFLAVONOID', 'NEOLIGNAN',
                  'NEUTRAL GLYCOSPHINGOLIPID', 'NICOTINIC ACID ALKALOID', 'NITRO FATTY ACID', 'NORKAURANE DITERPENOID',
                  'NORLABDANE DITERPENOID', 'NUCLEOSIDE', 'OCTADECANOID', 'OLEANANE TRITERPENOID', 'OLIGOMERIC STIBENE',
                  'OLIGOPEPTIDE', 'ONOCERANE TRITERPENOID', 'OPEN-CHAIN POLYKETIDE', 'ORNITHINE ALKALOID',
                  'OTHER DOCOSANOID', 'OTHER OCTADECANOID', 'OXO FATTY ACID', 'OXYGENATED HYDROCARBON',
                  'PATCHOULANE SESQUITERPENOID', 'PEPTIDE ALKALOID', 'PERFORANE SESQUITERPENOID', 'PHENANTHRENE',
                  'PHENANTHRENOID', 'PHENOLIC ACID', 'PHENYLALANINE-DERIVED ALKALOID', 'PHENYLETHANOID',
                  'PHENYLETHYLAMINE', 'PHENYLPROPANOID', 'PHLOROGLUCINOL', 'PHTHALIDE', 'PHYLLOCLADANE DITERPENOID',
                  'PHYTANE DITERPENOID', 'PICROTOXANE SESQUITERPENOID', 'PIMARANE DITERPENOID', 'PINANE MONOTERPENOID',
                  'PINGUISANE SESQUITERPENOID', 'PIPERIDINE ALKALOID', 'PODOCARPANE DITERPENOID', 'POLYAMINE',
                  'POLYCYCLIC AROMATIC POLYKETIDE', 'POLYENE MACROLIDE', 'POLYKETIDE', 'POLYOL', 'POLYPRENOL',
                  'POLYPRENYLATED CYCLIC POLYKETIDE', 'POLYSACCHARIDE', 'PREGNANE STEROID',
                  'PRENYL QUINONE MEROTERPENOID', 'PROANTHOCYANIN', 'PROSTAGLANDIN', 'PROTOBERBERINE ALKALOID',
                  'PROTOPINE ALKALOID', 'PSEUDOALKALOID', 'PSEUDOGUAIANE SESQUITERPENOID', 'PSEUDOPTERANE DITERPENOID',
                  'PTEROCARPAN', 'PULVINONE', 'PURINE ALKALOID', 'PYRANOCOUMARIN', 'PYRIDINE ALKALOID', 'PYRONE',
                  'PYRROLIDINE ALKALOID', 'QUASSINOID', 'QUINOLINE ALKALOID', 'QUINONE', 'ROTENOID', 'SACCHARIDE',
                  'SCALARANE SESTERTERPENOID', 'SECOABIETANE DITERPENOID', 'SECOIRIDOID MONOTERPENOID',
                  'SECOKAURANE DITERPENOID', 'SERRATANE TRITERPENOID', 'SESQUITERPENOID', 'SESTERTERPENOID',
                  'SHIKIMATE', 'SHIKIMIC ACIDS', 'SMALL PEPTIDE', 'SPHINGOID BASE', 'SPINGOLIPID',
                  'SPIROSTANE STEROID', 'SPONGIANE DITERPENOID', 'SPRIROMEROTERPENOID', 'STEROIDAL ALKALOID',
                  'STEROID', 'STIGMASTANE STEROID', 'STILBENOID', 'STILBENOLIGNAN', 'STYRYLPYRONE',
                  'TARAXASTANE TRITERPENOID', 'TARAXERANE TRITERPENOID', 'TAXANE DITERPENOID', 'TERPENE ALKALOID',
                  'TERPENE', 'TERPENOID ALKALOID', 'TERPENOID', 'TERPHENYL', 'TETRACYCLIC DITERPENOID',
                  'TETRAHYDROISOQUINOLINE ALKALOID', 'TETRAKETIDE MEROTERPENOID', 'TETRONATE', 'THIA FATTY ACID',
                  'TIRUCALLANE TRITERPENOID', 'TOTARANE DITERPENOID', 'TRACHYLOBANE DITERPENOID', 'TRIACYLGLYCEROL',
                  'TRIKETIDE MEROTERPENOID', 'TRIPEPTIDE', 'TRITERPENE', 'TRITERPENOID', 'TROPOLONE',
                  'TRYPTOPHAN ALKALOID', 'TYROSINE ALKALOID', 'UNSATURATED FATTY ACID', 'URSANE TRITERPENOID',
                  'USNIC ACID AND DERIVATIVE', 'VALERANE SESQUITERPENOID', 'WAX MONOESTER', 'XANTHONE', 'ZEARALENONE',
                  'ABEOABIETANE DITERPENOID', 'NAPHTHO-Γ-PYRONE', 'PHENYLSPIRODRIMANE', 'LIPOPEPTIDE', 'MACROLIDE',
                  'SORBICILLINOID', 'GLUCOSIDE', 'CHAMIGRANE', 'CYTOCHALASANE', 'ERGOSTANE', 'PEPTIDE',
                  'ALKYLRESORSINOL', 'FLUORENE', 'GUANIDINE ALKALOID', 'LINEAR POLYKETIDE', 'MITOMYCIN DERIVATIVE',
                  'MYCOSPORINE DERIVATIVE', 'POLYETHER', 'PROLINE ALKALOID', 'SERINE ALKALOID', 'TETRAMATE ALKALOID',
                  'Β-LACTAM', 'Γ-LACTAM-Β-LACTONE']
OPEN_BRACES = ["(", "[", "{", "<"]
CLOSE_BRACES = [")", "]", "}", ">"]


def bracket_matched(string):
    count = 0
    for i in string:
        if i in OPEN_BRACES:
            count += 1
        elif i in CLOSE_BRACES:
            count -= 1
        if count < 0:
            return False
    return count == 0


def name_search(text):
    def names_letter_range_add(compound_names, root_name, suffix_start, suffix_end):

        for c in range(ord(suffix_start), ord(suffix_end) + 1):
            name = root_name.capitalize() + " " + chr(c)
            if name not in compound_names:
                compound_names.append(name)

    def names_roman_numeral_range_add(compound_names, root_name, suffix_start, suffix_end):

        numeral_to_int = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
                          "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
                          "XIX": 19, "XX": 20}
        int_to_numeral = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
                          11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII",
                          19: "XIX", 20: "XX"}

        for c in range(numeral_to_int[suffix_start], numeral_to_int[suffix_end] + 1):
            name = root_name.capitalize() + " " + int_to_numeral[c]
            if name not in compound_names:
                compound_names.append(name)

    def name_add(compound_names, name):

        # Check name has sensible brackets
        if bracket_matched(name):
            # Check name isn't already in the list
            if name.lower() not in [n.lower() for n in compound_names]:
                compound_names.append(name)

    compound_names = []

    # look for compound names listed in groups (e.g. Examplamides A - C)
    a = re.findall(
        '((' + NAME_BASE + ')\s)?(' + NAME_BASE + ')[\s-]([A-Z])\s?' + SEPARATORS + '\s?([A-Z])(' + TERMINATORS + ')',
        text)
    if a:
        for entry in a:
            root_name = entry[3].rstrip('s')
            if root_name in TWO_WORD_NAME_TERMINI:
                root_name = entry[1].rstrip() + " " + root_name
            # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
            elif len(root_name) < 7:
                continue
            elif root_name in EXCLUDED_NAMES:
                continue
            else:
                suffix_start = entry[5]
                suffix_end = entry[6]
                names_letter_range_add(compound_names, root_name, suffix_start, suffix_end)

    # look for compounds where suffixes are listed explicitly (e.g. Examplamides A, B and C)
    # this search accounts for situations where compound numbers are also included (e.g. Examplamides A (1), B (2) and C (3))
    # it also handles both single letters, letters followed by one or two digits, and Roman numerals.
    for suffix_type in SUFFIX_TYPE_LIST:
        b = re.findall(
            '((' + NAME_BASE + ')\s)?(' + NAME_BASE + ')[\s|-](' + suffix_type + ')(\s\(\d{1,2}\))?(([,][\s]' + suffix_type +
            '(\s\(\d{1,2}\))?){0,20}),?\s(and)\s(' + suffix_type + ')', text)
        if b:
            for entry in b:
                root_name = entry[3].rstrip('s')
                if root_name in TWO_WORD_NAME_TERMINI:
                    # print(root_name)
                    root_name = entry[1].rstrip().rstrip('s') + " " + root_name
                # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
                if len(root_name) < 7:
                    continue
                elif root_name.upper() in EXCLUDED_NAMES:
                    continue
                else:
                    suffix_list = (entry[7]).split(", ")[1:]
                    suffix_list.append(entry[5])
                    suffix_list.append(entry[11])
                    for suffix in suffix_list:
                        # This is required to remove the bracketed numbers if these are
                        # in the original text (e.g. Wawawa A (1), B (2), C (3) and D (4))
                        if re.search("[\(]", suffix):
                            suffix = suffix.split("(")[0].rstrip()
                        name = root_name.capitalize() + " " + suffix
                        name_add(compound_names, name)

    # methyl ester finder
    # Capture two blocks of text that doesn't include whitespace characters (a word) prior to "methyl ester" or ether
    # 1. Like Helvolic acid methyl ester (1) or Ochratoxin A methyl ester (2)
    ce = re.findall('(\S+)\s(acid|[A-Z])\s(dimethyl ester|methyl ester|methyl ether)\s+(\(\d\))', text)
    if ce:
        for entry in ce:
            comp_name = '{0} {1} {2}'.format(entry[0].rstrip().capitalize(), entry[1].rstrip(), entry[2].rstrip())
            name_add(compound_names, comp_name)

    # 2. Or 3 words Like 6′,6‴-cryptoporic acid G dimethyl ester (1)
    ce_double = re.findall('(\S+)\s(acid|[A-Z])\s(acid|[A-Z])\s(dimethyl ester|methyl ester|methyl ether)\s+(\(\d\))',
                           text)
    if ce_double:
        for entry in ce_double:
            comp_name = '{0} {1} {2} {3}'.format(entry[0].rstrip().capitalize(), entry[1].rstrip(), entry[2].rstrip(),
                                                 entry[3].rstrip())
            name_add(compound_names, comp_name)

    # 3. Or just 1 word like Secoxyloganin methyl ester (1)
    ce_single = re.findall('(\S+[^A-Z])\s(dimethyl ester|methyl ester|methyl ether)\s+(\(\d\))',
                           text)
    if ce_single:
        for entry in ce_single:
            comp_name = '{0} {1}'.format(entry[0].rstrip().capitalize(), entry[1].rstrip())
            name_add(compound_names, comp_name)

    # Captures a word prior to "methyl ester" or ether and any text that doesn't include whitespace characters with it
    # Like alternariol 1'-hydroxy-9-methyl ether (1)
    se = re.findall('(\S+[^A-Z])\s(\S+)(dimethyl ester|methyl ester|methyl ether)\s+(\(\d\))', text)
    if se:
        for entry in se:
            comp_name = '{0} {1}{2}'.format(entry[0].rstrip().capitalize(), entry[1].rstrip(), entry[2].rstrip())
            name_add(compound_names, comp_name)

    # look for compounds that are followed by a compound number (e.g. (1)) or range of numbers (e.g. (1 - 3))
    for suffix_type in SUFFIX_TYPE_LIST:
        c = re.findall(
            '(' + NAME_BASE + '\s)?(' + NAME_BASE + ')\s((' + suffix_type + ')\s)?(\(\d{1,2}(\s?' + SEPARATORS + '\s?\d{1,2})?\))',
            text)
        if c:
            for entry in c:
                if entry[2] in TWO_WORD_NAME_TERMINI:
                    root_name = entry[0].rstrip().rstrip('s').capitalize() + " " + entry[2].rstrip().rstrip('s')
                # this requirement removes short 'words' like (1)H, and (4), that otherwise get selected as hits.
                elif len(entry[2]) < 8 and re.search("[\'′\",+\(\)]", entry[2]):
                    continue
                else:
                    root_name = entry[2].rstrip().rstrip('s').capitalize()
                if root_name.upper() in EXCLUDED_NAMES:
                    continue
                if len(root_name) < 7:
                    continue
                if entry[5]:
                    name = root_name + " " + entry[5]
                else:
                    name = root_name
                name_add(compound_names, name)

    # look for compounds that have Roman numeral suffixes listed in groups (e.g. Examplamides III - IX)
    d = re.findall(
        '(' + NAME_BASE + '\s)?(' + NAME_BASE + ')[\s-]([IVX]{1,5})\s?' + SEPARATORS + '\s?([IVX]{1,5})(' + TERMINATORS + ')',
        text)
    if d:
        for entry in d:
            root_name = entry[2].rstrip('s')
            if root_name in TWO_WORD_NAME_TERMINI:
                root_name = entry[0].rstrip() + " " + root_name
            # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
            if len(root_name) < 7:
                continue
            elif root_name.upper() in EXCLUDED_NAMES:
                continue
            else:
                suffix_start = entry[4]
                suffix_end = entry[5]
                names_roman_numeral_range_add(compound_names, root_name, suffix_start, suffix_end)

    # look for instances of single compounds (single letters, letters followed by one or two digits, and Roman numerals)

    for suffix_type in SUFFIX_TYPE_LIST:
        e = re.findall('(' + NAME_BASE + '\s)?(' + NAME_BASE + ')\s(' + suffix_type + ')(' + TERMINATORS + ')', text)

        if e:
            for entry in e:
                if entry[2] in TWO_WORD_NAME_TERMINI:
                    name = entry[0].rstrip().rstrip('s').capitalize() + " " + entry[2] + " " + entry[4]
                # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
                elif len(entry[2]) < 7:
                    continue
                elif entry[2].rstrip().rstrip('s').upper() in EXCLUDED_NAMES:
                    continue
                else:
                    name = entry[2].rstrip().rstrip('s').capitalize() + " " + entry[4]

                name_add(compound_names, name)

                # Add just the word closest to the bracket (e.g. lodophilone from "alkaloid lodophilone (1)"
                # Only do this if the second word is longer than 5 characters and isn't both short and containing special characters
                if len(entry[1]) > 4 and not (len(entry[1]) < 8 and re.search("[\'′\",+\(\)]", entry[1])):
                    if entry[1].rstrip().rstrip('s').upper() in EXCLUDED_NAMES:
                        continue
                    else:
                        name = entry[1].rstrip().rstrip('s').capitalize() + " " + entry[2]
                        name_add(compound_names, name)

    return sorted(compound_names)


def clean_detected_items(abstract_text):
    """ Cleans out Compound classes from the chemical compound entities
            :param abstract_text: raw string of abstract text
            :return: list of names of cleaned detected chemical compounds
            """
    detected_chemical_names = name_search(abstract_text)
    clean_detected_names = []
    for x in detected_chemical_names:
        upper_item = x.upper()
        if upper_item in COMPOUND_CLASS:
            continue
        else:
            clean_detected_names.append(x)
    return clean_detected_names


def article_compound_number(abstract_text):
    """ Detect the number of compound in the article
        :param abstract_text: raw string of abstract text
        :return: number of detected chemical compounds and list of names of detected chemical compounds
        """
    detected_chemical_names = name_search(abstract_text)
    clean_detected_chem_names = clean_detected_items(detected_chemical_names)
    list_length = len(clean_detected_chem_names)
    return clean_detected_chem_names, list_length


# Python3 program to remove invalid parenthesis; https://www.geeksforgeeks.org/remove-invalid-parentheses/
def is_parentheses(c):
    """ Method checks if character is parenthesis(open or closed)
            :param c: character
            :return: if it is open/closed parentheses
            """
    return (c == '(') or (c == ')')


def is_valid_string(string):
    """ Method returns true if contains valid parentheses
                :param string: string
                :return: False if open bracket otherwise 0 when valid parentheses
                """
    cnt = 0
    for i in range(len(string)):
        if string[i] == '(':
            cnt += 1
        elif string[i] == ')':
            cnt -= 1
        if cnt < 0:
            return False
    return cnt == 0


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

        if is_valid_string(string):
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


def improper_parentheses_capture(chem_list):
    """ Method to remove invalid parentheses, putting above 3 function together
                        :param chem_list: list of chemicals(strings)
                        :return: False if open bracket otherwise 0 when valid parentheses
                        """
    chemical_detection_list_no_invalid_parentheses = []
    for chemical in chem_list:
        if bracket_matched(chemical) is False:
            no_invalid_parentheses = remove_invalid_parentheses(chemical)
            chemical_detection_list_no_invalid_parentheses.append(
                no_invalid_parentheses[:1].upper() + no_invalid_parentheses[1:])
        else:
            chemical_detection_list_no_invalid_parentheses.append(chemical)
    unique_chemical_detection_list = list(set(chemical_detection_list_no_invalid_parentheses))
    return unique_chemical_detection_list


def main():
    """
    # add list of new classes to put into COMPOUND_CLASS
    classes_list = ['Peptides','Carbohydrates','Fatty acids','Polyketides','Phenylpropanoids','Shikimates','Terpenoids','Alkylresorsinols','Amino acid glycosides','Aminosugars and aminoglycosides','Anthranilic acid alkaloids','Apocarotenoids','Carotenoids (C40)','Carotenoids (C45)','Carotenoids (C50)','Chromanes','Coumarins','Cyclic polyketides','Diarylheptanoids','Diazotetronic acids','Diphenyl ethers','Diterpenoids','Docosanoids','Eicosanoids','Fatty acyl glycosides','Fatty acyls','Fatty amides','Fatty esters','Flavonoids','Fluorenes','Glycerolipids','Glycerophospholipids','Guanidine alkaloids','Histidine alkaloids','Isoflavonoids','Lignans','Linear polyketides','Lysine alkaloids','Macrolides','Meroterpenoids','Mitomycin derivatives','Monoterpenoids','Mycosporine derivatives','Naphthalenes','Nicotinic acid alkaloids','Nucleosides','Octadecanoids','Oligopeptides','Ornithine alkaloids','Peptide alkaloids','Phenanthrenoids','Phenolic acids','Phenylethanoids','Phenylpropanoids','Phloroglucinols','Polycyclic aromatic polyketides','Polyethers','Polyols','Polyprenols','Proline alkaloids','Pseudoalkaloids','Saccharides','Serine alkaloids','Sesquiterpenoids','Sesterterpenoids','Small peptides','Spingolipids','Steroids','Stilbenoids','Styrylpyrones','Terphenyls','Tetramate alkaloids','Triterpenoids','Tropolones','Tryptophan alkaloids','Tyrosine alkaloids','Xanthones','β-lactams','γ-lactam-β-lactones']
    counter=0
    for item in classes_list:
        new_item = item[:-1].upper()
        if new_item not in COMPOUND_CLASS:
            counter += 1
            COMPOUND_CLASS.append(item[:-1].upper())
    print(COMPOUND_CLASS)
    print(counter)
    """

    with open("npatlas_origin_articles_for_Pegah.json", "r") as file:
        data = json.load(file)
        with open("outputs.csv", "w", encoding="utf-8") as filer:
            headers = ['doi', 'abstract', 'detected_compounds', 'detection_number',
                       'actual_compound', 'actual_compnum']
            writer = csv.DictWriter(filer, fieldnames=headers)
            writer.writeheader()
            for item in data:
                abstract = item["reference"]["abstract"]
                doi = item["reference"]["doi"]
                actual_chemical_names = item["names"]
                if abstract and type(abstract) == str:
                    chemical_detection_list = clean_detected_items(abstract)
                    chemical_detection_list_no_open_parentheses = improper_parentheses_capture(chemical_detection_list)
                    length_chems = len(chemical_detection_list_no_open_parentheses)

                    abs_dict = {"doi": doi, "abstract": abstract, "actual_compound": actual_chemical_names,
                                "actual_compnum": len(actual_chemical_names),
                                "detected_compounds": chemical_detection_list_no_open_parentheses,
                                "detection_number": length_chems}
                    writer.writerow(abs_dict)
                    #json.dump(abs_dict, filer, indent=2)
                else:
                    continue
            #actual_chemical_names = item["names"]

            '''
            if abstract:
                chemical_detection_list = clean_detected_items(abstract)
                chemical_detection_list_no_open_parentheses = improper_parentheses_capture(chemical_detection_list)
                length_chems = len(improper_parentheses_capture(chemical_detection_list_no_open_parentheses))
                print(improper_parentheses_capture(chemical_detection_list_no_open_parentheses))
            else:
                print("none")'''

# TODO:
# 1. Class name removal -  Complete
# 2. Methyl ester finder(or other derivative type) - Complete
#       search for comp name with methyl ester, replace with combo
#       is comp and derivative contained in abstract too?
# 3. Strip hanging brackets function - IN PROGRESS
#       does name begin/ending bracket?
#       strip leading bracket if brackets don't match or trailing
# 4. Get entity location in abstract text


if __name__ == "__main__":
    main()
