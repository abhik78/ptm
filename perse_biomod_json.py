import sys
import json
import os
import traceback
with open ('ptm_data.json', 'r') as json_data:
    doc = json.load(json_data)
    print(type(doc))





x = doc['ProteinModifications']['Entry']



for i in x:
    d = (i['CrossReference'])
    for y in d:
        if True:
#            try:
#                if "phospho" in y.get('Name'):
#                    print(y.get('Id'))

            #except Exception as error:
            #    just_the_string = traceback.format_exc()
            #    print(just_the_string)
#            except:
#                pass

            try:
                if y.get('Id') == 'SEP':
                    print(y.get('Name'))
                    print(i.get('Id'))
                    print('YY')
            except:
                pass








