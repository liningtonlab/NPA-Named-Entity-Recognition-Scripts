import pytest
import compound_name_extractor

'''TEST_TUPLE_LIST = [('descriptive example name','abstract text: Three new amides Exampleamide A-C were isolated from a deep sea
sponge named Spongebob-SPS','["Exampleamide A", "Exampleamide B", "Exampleamide C" ]')]'''

TEST_TUPLE_LIST = [('test_range_1','Two new sesterterpenoids, aspterpenacids A (1) and B (2), with an unusual carbon skeleton of a 5/3/7/6/5 ring system were isolated from the mangrove endophytic fungus Aspergillus terreus H010. Their structures were elucidated on the basis of spectroscopic methods, single-crystal X-ray diffraction analysis, and electronic circular dichroism calculations. A biogenetic pathway for 1 and 2 is proposed. Both 1 and 2 showed no significant antibacterial activity or cytotoxicity at 50 μM.', ['Aspterpenacid A', 'Aspterpenacid B']),
                   ('test_range_2', 'Three novel monomeric naphtho-\u03b3-pyrones, peninaphones A-C (compounds 1-3), along with two known bis-naphtho-\u03b3-pyrones (compounds 4 and 5) were isolated from mangrove rhizosphere soil-derived fungus Penicillium sp. HK1-22. The absolute configurations of compounds 1 and 2 were determined by electronic circular dichroism (ECD) spectra, and the structure of compound 3 was confirmed by single-crystal X-ray diffraction analysis. Compounds 4 and 5 are a pair of hindered rotation isomers. A hypothetical biosynthetic pathway for the isolated monomeric and dimeric naphtho-\u03b3-pyrones is also discussed in this study. Compounds 1-3 showed antibacterial activity against Staphylococcus aureus (ATCC 43300, 33591, 29213, and 25923) with minimum inhibitory concentration (MIC) values in the range of 12.5-50 \u03bcg/mL. Compound 3 exhibited significant activity against the rice sheath blight pathogen Rhizoctonia solani.', ['Peninaphone A', 'Peninaphone B', 'Peninaphone C'])]


def chem_NER(text):
    new_text_chem_list = compound_name_extractor.chem_ner_prototype(text)
    chem_only = []
    for i in new_text_chem_list:
        chem_only.append(i[0])
    return sorted(chem_only)


@pytest.mark.parametrize("test_tuple", TEST_TUPLE_LIST)
def test_chem_NER(test_tuple):
    print(test_tuple)
    # Asserting that expected and observed will be the same.
    expected_output = test_tuple[2]  # Load expected output.
    observed_output = chem_NER(test_tuple[1])  # Running Input through Chem NER to get observed output.
    assert expected_output == observed_output
