import subprocess
from owlready2 import *

from create_onto import *
from instantiation_onto import *
from test_inconsistance import *
from compute_conterfactual import *
from ontology_correction import *

if __name__ == "__main__":
    create_ontologie()
    instantiation_ontologie()

    val_incon = False
    while(val_incon == False):
        val_cons, output = test_consistency()
        if val_cons:
            print("Ontologie cohérente.")
            val_incon = True
            break
        else :
            print("Ontologie incohérente.")

        # récuperation des objets et zones
        list_zone, list_obj = clean_output_cons(output)
        print("liste zone :",list_zone,"\nliste obj :", list_obj)

        # calcul des explications contrefactuelles et clean
        list_string = exec_CEO(list_obj)
        cf_final = clean_output_CEO(list_string, list_obj)
        # for i in cf_final:
        #     print(i,"\n")
        tab = store_CF(cf_final, list_obj)
        resultat = formatting_CF(tab)
        
        # Modification des objets inconsistants pour rendre l'ontologie consistante.
        modify_solution(resultat)


    # ici on a une ontologie cohérente, on va pouvoir commencer a chercher les potentiels
    # types des objets avec un cluster inconnu ...
    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()

    oui = input("Proposer des solutions pour les clusters inconnus ? oui / non \n")
    if oui == "oui":
        for i in onto.individuals():
            if onto.Ignorer in i.is_a :
                print("pas de type :", i)
                i.is_a.clear()
                i.is_a.append(onto.Inconnu)


    onto.save(file = "./src/main/resources/onto_herelles.owl", format = "rdfxml")
    
    val_incon = False
    while(val_incon == False):
        val_cons, output = test_consistency()
        if val_cons:
            print("Ontologie cohérente.")
            val_incon = True
            break
        else :
            print("Ontologie incohérente.")

        # récuperation des objets et zones
        list_zone, list_obj = clean_output_cons(output)
        print("liste zone :",list_zone,"\nliste obj :", list_obj)

        # calcul des explications contrefactuelles et clean
        list_string = exec_CEO(list_obj)
        cf_final = clean_output_CEO(list_string, list_obj)
        for i in cf_final:
            print(i,"\n")
        tab = store_CF(cf_final, list_obj)
        resultat = formatting_CF(tab)
        
        # Modification des objets inconsistants pour rendre l'ontologie consistante.
        modify_solution(resultat)
