import pytest
import compound_name_extractor

TEST_TUPLE_LIST = [('test_range_1',
                    'Two new sesterterpenoids, aspterpenacids A (1) and B (2), with an unusual carbon skeleton of a 5/3/7/6/5 ring system were isolated from the mangrove endophytic fungus Aspergillus terreus H010. Their structures were elucidated on the basis of spectroscopic methods, single-crystal X-ray diffraction analysis, and electronic circular dichroism calculations. A biogenetic pathway for 1 and 2 is proposed. Both 1 and 2 showed no significant antibacterial activity or cytotoxicity at 50 μM.',
                    ['Aspterpenacid A', 'Aspterpenacid B']),
                   ('test_range_2',
                    'Three novel monomeric naphtho-\u03b3-pyrones, peninaphones A-C (compounds 1-3), along with two known bis-naphtho-\u03b3-pyrones (compounds 4 and 5) were isolated from mangrove rhizosphere soil-derived fungus Penicillium sp. HK1-22. The absolute configurations of compounds 1 and 2 were determined by electronic circular dichroism (ECD) spectra, and the structure of compound 3 was confirmed by single-crystal X-ray diffraction analysis. Compounds 4 and 5 are a pair of hindered rotation isomers. A hypothetical biosynthetic pathway for the isolated monomeric and dimeric naphtho-\u03b3-pyrones is also discussed in this study. Compounds 1-3 showed antibacterial activity against Staphylococcus aureus (ATCC 43300, 33591, 29213, and 25923) with minimum inhibitory concentration (MIC) values in the range of 12.5-50 \u03bcg/mL. Compound 3 exhibited significant activity against the rice sheath blight pathogen Rhizoctonia solani.',
                    ['Peninaphone A', 'Peninaphone B', 'Peninaphone C']),
                   ('test_range_double',
                    'Five new benzenoids, benzocamphorins A-E (1-5), and 10 recently isolated triterpenoids, camphoratins A-J (16-25), together with 23 known compounds including seven benzenoids (6-12), three lignans (13-15), and 13 triterpenoids (26-38) were isolated from the fruiting body of Taiwanofungus camphoratus. Their structures were established by spectroscopic analysis. Selected compounds were examined for cytotoxic and anti-inflammatory activities. Compounds 9 and 21 showed moderate cytotoxicity against MCF-7 and Hep2 cell lines with ED(50) values of 3.4 and 3.0Î¼g/mL, respectively. Compounds 21, 25, 26, 29-31, 33, and 36 demonstrated potent anti-inflammatory activity by inhibiting lipopolysaccharide (LPS)-induced nitric oxide (NO) production with IC(50) values of 2.5, 1.6, 3.6, 0.6, 4.1, 4.2, 2.5, and 1.5Î¼M, respectively, which were better than those of the nonspecific nitric oxide synthase (NOS) inhibitor N-nitro-l-arginine methyl ester (l-NAME) (IC(50): 25.8Î¼M). These results may substantiate the use of T. camphoratus in traditional Chinese medicine (TCM) for the treatment of inflammation and cancer-related diseases. The newly discovered compounds deserve further development as anti-inflammatory candidates.',
                    ['Benzocamphorin A', 'Benzocamphorin B', 'Benzocamphorin C', 'Benzocamphorin D', 'Benzocamphorin E',
                     'Camphoratin A', 'Camphoratin B', 'Camphoratin C', 'Camphoratin D', 'Camphoratin E',
                     'Camphoratin F', 'Camphoratin G', 'Camphoratin H', 'Camphoratin I', 'Camphoratin J']),
                   ('test_standard_secondary_letter',
                    'As part of our research to discover novel bioactive natural products from marine microorganisms, five bagremycin analogues, including the previously unreported bagremycins F (1) and G (2), were isolated from a marine actinomycete Streptomyces sp. ZZ745. The structures of these compounds were determined by means of NMR spectroscopic analysis, HRESIMS data, and optical rotation. Both bagremycins F (1) and G (2) showed antibacterial activity against Escherichia coli, with MIC values of 41.8 and 61.7 Î¼ M, respectively.',
                    ['Bagremycin F', 'Bagremycin G']),
                   ('test_standard_tertiary_letter',
                    'Three novel cyclodepsipeptides, alveolarides A (1), B (2), and C (3), each possessing the rare 2,3-dihydroxy-4-methyltetradecanoic acid unit and a Î²-phenylalanine amino acid residue, along with the known peptide scopularide were isolated and identified from the culture broth of Microascus alveolaris strain PF1466. The pure compounds were evaluated for biological activity, and alveolaride A (1) provided strong in vitro activity against the plant pathogens Pyricularia oryzae, Zymoseptoria tritici, and Ustilago maydis. Moderate activity of alveolaride A was observed under in planta conditions against Z. tritici, Puccinia triticina, and Phakopsora pachyrhizi. Structures of 1, 2, and 3 were determined by detailed analysis of NMR (1D and 2D) and mass spectrometry data. The partial absolute configuration of alveolaride A (1) was established.',
                    ['Alveolaride A', 'Alveolaride B', 'Alveolaride C']),
                   ('test_standard_secondary_letter_v2',
                    'One new cerapicane cerrenin A (1), and two new isohirsutane sesquiterpenoids cerrenins B and C (2 and 3), were isolated from the broth extract of Cerrena sp. A593. Cerrenin A featured a rare cage-like bicyclo[3.2.1]octane skeleton, and cerrenin B represented the rearranged triquinane-type sesquiterpenoid. Their structures were extensively elucidated by NMR spectroscopic analysis with the absolute configuration determined by X-ray crystallography and ECD calculations. The anti-cancer activity for all the compounds were evaluated, and their plausible biosynthetic relationships involving fascinating carbon skeleton rearrangements were also suggested.',
                    ['Cerrenin A', 'Cerrenin B', 'Cerrenin C']),
                   ('test_methyl_ether',
                    'Penicimutanolones A (1) and B (2), penicimutanolone A methyl ether (3), and penicimumide (4), four new antitumor metabolites, were isolated from a neomycin-resistant mutant of the marine-derived fungus Penicillium purpurogenum G59. The structures of the compounds were elucidated by spectroscopic methods, and the absolute configurations were determined by X-ray crystallography and calculated ECD. In MTT and SRB assays, compounds 1â€“3 showed strong inhibitory effects on 14 human cancer cell lines. Compounds 1 and 2 maybe induce apoptosis of cancer cells mainly due to the inhibition of the expression of survivin, a client protein of HSP90. In addition, in vivo antitumor activity was observed for compound 1 in murine sarcoma HCT116 tumor-bearing Kunming mice, using docetaxel as a positive control.',
                    ['Penicimumide', 'Penicimutanolone A', 'Penicimutanolone A methyl ether', 'Penicimutanolone B']),
                   ('test_standard_secondary_letter_v3',
                    'The marine fungus Chondrostereum sp. was collected from a soft coral Sarcophyton tortuosum from the South China Sea. This fungus was cultured in glucose-peptone-yeast (GPY) medium and the culture broth was extracted with EtOAc. By the method of 1H NMR pre-screening and tracing the diagnostic proton signals of the methyl groups, two new hirsutane-type sesquiterpenoids, chondrosterins N and O (1 and 2) were isolated from the metabolite extracts. Their structures were elucidated on the basis of MS, 1D and 2D NMR data.',
                    ['Chondrosterin N', 'Chondrosterin O']),
                   ('test_standard_secondary_letter_v4',
                    'Two new decaline metabolites, wakodecalines A and B, were isolated from a fungus, Pyrenochaetopsis sp. RK10-F058, by screening for structurally unique metabolites using LC/MS analysis. Their structures were determined on the basis of NMR and mass spectrometric measurements. The absolute structures were confirmed by a combination of chemical methods including chemical degradation, a modified Mosher"s method and Marfey"s method, and comparison of the experimental electronic CD (ECD) spectrum with calculated one. Both compounds had a cyclopentanone-fused decaline skeleton and an N-methylated amino acid moiety derived from a serine. They showed moderate antimalarial activity against the Plasmodium falciparum 3D7 strain.',
                    ['Wakodecaline A', 'Wakodecaline B']),
                   ('test_brackets',
                    'A new polyketide erubescensoic acid (1), and the previously reported xanthonopyrone, SPF-3059-26 (2), were isolated from the uninvestigated fractions of the ethyl acetate crude extract of the marine sponge-associated fungus Penicillium erubescens KUFA0220. The structures of the new compound, erubescensoic acid (1), and the previously reported SPF-3059-26 (2), were elucidated by extensive analysis of 1D and 2D-NMR spectra as well as HRMS. The absolute configuration of the stereogenic carbon of erubescensoic acid (1) was determined by X-ray analysis. Erubescensoic acid (1) and SPF-3059-26 (2), together with erubescenschromone B (3), penialidin D (4), and 7-hydroxy-6-methoxy-4-oxo-3-[(1E)-3-oxobut-1-en-1-yl]-4H-chromen-5-carboxylic acid (5), recently isolated from this fungus, were assayed for their antibacterial activity against gram-positive and gram-negative reference strains and the multidrug-resistant (MDR) strains from the environment. The capacity of these compounds to interfere with the bacterial biofilm formation and their potential synergism with clinically relevant antibiotics for the MDR strains were also investigated.',
                    ['7-hydroxy-6-methoxy-4-oxo-3-[(1e)-3-oxobut-1-en-1-yl]-4h-chromen-5-carboxylic acid',
                     'Erubescenschromone B',
                     'Erubescensoic acid',
                     'Penialidin D',
                     'Spf-3059-26']),
                   ('test_methyl_ether_2',
                    "Diaporone A (1), one new dihydroisocoumarin derivative and four known α-dibenzopyrones, alternariol (2), 5'-hydroxyalternariol (3), alternariol 4,10-dimethyl ether (4), and alternariol 4-methyl ether (5) were isolated from the crude extract of the plant endophytic fungus Diaporthe sp. Their structures were determined on the basis of spectroscopic analysis, including 1D and 2D NMR techniques as well as HRESIMS and comparison with data from the literature. The absolute configuration of 1 was assigned by electronic circular dichroism (ECD) calculations. Compound 1 showed moderate antibacterial activity against Bacillus subtilis with the MIC value of 66.7μM, and exhibited weak cytotoxicity against human cervical carcinoma (HeLa) cell line with IC50 value of 97.4μM.",
                    ["5'-hydroxyalternariol",
                     'Alternariol',
                     'Alternariol 4,10-dimethyl ether',
                     'Alternariol 4-methyl ether',
                     'Diaporone A']),
                   ('test_standard_secondary_letter_parentheses',
                    'Ralstonia solanacearum has an orphan hybrid polyketide synthase-nonribosomal peptide synthetase gene cluster. We herein isolate its products (named ralstonins A and B) from R. solanacearum and elucidate their structures and biological activities. Ralstonins are unusual lipodepsipeptides composed of 11 amino acids (containing unique amino acids such as Î²-hydroxytyrosine and dehydroalanine) and a 3-amino-2-hydroxyoctadecanoic acid, and their production is controlled by quorum sensing, a mechanism of bacterial cell-cell communication. Ralstonins exhibited chlamydospore-inducing activity and phytotoxicity.',
                    ['Ralstonin A', 'Ralstonin B'])]


def chem_NER(text):
    new_text_chem_list = compound_name_extractor.chem_ner_prototype(text)
    chem_only = []
    for i in new_text_chem_list:
        chem_only.append(i[0])
    return sorted(chem_only)


@pytest.mark.parametrize("test_tuple", TEST_TUPLE_LIST)
def test_chem_NER(test_tuple):
    # Asserting that expected and observed will be the same.
    expected_output = test_tuple[2]  # Load expected output.
    observed_output = chem_NER(test_tuple[1])  # Running Input through Chem NER to get observed output.
    assert expected_output == observed_output
