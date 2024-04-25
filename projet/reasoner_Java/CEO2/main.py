import sys
from onto_utils import load_ontology
from graph_generator import test_counterfactuals

def main() :
    if len(sys.argv) != 3:
        print("il faut 2 arguements a la fonction")
        sys.exit(1)

    print(sys.argv[1])
    print(sys.argv[2])
    obj = str(sys.argv[1])


    onto_path = "instruments.owl"
    onto_path2 = "onto_herelles.owl"
    onto = load_ontology(onto_path2)
    
    print(onto.has_pixels)
    # non_actionnable_property = onto.test_prop

    original_ikg = getattr(onto, obj)

    counterfactual_class = [onto.Object_Geo]
    # display graph shows the part of the graph explored, with the closest IKG in orange.
    test_counterfactuals(onto, original_ikg, counterfactual_class, non_actionnable_property = [onto.has_pixels, onto.is_in, onto.has_state], display_graph=False)



if __name__ == "__main__":
    main()