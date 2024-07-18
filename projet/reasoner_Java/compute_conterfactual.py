import subprocess
from owlready2 import *
from ontology_correction import get_str_obj

def keep_objects(list_obj):
    world1 = World()
    onto = world1.get_ontology("./src/main/resources/onto_herelles.owl").load()

    for i in onto.individuals():
        if(type(i) == onto.Object_Geo):
            name = get_str_obj(str(i))
            if not(name in list_obj):
                destroy_entity(i)

    onto.save(file = "./onto_herelles_temp1.owl", format = "rdfxml")
    return 0

def exec_CEO(list_obj):
    list_string = []
    
    # Supprimer tous les objets != list_obj:
    keep_objects(list_obj)

    for i in list_obj:
        world1 = World()
        onto = world1.get_ontology("./onto_herelles_temp1.owl").load()
        for j in list_obj:
            if j != i:
                destroy_entity(getattr(onto, j))
        onto.save(file = "./onto_herelles.owl", format = "rdfxml")
        python_command = ["python3","./CEO2/main.py",i,'Object_Geo'] #State_Geo si on rajoute les remblais
        counterfactual_output = subprocess.run(python_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        list_string.append(str(counterfactual_output.stdout))
    return list_string
        

def clean_output_CEO(list_string, list_obj):
    x = 0
    cf_final = []
    for i in list_string:
        cf_inter = []
        cf_output = i #str(counterfactual_output.stdout)
        cf_output = cf_output.split("generate individuals")
        cf_output = cf_output[1]
        cf_output = cf_output.split("\\n\\n")

        cf_inter.append(list_obj[x])
        for j in cf_output:
            j = j.replace("\\n","")
            j = j.replace("\"","")
            if "Assertion" in j:
                cf_inter.append(j)
        cf_final.append(cf_inter)

        x = x+1

    return cf_final

def store_CF(cf_final, list_obj):
    tab = []
    tab_create = []
    for i in cf_final:
        for j in i:
            if j in list_obj:
                if len(tab_create)==0:
                    tab_create.append(j)
                    continue
                else:
                    tab.append(tab_create)
                    tab_create = []
                    tab_create.append(j)
                    continue
            tab_create.append(j)
    tab.append(tab_create)
    
    return tab

import re

def formatting_CF(tab):
    pattern = r"(?P<numero>\d+)Assertions: \[(?P<relations>.+?)\]Distance = (?P<distance>\d+)"

    resultat = []

    for x in range(len(tab)):
        inter = []
        # resultat.append(tab[x][0])
        inter.append(tab[x][0])

        for i in range(1,len(tab[x])):
            match = re.search(pattern, tab[x][i], re.DOTALL)

            if match:
                numero = int(match.group('numero'))
                relations = match.group('relations').strip('[]').split(', ')
                distance = int(match.group('distance'))

                transformed_assertions = []
                for relation in relations:
                    relation = re.sub('[\"\'()]','',relation)
                    nom, reste = relation.split(' is a ')
                    nom_classe = reste.strip('[]')

                    res = nom, nom_classe

                    transformed_assertions.append(res)
                res = transformed_assertions, distance
                # resultat.append(res)
                inter.append(res)    
            else :
                print("wow probleme")
                print(resultat)

        resultat.append(inter)
    return resultat

