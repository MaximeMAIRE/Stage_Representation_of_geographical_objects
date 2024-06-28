from owlready2 import *

def instantiation_ontologie():
    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()

    with onto:
        t1 = onto.Valid_Time("t1")
        Bati_indu = onto.Zone_industrielle_commerciale_ou_tertiaire("bati_industrielle", has_time = t1)
        bati_act = onto.Bati_activite("bati_act", has_time = t1)
        EA_1 = onto.Espaces_agricoles("EA_1", has_time = t1)
        V1 = onto.Vigne("Vigne_1", has_time = t1)
        C1 = onto.Canal("Canal_2", has_time = t1)
        inc = onto.Inconnu("inc_1", has_time = t1)

        # Pixel
        px1 = onto.Pixel("Px_1", has_state = [Bati_indu])
        px2 = onto.Pixel("Px_2", has_state = [V1])
        px3 = onto.Pixel("Px_3", has_state = [EA_1])
        px4 = onto.Pixel("Px_4", has_state = [C1])
        # Object
        obj1 = onto.Object_Geo("obj_1", has_pixels = [px1], has_state = [Bati_indu], Candidate_Final_State = [Bati_indu])
        obj2 = onto.Object_Geo("obj_2", has_pixels = [px2], has_state = [V1], Candidate_Final_State = [V1])
        obj3 = onto.Object_Geo("obj_3", has_pixels = [px3], has_state = [Bati_indu], Candidate_Final_State = [inc])
        obj4 = onto.Object_Geo("obj_4", has_pixels = [px4], has_state = [C1], Candidate_Final_State = [C1])

        ### Zone
        z1 = onto.ZoneArticle1("zone_1", z_has_pixels = [px1], contains_object = [obj1])
        z2 = onto.ZoneEA("zone_2", z_has_pixels = [px1, px2], contains_object = [obj1, obj2])
        z3 = onto.ZoneEA("zone_3", z_has_pixels = [px3, px4], contains_object = [obj3, obj4])

        ### Image creation :
        img_1 = onto.Image("Img", composed_by = [obj1, obj2, obj3, obj4])
        img_2 = onto.Image("Img2", has_rules= [z1, z2])

        ####################################""""

        # t1 = onto.Valid_Time("t1")
        # Bati_indu = onto.Zone_industrielle_commerciale_ou_tertiaire("bati_industrielle", has_time = t1)
        # bati_act = onto.Bati_activite("bati_act", has_time = t1)
        # EA = onto.Espaces_agricoles("EA_1", has_time = t1)
        # EA2 = onto.Espaces_agricoles("EA_2", has_time = t1)
        # inc = onto.Inconnu("inc_1", has_time = t1)

        # # Pixel
        # px1 = onto.Pixel("Px_1", has_state = [Bati_indu])
        # px2 = onto.Pixel("Px_2", has_state = [Bati_indu])

        # # Object
        # obj1 = onto.Object_Geo("obj_1", has_pixels = [px1,px2], has_state = [Bati_indu], Candidate_Final_State = [Bati_indu])
        # # obj1 = onto.Object_Geo("obj_1", has_pixels = [px1,px2], has_state = [Bati_indu], Candidate_Final_State = [inc])

        # ### Zone
        # z1 = onto.ZoneArticle1("zone_1", z_has_pixels = [px1], contains_object = [obj1])
        # z2 = onto.ZoneEA("zone_2", z_has_pixels = [px2], Candidate_Final_State = [EA], contains_object = [obj1])
        # # z1 = ZoneArticle1("zone_1", z_has_pixels = [px1])
        # # z2 = ZoneEA("zone_2", z_has_pixels = [px2], Candidate_Final_State = [EA])

        # ### Image creation :
        # img_1 = onto.Image("Img", composed_by = [obj1])
        # img_2 = onto.Image("Img2", has_rules= [z1,z2])

        onto.save(file = "./src/main/resources/onto_herelles.owl", format = "rdfxml")
        onto.save(file = "./onto_herelles.owl", format = "rdfxml")