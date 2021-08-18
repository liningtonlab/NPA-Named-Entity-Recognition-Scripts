"""
Script to find compound names from abstract text and derive list of compounds
ISSUES
* Leading "-"
* Missing base names
"""
import re
import json
import miscellaneous_functions

# Regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
NAME_BASE = "(\'|′|\"|,|\+|\(|\)|\[|\]|\d|-|α|β|γ|δ|[A-Z]|[a-z]){4,200}"

# Regex for the characters that separate ranges (e.g. A - H)
SEPARATORS = "[-~–−]"

# Regex for the terminus at the end of sentences or next to punctuation helps to find compounds with terminator suffixes
TERMINATORS = "[\s.,:;$\)]|$"

# Regex to describe compound suffixes (e.g. compoundine B12)
SUFFIX_TYPE_LIST = ["[A-Z]\d{0,2}", "[IVX]{1,5}"]

# List of allowed termini for compound names that are more than one word (e.g. allegic acid C)
TWO_WORD_NAME_TERMINI = ['acid', 'ester', 'acetate', 'butyrate', 'anhydride',
                         'dimer', 'methyl', 'ethyl', 'aglycon', 'aglycone', 'peroxide']

# Regex of possible variations on methyl ester
METHYL_ESTER_VARIATIONS = 'dimethyl ester|methyl ester|methyl ether'

# List of excluded names; Put diseases and other Excluded terms that are commonly matched in here:
EXCLUDED_NAMES = ["COMPOUND", "ALKALOID", "TERPENE", "POLYKETIDE", "MOIETY", "DEGREE", "STRUCTURE", "ANALOGUE",
                  "DERIVATIVE", "METABOLITE", "COENZYME", "TOPOISOMERASE", "COMPLEX", "DERIVATIVE", "REPORTED",
                  "AGAINST", "ALBICANS", "AERUGINOSA", "AUREUS", "COLI", "COMPONENT", "SYNTHASE", "COMPLEX",
                  "FACTOR", "WHEREA", "STIMULATION", "SYSTEM", "CYANOBACTERIA", "CANDIDUS", "ANALOG", "FRACTION",
                  "HEPATITIS", "HEPATITI", "EIGHTEEN", "CONGENER", "INHIBIT", "METHYL ESTER", "BENZOIC ACID",
                  'CONSTITUENT', 'INCLUDING', 'PRODUCT', 'DIFFRACTION']

# List of natural product compound classes
COMPOUND_CLASS = ['ABEOLUPANE TRITERPENOID', 'ABEOTAXANE DITERPENOID', 'ABIETANE DITERPENOID', 'ACETOGENIN',
                  'ACRIDONE ALKALOID', 'ACYCLIC MONOTERPENOID', 'ACYCLIC TRITERPENOID', 'ACYL PHLOROGLUCINOL',
                  'AGAROFURAN SESQUITERPENOID', 'ALKALOID', 'AMARYLIDACEAE ALKALOID', 'AMIDE ALKALOID',
                  'AMINO ACID GLYCOSIDE', 'AMINO ACID', 'AMINO CYCLITOL', 'AMINO FATTY ACID', 'AMINOGLYCOSIDE',
                  'AMINOSUGAR', 'ANDROSTANE STEROID', 'ANGUCYCLINE', 'ANTHOCYANIDIN', 'ANTHRACYCLINE',
                  'ANTHRANILIC ACID ALKALOID', 'ANTHRANILLIC ACID DERIVATIVE', 'ANTHRAQUINONE', 'ANTHRONE',
                  'APOCAROTENOID', 'APORPHINE ALKALOID', 'APOTIRUCALLANE TRITERPENOID', 'ARBORINANE TRITERPENOID',
                  'AROMATIC POLYKETIDE', 'ARYLBENZOFURAN', 'ARYLNAPHTHALENE LIGNANS', 'ARYLTETRALIN LIGNAN',
                  'ATISANE DITERPENOID', 'AZAPHILONE', 'BACCHARANE TRITERPENOID', 'BACTOPRENOL',
                  'BAUERANE TRITERPENOID', 'BENZOFURAN', 'BENZENOID', 'BENZOPHENONE', 'BENZOPYRANONE', 'BENZOQUINONE',
                  'BERGAMOTANE SESQUITERPENOID', 'BEYERANE DITERPENOID', 'BIARYL TYPE DIARYLHEPTANOID',
                  'BISABOLANE SESQUITERPENOID', 'BISNAPHTHALENE', 'BRANCHED FATTY ACID',
                  'BRASILANE SESQUITERPENOID', 'BREVIANE DITERPENOID', 'BUFADIENOLIDE', 'BUTENOLIDE', 'BUTYROLACTONE',
                  'CADINANE SESQUITERPENOID', 'CAMPHANE MONOTERPENOID', 'CANNABINOID', 'CAPSAICINOID', 'CAPSAICIN',
                  'CARABRANE SESQUITERPENOID',
                  'CARBAZOLE ALKALOID', 'CARBOCYCLIC FATTY ACID', 'CARBOHYDRATE', 'CARBOLINE ALKALOID', 'CARDENOLIDE',
                  'CAROTENOID', 'CATECHOLAMINE', 'CATECHOL', 'CEMBRANE DITERPENOID', 'CEREBROSIDE', 'CERAMIDE',
                  'CHALCONE', 'CHEILANTHANE SESTERTERPENOID', 'CHOLANE STEROID', 'CHOLESTANE STEROID', 'CHROMANE',
                  'CHROMONE',
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
                  'GLYCEROLIPID', 'GLYCEROPHOSPHATE', 'GLYCEROPHOSPHOLIPID', 'GLYCOSIDES',
                  'GLYCOSYLMONOACYLGLYCEROL', 'GUAIANE SESQUITERPENOID', 'HALIMANE DITERPENOID',
                  'HALOGENATED HYDROCARBON', 'HASUBANAN ALKALOID', 'HETEROCYCLIC FATTY ACID', 'HISTIDINE ALKALOID',
                  'HOPANE TRITERPENOID', 'HYDROXY FATTY ACID', 'HYDROXY-HYDROPEROXYEICOSATETRAENOIC ACID',
                  'HYDROXY-HYDROPEROXYEICOSATRIENOIC ACID', 'ICETEXANE DITERPENOID', 'ILLUDALANE SESQUITERPENOID',
                  'ILLUDANE SESQUITERPENOID', 'IMIDAZOLE ALKALOID', 'INDOLE ALKALOID',
                  'INDOLE DIKETOPIPERAZINE ALKALOID', 'INDOLE-DITERPENOID ALKALOID', 'IRIDOID MONOTERPENOID',
                  'ISOBENZOFURANONE', 'ISOCHROMENONE', 'ISOCHROMAN',
                  'ISOCOUMARIN', 'ISOFLAVANONE', 'ISOFLAVONE', 'ISOFLAVONOID', 'ISOINDOLE ALKALOID',
                  'ISOPIMARANE DITERPENOID', 'ISOPROSTANE', 'ISOQUINOLINE ALKALOID', 'IVAXILLARANE SESQUITERPENOID',
                  'JASMONIC ACID', 'KAURANE DITERPENOID', 'KAVALACTONE', 'LABDANE DITERPENOID', 'LACTONE', 'LANOSTANE',
                  'LEUKOTRIENE', 'LIGNAN', 'LIMONOID', 'LIPOPEPTIDE', 'LIPOXIN', 'LONGIBORNANE SESQUITERPENOID',
                  'LUPANE TRITERPENOID', 'LYSINE ALKALOID', 'MACROLACTAMS', 'MACROLIDE LACTONE', 'MACROLIDE', 'MARESIN',
                  'MEGASTIGMANE',
                  'MENTHANE MONOTERPENOID', 'MEROHEMITERPENOID', 'MEROSESQUITERPENOID', 'MEROTERPENE', 'MEROTERPENOID',
                  'METHYL XANTHONE', 'MICROGININ', 'MINOR LIGNAN', 'MISCELLANEOUS POLYKETIDE', 'MONOACYLGLYCEROL',
                  'MONOCYCLIC MONOTERPENOID', 'MONOMERIC STILBENE', 'MONOSACCHARIDE', 'MONOTERPENE', 'MONOTERPENOID',
                  'MORETANE TRITERPENOID', 'MULTIFLORANE TRITERPENOID', 'MYRSINANE DITERPENOID', 'N-ACYL AMINE',
                  'N-ACYL ETHANOLAMINE', 'NAPHTHALENE', 'NAPHTHALENONE', 'NAPHTHOQUINONE', 'NEOFLAVONOID', 'NEOLIGNAN',
                  'NEUTRAL GLYCOSPHINGOLIPID', 'NICOTINIC ACID ALKALOID', 'NITRO FATTY ACID', 'NORKAURANE DITERPENOID',
                  'NORLABDANE DITERPENOID', 'NORTRITERPENOID', 'NUCLEOSIDE', 'OCTADECANOID', 'OLEANANE TRITERPENOID',
                  'OLIGOMERIC STIBENE',
                  'OLIGOPEPTIDE', 'ONOCERANE TRITERPENOID', 'OPEN-CHAIN POLYKETIDE', 'ORNITHINE ALKALOID',
                  'OTHER DOCOSANOID', 'OTHER OCTADECANOID', 'OXO FATTY ACID', 'OXYGENATED HYDROCARBON',
                  'PATCHOULANE SESQUITERPENOID', 'PERYLENEQUINONE', 'PEPTIDE ALKALOID', 'PERFORANE SESQUITERPENOID',
                  'PHENANTHRENE',
                  'PHENANTHRENOID', 'PHENOLIC ACID', 'PHENYLALANINE-DERIVED ALKALOID', 'PHENYLETHANOID',
                  'PHENYLETHYLAMINE', 'PHENYLPROPANOID', 'PHLOROGLUCINOL', 'PHTHALIDE', 'PHYLLOCLADANE DITERPENOID',
                  'PHYTANE DITERPENOID', 'PICROTOXANE SESQUITERPENOID', 'PIMARANE DITERPENOID', 'PINANE MONOTERPENOID',
                  'PINGUISANE SESQUITERPENOID', 'PIPERIDINE ALKALOID', 'PODOCARPANE DITERPENOID', 'POLYAMINE',
                  'POLYCYCLIC AROMATIC POLYKETIDE', 'POLYENE MACROLIDE', 'POLYKETIDE', 'POLYOL', 'POLYPRENOL',
                  'POLYPRENYLATED CYCLIC POLYKETIDE', 'POLYSACCHARIDE', 'PREGNANE STEROID',
                  'PRENYL QUINONE MEROTERPENOID', 'PROANTHOCYANIN', 'PROSTAGLANDIN', 'PROTOBERBERINE ALKALOID',
                  'PROTOPINE ALKALOID', 'PSEUDOALKALOID', 'PSEUDOGUAIANE SESQUITERPENOID', 'PSEUDOPTERANE DITERPENOID',
                  'PTEROCARPAN', 'PULVINONE', 'PURINE ALKALOID', 'PYRANOCOUMARIN', 'PYRANONAPHTHOQUINONE',
                  'PYRIDINE ALKALOID', 'NAPHTHOPYRONE', 'PYRONE',
                  'PYRROLIDINE ALKALOID', 'QUASSINOID', 'QUINOLINE ALKALOID', 'QUINONE', 'ROTENOID', 'SACCHARIDE',
                  'SCALARANE SESTERTERPENOID', 'SECOABIETANE DITERPENOID', 'SECOIRIDOID MONOTERPENOID',
                  'SECOKAURANE DITERPENOID', 'SERRATANE TRITERPENOID', 'SESQUITERPENE', 'SESQUITERPENOID',
                  'SESTERTERPENOID',
                  'SHIKIMATE', 'SIDEROPHORE', 'SMALL PEPTIDE', 'SOLANAPYRONE', 'SPHINGOID BASE',
                  'SPHINGOLIPID',
                  'SPIROSTANE STEROID', 'SPONGIANE DITERPENOID', 'SPRIROMEROTERPENOID', 'STEROIDAL ALKALOID',
                  'STEROID', 'STIGMASTANE STEROID', 'STILBENOID', 'STILBENOLIGNAN', 'STYRYLPYRONE',
                  'TARAXASTANE TRITERPENOID', 'TARAXERANE TRITERPENOID', 'TAXANE DITERPENOID', 'TERPENE ALKALOID',
                  'TERPENE', 'TERPENOID ALKALOID', 'TERPENOID', 'TERPHENYL', 'TERREULACTONE', 'TETRACYCLIC DITERPENOID',
                  'TETRAHYDROISOQUINOLINE ALKALOID', 'TETRAKETIDE MEROTERPENOID', 'TETRONATE', 'THIA FATTY ACID',
                  'TIRUCALLANE TRITERPENOID', 'TOTARANE DITERPENOID', 'TRACHYLOBANE DITERPENOID', 'TRIACYLGLYCEROL',
                  'TRIKETIDE MEROTERPENOID', 'TRIPEPTIDE', 'TRITERPENE', 'TRITERPENOID', 'TROPOLONE',
                  'TRYPTOPHAN ALKALOID', 'TYROSINE ALKALOID', 'UNSATURATED FATTY ACID', 'URSANE TRITERPENOID',
                  'USNIC ACID AND DERIVATIVE', 'VALERANE SESQUITERPENOID', 'WAX MONOESTER', 'XANTHONE', 'ZEARALENONE',
                  'ABEOABIETANE DITERPENOID', 'NAPHTHO-Γ-PYRONE', 'PHENYLSPIRODRIMANE', 'LIPOPEPTIDE', 'MACROLIDE',
                  'SORBICILLINOID', 'GLUCOSIDE', 'CHAMIGRANE', 'CYTOCHALASANE', 'ERGOSTANE', 'PEPTIDE',
                  'ALKYLRESORSINOL', 'FLUORENE', 'GUANIDINE ALKALOID', 'LINEAR POLYKETIDE', 'MITOMYCIN DERIVATIVE',
                  'MYCOSPORINE DERIVATIVE', 'POLYETHER', 'PROLINE ALKALOID', 'SERINE ALKALOID', 'TETRAMATE ALKALOID',
                  'Β-LACTAM', 'Γ-LACTAM-Β-LACTONE', 'INDOLOCARBAZOLE', 'HYDROXYANTHRAQUINONE', 'HEPTAPEPTIDE',
                  'FURANONE', 'DIPHENYLETHER', 'DIKETOPIPERAZINE', 'DIHYDROXANTHONE', 'DIHYDROBENZOFURAN', 'XANTHENE',
                  'DIHYDROCHROMONE DIMER', 'YANUTHONE', 'MACROLACTAM', 'GIBBERELLINS', 'MYCOTOXIN', 'POLYKETIDE']


def name_search(text):
    def names_letter_range_add(compound_names_list, root_name_variable, suffix_start_point, suffix_end_point,
                               match_index, texts):
        """ Function for appending chemical compound names to list of compound names detected within the abstract text.
                :param compound_names_list: list of all compound names found in abstract text
                :param root_name_variable: root of the chemical name
                :param suffix_start_point: starting point location of suffix
                :param suffix_end_point: ending point location of suffix
                :param match_index: match index location
                :param texts: abstract text
                :return: none"""
        for char in range(ord(suffix_start_point), ord(suffix_end_point) + 1):
            chem_name = root_name_variable.capitalize() + " " + chr(char)
            if chem_name not in compound_names_list:
                compound_names_list.append((chem_name, match_index, texts))

    def names_roman_numeral_range_add(compound_names_list, root_name_variable, suffix_start_point, suffix_end_point,
                                      match_index, texts):
        """ Function for appending chemical compound names to list of compound names detected within the abstract text.
                :param compound_names_list: list of all compound names found in abstract text
                :param root_name_variable: root of the chemical name
                :param suffix_start_point: starting point location of suffix
                :param suffix_end_point: ending point location of suffix
                :param match_index: match index location
                :param texts: abstract text
                :return: none"""
        numeral_to_int = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
                          "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16, "XVII": 17, "XVIII": 18,
                          "XIX": 19, "XX": 20}
        int_to_numeral = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
                          11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII",
                          19: "XIX", 20: "XX"}

        for char in range(numeral_to_int[suffix_start_point], numeral_to_int[suffix_end_point] + 1):
            chem_name = root_name_variable.capitalize() + " " + int_to_numeral[char]
            if chem_name not in compound_names_list:
                compound_names_list.append((chem_name, match_index, texts))

    def name_add(compound_names_list, chem_name, match_index, texts):
        """ Function for appending a chemical compound name to the list of compound names detected within the abstract text.
                        :param compound_names_list: list of all compound names found in abstract text
                        :param chem_name: detected chemical compound name
                        :param match_index: match index location
                        :param texts: abstract text
                        :return: none"""
        # Check name has sensible brackets
        if miscellaneous_functions.bracket_matched(chem_name):
            # Check name isn't already in the list
            if chem_name.lower() not in [n[0].lower() for n in compound_names_list]:
                compound_names_list.append((chem_name, match_index, texts))

    def group_listed_comps(abstract_text, comp_name_list, base_names_list, separators_list, terminators_list,
                           two_word_termini_list, excluded_names_list):
        """ Look for compound names listed in groups (e.g. Examplamides A - C), appends compound names to the list
        of all compound names found in the abstract text
                :param abstract_text: raw string of abstract text
                :param comp_name_list: list of all compound names found in abstract text
                :param base_names_list: regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
                :param separators_list:  regex for the characters that separate ranges (e.g. A - H)
                :param terminators_list: regex for the terminus if the search. helps to find compounds with suffixes
                that are at the end of sentences or next to punctuation.
                :param two_word_termini_list: list of allowed termini for compound names that are more than one word
                (e.g. allegic acid C)
                :param excluded_names_list: list of excluded names
                :return: none
                """
        search_matches = re.finditer(
            '((' + base_names_list + ')\s)?(' + base_names_list + ')[\s-]([A-Z])\s?' + separators_list + '\s?([A-Z])(' + terminators_list + ')',
            abstract_text)
        if search_matches:
            for match in search_matches:
                findall_list = tuple(match.groups())
                for entry in findall_list:
                    root_name = findall_list[3].rstrip('s')
                    if root_name in two_word_termini_list:
                        root_name = findall_list[1].rstrip() + " " + root_name
                    # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
                    elif len(root_name) < 7:
                        continue
                    elif root_name in excluded_names_list:
                        continue
                    else:
                        suffix_start = findall_list[5]
                        suffix_end = findall_list[6]
                        names_letter_range_add(comp_name_list, root_name, suffix_start, suffix_end, match.span(),
                                               abstract_text)

    def explict_suffix_listed_comps(abstract_text, comp_name_list, name_base_list, suffix_type_list,
                                    two_word_termini_list, excluded_names_list):
        """ look for compounds where suffixes are listed explicitly (e.g. Examplamides A, B and C). This search
        accounts for situations where compound numbers are also included (e.g. Examplamides A (1), B (2) and C (3)).
        It also handles both single letters, letters followed by one or two digits, and Roman numerals.
                        :param abstract_text: raw string of abstract text
                        :param comp_name_list: list of all compound names found in abstract text
                        :param name_base_list: regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
                        :param suffix_type_list:  regex for the characters that separate ranges (e.g. A - H)
                        :param two_word_termini_list: list of allowed termini for compound names that are more
                        than one word (e.g. allegic acid C)
                        :param excluded_names_list: list of excluded names
                        :return: none
                        """
        for suffix_type in suffix_type_list:
            search_match = re.finditer(
                '((' + name_base_list + ')\s)?(' + name_base_list + ')[\s|-](' + suffix_type + ')(\s\(\d{1,2}\))?(([,][\s]' + suffix_type +
                '(\s\(\d{1,2}\))?){0,20}),?\s(and)\s(' + suffix_type + ')', abstract_text)
            if search_match:
                for match in search_match:
                    findall_list = tuple(match.groups())
                    for entry in findall_list:
                        root_name = findall_list[3].rstrip('s')
                        if root_name in two_word_termini_list:
                            # print(root_name)
                            root_name = findall_list[1].rstrip().rstrip('s') + " " + root_name
                        # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
                        if len(root_name) < 7:
                            continue
                        elif root_name.upper() in excluded_names_list:
                            continue
                        else:
                            suffix_list = (findall_list[7]).split(", ")[1:]
                            suffix_list.append(findall_list[5])
                            suffix_list.append(findall_list[11])
                            for suffix in suffix_list:
                                # This is required to remove the bracketed numbers if these are
                                # in the original text (e.g. Wawawa A (1), B (2), C (3) and D (4))
                                if re.search("[\(]", suffix):
                                    suffix = suffix.split("(")[0].rstrip()
                                name = root_name.capitalize() + " " + suffix
                                name_add(comp_name_list, name, match.span(), abstract_text)

    def methyl_ester_finder(abstract_text, comp_name_list, methyl_ester_finder_list):
        """For the detection of certain cases of methyl esters or similar types, such as dimethyl ether or methyl ester.
                                :param abstract_text: raw string of abstract text
                                :param comp_name_list: list of all compound names found in abstract text
                                :param methyl_ester_finder_list: regex pattern for different types of esters of ethers
                                :return: none
                                """
        # Capture two segments of text that doesn't include whitespace characters (a word) prior to "methyl ester"
        # 1. Ex. "Helvolic acid methyl ester (1)" or "Ochratoxin A methyl ester (2)"
        ce = re.finditer('(\S+)\s(acid|[A-Z])\s(' + methyl_ester_finder_list + ')\s+(\(\d\))', abstract_text)
        if ce:
            for match in ce:
                findall_list = tuple(match.groups())
                for entry in findall_list:
                    comp_name = '{0} {1} {2}'.format(findall_list[0].rstrip().capitalize(), findall_list[1].rstrip(),
                                                     findall_list[2].rstrip())
                    name_add(comp_name_list, comp_name, match.span(), abstract_text)

        # 2. Or 3 words: Ex. "6′,6-cryptoporic acid G dimethyl ester (1)"
        ce_double = re.finditer('(\S+)\s(acid|[A-Z])\s(acid|[A-Z])\s(' + methyl_ester_finder_list + ')\s+(\(\d\))',
                                abstract_text)
        if ce_double:
            for match in ce_double:
                findall_list = tuple(match.groups())  # Convert iterable object into
                for entry in findall_list:
                    comp_name = '{0} {1} {2} {3}'.format(findall_list[0].rstrip().capitalize(),
                                                         findall_list[1].rstrip(), findall_list[2].rstrip(),
                                                         findall_list[3].rstrip())
                    name_add(comp_name_list, comp_name, match.span(), abstract_text)

        # 3. Or just 1 word like Secoxyloganin methyl ester (1)
        ce_single = re.finditer('(\S+[^A-Z]^acid)\s(' + methyl_ester_finder_list + ')\s+(\(\d\))', abstract_text)
        if ce_single:
            for match in ce_single:
                findall_list = tuple(match.groups())
                for entry in findall_list:
                    comp_name = '{0} {1}'.format(findall_list[0].rstrip().capitalize(), findall_list[1].rstrip())
                    name_add(comp_name_list, comp_name, match.span(), abstract_text)

        # Benzoic acid finder
        ce_single2 = re.finditer('(\S+)\s(benzoic acid)\s+(\(\d\))', abstract_text)
        if ce_single2:
            for match in ce_single2:
                findall_list = tuple(match.groups())
                for entry in findall_list:
                    comp_name = '{0} {1}'.format(findall_list[0].rstrip().capitalize(), findall_list[1].rstrip())
                    name_add(comp_name_list, comp_name, match.span(), abstract_text)

        # Captures a word prior to "methyl ester" that could have any text that doesn't include whitespace characters with it
        # Like alternariol 1'-hydroxy-9-methyl ether (1)
        se = re.finditer('(\S+[^A-Z])\s(\S+)(' + methyl_ester_finder_list + ')\s+(\(\d\))', abstract_text)
        if se:
            for match in se:
                findall_list = tuple(match.groups())
                for entry in findall_list:
                    comp_name = '{0} {1}{2}'.format(findall_list[0].rstrip().capitalize(), findall_list[1].rstrip(),
                                                    findall_list[2].rstrip())
                    name_add(comp_name_list, comp_name, match.span(), abstract_text)

    def post_comps_numbers(abstract_text, comp_name_list, name_base_list, suffix_type_list, two_word_termini_list,
                           excluded_names_list, separators_list):
        """ Look for compounds that are followed by a compound number (e.g. (1)) or range of numbers (e.g. (1 - 3))
                        :param abstract_text: raw string of abstract text
                        :param comp_name_list: list of all compound names found in abstract text
                        :param name_base_list: regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
                        :param suffix_type_list:  regex for the characters that separate ranges (e.g. A - H)
                        :param two_word_termini_list: list of allowed termini for compound names that are more
                         than one word (e.g. allegic acid C)
                        :param excluded_names_list: list of excluded names
                        :param separators_list: regex for the characters that separate ranges (e.g. A - H)
                        :return: none
                        """
        for suffix_type in suffix_type_list:
            c = re.finditer(
                '(' + name_base_list + '\s)?(' + name_base_list + ')\s((' + suffix_type + ')\s)?(\(\d{1,2}(\s?' + separators_list + '\s?\d{1,2})?\))',
                abstract_text)
            if c:
                for match in c:
                    findall_list = tuple(match.groups())
                    for entry in findall_list:
                        if findall_list[2] in two_word_termini_list:
                            try:
                                root_name = findall_list[0].rstrip().rstrip('s').capitalize() + " " + findall_list[
                                    2].rstrip().rstrip('s')
                            except AttributeError as error:
                                print(error)
                        # this requirement removes short 'words' like (1)H, and (4), that otherwise get selected as hits.
                        elif len(findall_list[2]) < 8 and re.search("[\'′\",+\(\)]", findall_list[2]):
                            continue
                        else:
                            root_name = findall_list[2].rstrip().rstrip('s').capitalize()
                        if root_name.upper() in excluded_names_list:
                            continue
                        if len(root_name) < 7:
                            continue
                        if findall_list[5]:
                            name = root_name + " " + findall_list[5]
                        else:
                            name = root_name
                        name_add(comp_name_list, name, match.span(), abstract_text)

    def roman_numeral_suffix_comps(abstract_text, comp_name_list, name_base_list, two_word_termini_list,
                                   excluded_names_list, separators_list, terminators_list):
        """ Look for compounds that have Roman numeral suffixes listed in groups (e.g. Examplamides III - IX)
                    :param abstract_text: raw string of abstract text
                    :param comp_name_list: list of all compound names found in abstract text
                    :param name_base_list: regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
                    :param terminators_list: regex for the terminus if the search. Helps to find compounds with suffixes
                    that are at the end of sentences or next to punctuation.
                    :param two_word_termini_list: list of allowed termini for compound names that are more than one word
                     (e.g. allegic acid C)
                    :param excluded_names_list: list of excluded names
                    :param separators_list: regex for the characters that separate ranges (e.g. A - H)
                    :return: none
                        """
        d = re.finditer(
            '(' + name_base_list + '\s)?(' + name_base_list + ')[\s-]([IVX]{1,5})\s?' + separators_list + '\s?([IVX]{1,5})(' + terminators_list + ')',
            abstract_text)
        if d:
            for match in d:
                findall_list = tuple(match.groups())
                for entry in findall_list:
                    root_name = findall_list[2].rstrip('s')
                    if root_name in two_word_termini_list:
                        root_name = findall_list[0].rstrip() + " " + root_name
                    # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
                    if len(root_name) < 7:
                        continue
                    elif root_name.upper() in excluded_names_list:
                        continue
                    else:
                        suffix_start = findall_list[4]
                        suffix_end = findall_list[5]
                        names_roman_numeral_range_add(comp_name_list, root_name, suffix_start, suffix_end, match.span(),
                                                      abstract_text)

    def single_comps(abstract_text, comp_name_list, name_base_list, suffix_type_list, two_word_termini_list,
                     excluded_names_list, terminators_list):
        """ Look for compounds that are followed by a compound number (e.g. (1)) or range of numbers (e.g. (1 - 3))
                            :param abstract_text: raw string of abstract text
                            :param comp_name_list: list of all compound names found in abstract text
                            :param name_base_list: regex for the main part of the name (e.g. (+)-4-oxo-3-chloro-compamaide)
                            :param terminators_list: regex for the terminus if the search. Helps to find compounds with suffixes
                            that are at the end of sentences or next to punctuation.
                            :param two_word_termini_list: list of allowed termini for compound names that are more than one word
                             (e.g. allegic acid C)
                            :param excluded_names_list: list of excluded names
                            :param suffix_type_list:  regex for the characters that separate ranges (e.g. A - H)
                            :return: none
                                """
        # look for instances of single compounds (single letters, letters followed by one or two digits, and Roman numerals)
        for suffix_type in suffix_type_list:
            e = re.finditer(
                '(' + name_base_list + '\s)?(' + name_base_list + ')\s(' + suffix_type + ')(' + terminators_list + ')',
                abstract_text)

            if e:
                for match in e:
                    findall_list = tuple(match.groups())
                    for entry in findall_list:
                        if findall_list[2] in two_word_termini_list:
                            name = findall_list[0].rstrip().rstrip('s').capitalize() + " " + findall_list[2] + " " + \
                                   findall_list[4]
                        # Removes matches with very short words such as "among them, III and IV" that are not real compounds.
                        elif len(findall_list[2]) < 7:
                            continue
                        elif findall_list[2].rstrip().rstrip('s').upper() in excluded_names_list:
                            continue
                        else:
                            name = findall_list[2].rstrip().rstrip('s').capitalize() + " " + findall_list[4]

                        name_add(comp_name_list, name, match.span(), abstract_text)

                        # Add just the word closest to the bracket (e.g. lodophilone from "alkaloid lodophilone (1)"
                        # Only do this if the second word is longer than 5 characters and isn't both short and containing special characters
                        try:
                            if len(findall_list[1]) > 4 and not (
                                    len(findall_list[1]) < 8 and re.search("[\'′\",+\(\)]", findall_list[1])):
                                if findall_list[1].rstrip().rstrip('s').upper() in excluded_names_list:
                                    continue
                            else:
                                name = findall_list[1].rstrip().rstrip('s').capitalize() + " " + findall_list[2]
                                name_add(comp_name_list, name, match.span(), abstract_text)
                        except TypeError as errors:
                            continue

    compound_names = []  # list of chemical name

    group_listed_comps(text, compound_names, NAME_BASE, SEPARATORS, TERMINATORS, TWO_WORD_NAME_TERMINI, EXCLUDED_NAMES)
    explict_suffix_listed_comps(text, compound_names, NAME_BASE, SUFFIX_TYPE_LIST, TWO_WORD_NAME_TERMINI,
                                EXCLUDED_NAMES)
    methyl_ester_finder(text, compound_names, METHYL_ESTER_VARIATIONS)
    post_comps_numbers(text, compound_names, NAME_BASE, SUFFIX_TYPE_LIST, TWO_WORD_NAME_TERMINI, EXCLUDED_NAMES,
                       SEPARATORS)
    roman_numeral_suffix_comps(text, compound_names, NAME_BASE, TWO_WORD_NAME_TERMINI, EXCLUDED_NAMES, SEPARATORS,
                              TERMINATORS)
    # single_comps(text, compound_names, NAME_BASE, SUFFIX_TYPE_LIST, TWO_WORD_NAME_TERMINI, EXCLUDED_NAMES, TERMINATORS)
    # Very inaccurate, introduces many error entries. This is because it can match without a (1)
    return sorted(compound_names)


def clean_detected_items(abstract_text):
    """ Cleans out Compound classes from the chemical compound entities
            :param abstract_text: raw string of abstract text
            :return: list of names of cleaned detected chemical compounds
            """
    detected_chemical_names = name_search(abstract_text)
    clean_detected_names = []
    for x in detected_chemical_names:
        upper_item = x[0].upper()
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


def improper_parentheses_capture(chem_list):
    """ Method to remove invalid parentheses, putting above 3 functions together
                        :param chem_list: list of chemicals(strings) as tuples with match index
                        :return: False if open bracket otherwise 0 when valid parentheses
                        """
    chemical_detection_list_no_invalid_parentheses = []
    for chemical in chem_list:
        if miscellaneous_functions.bracket_matched(chemical[0]) is False:
            no_invalid_parentheses = miscellaneous_functions.remove_invalid_parentheses(chemical[0])
            chemical_detection_list_no_invalid_parentheses.append((
                (no_invalid_parentheses[:1].upper() + no_invalid_parentheses[1:]), chemical[1]))
        else:
            chemical_detection_list_no_invalid_parentheses.append(chemical)
    unique_chemical_detection_list = list(set(chemical_detection_list_no_invalid_parentheses))
    return unique_chemical_detection_list


def chem_ner_prototype(abstract_text):
    """ Detect the compounds in the article ONLY!!! works for abstracts with compound names listed in groups
    (e.g. Examplamides A - C)
            :param abstract_text: raw string of abstract text
            :return: tuple contains with: compound name, match object index and abstract text with compound placeholders
            """
    chemical_detection_list = clean_detected_items(abstract_text)
    chemical_detection_list_no_open_parentheses = improper_parentheses_capture(chemical_detection_list)
    number_of_detected_chemical_names = len(chemical_detection_list_no_open_parentheses)

    new_text_chem_list = []

    for idx, chem in enumerate(chemical_detection_list_no_open_parentheses):
        match_index = chem[1]
        comp_number = str(idx + 1)

        try:
            new_text = chem[2][:match_index[0]] + "comp_{0} ".format(comp_number) + chem[2][match_index[1]:]
            new_text_chem_list.append((chem[0], chem[1], new_text))

        except IndexError as error:
            print(error)
            # continue
    return new_text_chem_list


def main():
    with open("json_files/npatlas_origin_articles_for_NER_training.json", "r") as file:
        data = json.load(file)

        for item in data:

            abstract = item["reference"]["abstract"]
            npatlas_chemical_names = item["names"]
            number_of_actual_chemical_names = len(npatlas_chemical_names)
            doi = item["reference"]["DOI"]
            title = item["reference"]["title"]

            if abstract:
                '''chems_only = []
                chem_list = clean_detected_items(abstract)
                for i in chem_list:
                    chems_only.append(i[0])
                print(chems_only)'''

                new_text_chem_list = chem_ner_prototype(abstract)
                chem_only = []
                for i in new_text_chem_list:
                    chem_only.append(i[0])
                print(sorted(chem_only))

            else:
                continue


if __name__ == "__main__":
    main()
