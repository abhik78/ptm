import json
import mmCIF_handling as mmCIF_handling
import sys
import csv
import os

def find_side_chain_link():

    ptnr1_dict = {}
    ptnr2_dict = {}
    result_list = []
    for d in struct_conn:
        if (d.get("conn_type_id")) == 'covale':
            ptnr1_dict[d.get("ptnr1_label_comp_id")] = d.get("ptnr1_label_atom_id")
            ptnr2_dict[d.get("ptnr2_label_comp_id")] = d.get("ptnr2_label_atom_id")

            if (ptnr1_dict.viewitems() <= aa_dict.viewitems() and ptnr2_dict.viewitems() <= phosphate_dict.viewitems()) or \
                (ptnr2_dict.viewitems() <= aa_dict.viewitems() and ptnr1_dict.viewitems() <= phosphate_dict.viewitems()):
                result_list.append(d)
    return(result_list)


if __name__ == "__main__":
    aa_dict = {'SER': 'OG', 'THR': 'OG1', 'TYR': 'OH', 'HIS': 'NE2', 'ARG': 'NH1', 'LYS': 'NZ', 'ASP': 'OD2',
               'GLN': 'NE2', 'CYS': 'SG'}
    phosphate_dict = {'PO4': 'P', 'PO3': 'P'}

    id_list = []

    with open(sys.argv[1]) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            id_list.append(row['entry'])
    print(id_list)

    for pdbid in id_list:


        id = mmCIF_handling.get_depid_from_pdb(pdbid)
        if id is not None:
            mc = mmCIF_handling.mmcifHandling(depID=id, filesource='archive')

            mc.get_latest_model()
            mc.parse_mmcif()
            struct_conn = (mc.get_category_list_of_dictionaries(category='struct_conn'))


            result_list = find_side_chain_link()

            if result_list:

                list_of_items = [d.keys() for d in result_list]
                list_of_values = [d.values() for d in result_list]

                cif_dict = {'items': list_of_items[0], 'values' :list_of_values}
                mc.add_new_category(category='side_chain_mod_aa_ext_ref', cat_item_value_dict=cif_dict)
                directory = (('/homes/abhik/work2/ptm/side_chain_data/%s/%s') % (pdbid[1:-1], pdbid))

                os.makedirs(directory)
                filename = ('%s_test_1.cif' % (pdbid))
                file_path = os.path.join(directory, filename)
                mc.set_output_mmcif(file_path)
                mc.write_mmcif()

                mc.remove_working_path()


            else:
                print('{} no side chain PO4'.format(pdbid))

        else:
            print('{} not pdbe entry'.format(pdbid))


