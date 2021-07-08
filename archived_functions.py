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