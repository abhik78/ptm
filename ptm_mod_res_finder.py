import json
import mmCIF_handling as mmCIF_handling
import sys
import csv
import os



def find_modified_aa_in_entry():

    non_poly_list = set(mc.get_cat_item_values('pdbx_poly_seq_scheme', 'mon_id'))


    list_of_modified_aa = [item for item in non_poly_list if item not in list_of_amino_acids]
    return list_of_modified_aa





def find_biomod_id(hetcode):
    with open ('ptm_data.json', 'r') as json_data:
        doc = json.load(json_data)
        x = doc['ProteinModifications']['Entry']

        for i in x:
            d = (i['CrossReference'])
            for y in d:
                if True:
                    try:
                        if y.get('Id') == hetcode:

                            biomod_id = (i.get('Id'))

                    except:
                        pass

    return biomod_id




def create_modified_aa_dict():
    modified_aa_dict = {}

    list_of_modified_aa = find_modified_aa_in_entry()
    hetcode_for_biomod_check = [het for het in list_of_modified_aa if het in biomod_residues_list]
    for modified_aa in hetcode_for_biomod_check:
        for d in pdbx_poly_seq:



            if modified_aa in d.values():
                d['biomod'] = find_biomod_id(modified_aa)
                modified_aa_dict[modified_aa] = d
    return modified_aa_dict

def write_biomod_cif_category(my_dict):


    list_of_items = [v.keys() for k, v in my_dict.items()]
    list_of_values = [v.values() for k, v in my_dict.items()]


    cif_dict = {'items': list_of_items[0], 'values' :list_of_values}

    return cif_dict




if __name__ == "__main__":

    id_list = []

    with open(sys.argv[1]) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            id_list.append(row['entry'])


    for pdbid in id_list:

        id = mmCIF_handling.get_depid_from_pdb(pdbid)

        mc = mmCIF_handling.mmcifHandling(depID=id, filesource='archive')

        mc.get_latest_model()
        mc.parse_mmcif()
        pdbx_poly_seq = mc.get_category_list_of_dictionaries('pdbx_poly_seq_scheme')

        list_of_amino_acids = ['ALA', 'ARG', 'ASP', 'ASN', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS',
                               'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL', 'PYL', 'SEC']

        biomod_residues_list = ['CSP', 'NEP', 'HIP', 'SEP', 'TPO', 'PTR']

        list_of_modified_aa = find_modified_aa_in_entry()
        hetcode_for_biomod_check = [het for het in list_of_modified_aa if het in biomod_residues_list]

        print(list_of_modified_aa)

        if not list_of_modified_aa:
            print(" %s does not have biomod residue" % (id))
        elif not hetcode_for_biomod_check:
            print("%s does not have biomod residue" % (id))
        else:

            dict_to_convert_cif_dict = create_modified_aa_dict()

            new_cif_dict = write_biomod_cif_category(dict_to_convert_cif_dict)



            mc.add_new_category(category='modified_aa_ext_ref', cat_item_value_dict=new_cif_dict)
            directory = (('/homes/abhik/work2/ptm/data/%s/%s') % (pdbid[1:-1], pdbid))

            os.makedirs(directory)
            filename = ('%s_test_1.cif' % (pdbid))
            file_path = os.path.join(directory, filename)
            #mc.set_output_mmcif('/homes/abhik/work2/ptm/data/%s/%s_test_1.cif' % (pdbid[1:-1], pdbid))
            mc.set_output_mmcif(file_path)
            mc.write_mmcif()
            mc.remove_working_path()



