from owlready2 import *

def obj_reltaion(obj):
    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()

    liste_objet = []
    liste_relation = []

    for i in onto.object_properties():
        o,rel = str(i).split(".")
        attr_value = getattr(obj, rel)
        if attr_value is not None:
            try :
                for j in attr_value:
                    if not(j in liste_objet):
                        liste_objet.append(j)
                        liste_relation.append(rel)
                    elif not(rel in liste_relation):
                        liste_objet.append(j)
                        liste_relation.append(rel)
            except Exception as e:
                if not(attr_value in liste_objet):
                    liste_objet.append(attr_value)
                    liste_relation.append(rel)
                elif not(rel in liste_relation):
                    liste_objet.append(attr_value)
                    liste_relation.append(rel)

    return liste_relation, liste_objet

def get_str_obj(obj):
    x, y = str(obj).split(".")
    return y

def get_str_tab_obj(tab_obj):
    res = []
    for i in tab_obj:
        res.append(get_str_obj(i))
    return res

def compare_liste(tab1, tab2):
    tabx = ["must"]
    taby = ["have"]
    for i in tab1:
        x = 0
        for j in tab2:
            if i == j:
                x = 1
                break
        if(x == 0):
            tabx.append(i)

    for i in tab2:
        x = 0
        for j in tab1:
            if i == j:
                x = 1
                break
        if(x == 0):
            taby.append(i)
    
    return [tabx,taby]

def tab_contain_object(tab, obj):
    res = False
    for i in tab:
        if obj == i:
            res = True
    return res

def index_tab(tab, name):
    for i in range(len(tab)):
        if tab[i] == name:
            return i
    return -1

def get_relation_obj(tab):
    grouped_by_relation = {}
    for i in range(0, len(tab), 2):
        relation = tab[i]
        if relation in grouped_by_relation:
            grouped_by_relation[relation].append(tab[i+1])
        else:
            grouped_by_relation[relation] = [tab[i+1]]

    tableau_relations = []
    for k,v in grouped_by_relation.items():
        tableau_relations.append([k, v])

    return tableau_relations

def replace_object(obj, new_obj):
    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()
    
    ob = getattr(onto,str(new_obj))
    if (ob != None):
        type = ob.is_a[0]
        
    else:
        type = new_obj[0].upper() + new_obj[1:]
        type = getattr(onto,type)

    obj = getattr(onto,obj)
    obj.is_a.clear()
    obj.is_a.append(type)
    onto.save(file = "./src/main/resources/onto_herelles.owl", format = "rdfxml")

def modify_object(tab_curr, tab_ok, tab_change):
    for i in range(len(tab_ok)):
        for j in range(len(tab_curr)):
            if tab_ok[i] == tab_curr[j]:
                tab_curr[j] = 0

    x = 0
    # print("\n\n\n",len(tab_curr), tab_curr,"\n")
    # print(len(tab_change), tab_change)
    for i in tab_curr:
        if not(i == 0):
            # print("\n\n",i, tab_change[x])
            replace_object(i,tab_change[x])
            x = x+1
    return 0

def modify_solution(resultat):
    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()

    with onto :
        for num_inc in range(len(resultat)):
            # afficher les solutions possible, puis laisser l'utilisateur rentrer son choix
            numero_sol = 0
            for j in range(len(resultat[num_inc])):
                print(numero_sol,"\n", resultat[num_inc][j],"\n")
                numero_sol = numero_sol +1
            num_solution = input("enter a number\n")
            num_solution = int(num_solution)

            # recuperation des relations que l'on souhaite mettre
            tab_wanted = []
            for i in range (len(resultat[num_inc][num_solution][0])):
                relation, obj_name = resultat[num_inc][num_solution][0][i][0].split(" ")
                tab_wanted.append(relation)
                tab_wanted.append(obj_name)

                
            tab_wanted = get_relation_obj(tab_wanted)
            obj_to_change = getattr(onto, resultat[num_inc][0])
            
            tab_curr = []
            x,y = obj_reltaion(obj_to_change)

            y = get_str_tab_obj(y)
            for i in range(len(x)):
                tab_curr.append(x[i])
                tab_curr.append(y[i])
            tab_curr = get_relation_obj(tab_curr)

            for i in range(len(tab_wanted)):
                tab_ok = []
                tab_change = []
                rel = tab_wanted[i][0]
                for j in range(len(tab_curr)):
                    if rel == tab_curr[j][0]:
                        for k in tab_wanted[i][1]:
                            if tab_contain_object(tab_curr[j][1], k):
                                tab_ok.append(k)
                            else:
                                tab_change.append(k)
                        print(tab_curr[j][1],"\n",tab_ok,"\n",tab_change)
                        modify_object(tab_curr[j][1], tab_ok, tab_change)
                        break
