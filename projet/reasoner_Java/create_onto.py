from owlready2 import *
import os

def create_ontologie():
    onto = get_ontology("http://test.org/onto_herelles.owl")

    ### Image Module
    class Image(Thing):
        namespace=onto
    class Elements(Thing):
        namespace=onto
    class Pixel(Elements):
        pass
    class Object_Geo(Elements):
        pass

    ### Evolution Module
    class Evolution_Process(Thing):
        namespace=onto
    class Pixel_Evolution_Process(Evolution_Process):
        pass
    class ObjGeo_Evolution_Process(Evolution_Process):
        pass

    ### Temporal Module
    class Valid_Time(Thing):
        namespace=onto
    class Valid_Instant(Valid_Time):
        pass
    class Valid_Interval(Valid_Time):
        pass

    ### Herelles Module
    class State_Geo(Thing):
        namespace=onto

    class Inconnu(State_Geo):
        pass

    class Ignorer (State_Geo):
        pass

    class Surface_artificialisee(State_Geo):
        pass
    class Vegetation_urbaine(Surface_artificialisee):
        pass
    class Arbre_urbain(Vegetation_urbaine):
        pass
    class Pelouse(Vegetation_urbaine):
        pass
    class Jardin(Vegetation_urbaine):
        pass
    class Parc(Vegetation_urbaine):
        pass
    class Alignement_darbres_urbain(Vegetation_urbaine):
        pass
    class Ensemble_darbres_urbain(Vegetation_urbaine):
        pass
    class Bati(Surface_artificialisee):
        pass
    class Bati_residentiel(Bati):
        pass
    class Tu_discontinu(Bati_residentiel):
        pass
    class Tu_discontinu_collectif(Tu_discontinu):
        pass
    class Tu_discontinu_individuel(Tu_discontinu):
        pass
    class Tu_continu(Bati_residentiel):
        pass
    class Tu_continu_collectif(Tu_continu):
        pass
    class Tu_continu_individuel(Tu_continu):
        pass
    class Bati_activite(Bati):
        pass
    class Zone_industrielle_commerciale_ou_tertiaire(Bati_activite):
        pass
    class Bâtiment_rural(Bati_activite):
        pass
    class Serre(Bati_activite):
        pass
    class Autre_Bati(Bati):
        pass
    class Infrastructure_de_transport(Surface_artificialisee):
        pass
    class Voies_de_communication(Infrastructure_de_transport):
        pass
    class Route(Voies_de_communication):
        pass
    class Chemin(Voies_de_communication):
        pass
    class Chemin_de_fer(Voies_de_communication):
        pass
    class Route_Grande_Vitesse(Voies_de_communication):
        pass
    class Autre_Route(Voies_de_communication):
        pass
    class Equipement_transports(Infrastructure_de_transport):
        pass
    class Parking(Equipement_transports):
        pass
    class Zone_aeroportuaire(Equipement_transports):
        pass
    class Ilot_de_circulation(Equipement_transports):
        pass
    class Carrefour(Equipement_transports):
        pass
    class Pont(Equipement_transports):
        pass
    class Echangeur(Equipement_transports):
        pass
    class Autre_artificialisation(Surface_artificialisee):
        pass
    class Cimetiere(Autre_artificialisation):
        pass
    class Place(Autre_artificialisation):
        pass
    class Terrain_vacant(Autre_artificialisation):
        pass
    class Terrain_de_Sport(Autre_artificialisation):
        pass
    class Piscine_exterieure(Autre_artificialisation):
        pass
    class Zone_sportif_loisir(Autre_artificialisation):
        pass
    class Zone_dextraction(Autre_artificialisation):
        pass

    class Eau(State_Geo):
        pass
    class Surface_en_eau_artificielle(Eau):
        pass
    class Canal(Surface_en_eau_artificielle):
        pass
    class Bassin_artificiel(Surface_en_eau_artificielle):
        pass
    class Surface_en_eau_naturelle(Eau):
        pass
    class Etendue_deau(Surface_en_eau_naturelle):
        pass
    class Cours_deau(Surface_en_eau_naturelle):
        pass

    class Espaces_agricoles(State_Geo):
        pass
    class Parcelle_agricole(Espaces_agricoles):
        pass
    class Vigne(Parcelle_agricole):
        pass
    class Autres_cultures(Parcelle_agricole):
        pass
    class Surface_herbeuse_agricole(Parcelle_agricole):
        pass
    class Element_boise_agricole(Espaces_agricoles):
        pass
    class Groupe_darbres_agricole_sylviculture(Element_boise_agricole):
        pass
    class Alignement_darbres_agricole(Element_boise_agricole):
        pass
    class Verger(Element_boise_agricole):
        pass
    class Autre_vegetation_agricole(Espaces_agricoles):
        pass
    class Haie(Autre_vegetation_agricole):
        pass

    class Espaces_forestiers_et_naturels(State_Geo):
        pass
    class Foret(Espaces_forestiers_et_naturels):
        pass
    class Espace_libre_naturel(Espaces_forestiers_et_naturels):
        pass
    class Sable(Espace_libre_naturel):
        pass
    class Zones_humides(Espaces_forestiers_et_naturels):
        pass
    class Vegetation_autre(Espaces_forestiers_et_naturels):
        pass
    class Surface_herbeuse_naturelle(Vegetation_autre):
        pass

    ### Object properties
    class composed_by(ObjectProperty, InverseFunctionalProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Image]
        range     = [Elements]
    class has_pixels(ObjectProperty, InverseFunctionalProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Object_Geo]
        range     = [Pixel]
    class has_state(ObjectProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Elements]
        range     = [State_Geo]
    class is_involved(ObjectProperty):
        namespace=onto
        domain    = [Elements]
        range     = [Evolution_Process]
    class has_duration(ObjectProperty):
        namespace=onto
        domain    = [Evolution_Process]
        range     = [Valid_Time]
    class has_time(ObjectProperty, FunctionalProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [State_Geo]
        range     = [Valid_Time]

    ### ajout de la classe Zone :
    class Zone(Elements):
        namespace=onto

    class ZoneEau(Zone):
        pass

    class ZoneEA(Zone):
        pass

    class ZoneArticle1(Zone):
        pass

    class Zone_Z2(Zone):
        pass

    class ZoneSA(Zone):
        pass

    # ajout de relation pour cette derniere :
    class has_rules(ObjectProperty, InverseFunctionalProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Image]
        range     = [Zone]

    class z_has_pixels (ObjectProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Zone]
        range     = [Pixel]

    class Candidate_Final_State(ObjectProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Elements]
        range     = [State_Geo]

    class is_in(ObjectProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Object_Geo]
        range     = [Zone]

    class contains_object(ObjectProperty,  IrreflexiveProperty):
        namespace=onto
        domain    = [Zone]
        range     = [Object_Geo]
        inverse_property = is_in

    class is_pixel_of_zone(ObjectProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Pixel]
        range     = [Zone]
        inverse_property = z_has_pixels

    class is_pixel_of(ObjectProperty, FunctionalProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [Pixel]
        range     = [Object_Geo]
        inverse_property = has_pixels


    class hasPostitionX(DataProperty):
        namespace=onto
        domain = [Pixel]
        range= [int]

    class hasPostitionY(DataProperty):
        namespace=onto
        domain    = [Pixel]
        range     = [int]

    class hasValueClust(DataProperty):
        namespace=onto
        domain    = [Pixel]
        range     = [int]

    class is_Neighbor_Of(ObjectProperty, SymmetricProperty):
        namespace=onto
        domaine   = [Object_Geo]
        range     = [Object_Geo]

    ### Obstacle :
    class Obstacle(Thing):
        namespace = onto

    class Ecoulement_des_crues(Obstacle):
        pass

    class Remblais(Obstacle):
        pass

    class createSome(ObjectProperty, IrreflexiveProperty):
        namespace=onto
        domain    = [State_Geo]
        range     = [Obstacle]

    try:
        os.mkdir('./src/main/resources')
    except:
        print("fihcier deja existant")

    Zone.equivalent_to.append(Zone & Not(contains_object.some(Candidate_Final_State.some(Inconnu))))

    ZoneArticle1.equivalent_to.append(Zone & Not(contains_object.some(Candidate_Final_State.some(Zone_industrielle_commerciale_ou_tertiaire))) )
    ZoneEA.equivalent_to.append(Zone & contains_object.only(Candidate_Final_State.only(Espaces_agricoles)))
    ZoneSA.equivalent_to.append(Zone & contains_object.only(Candidate_Final_State.only(Surface_artificialisee)))
    Zone_Z2.equivalent_to.append(Zone & contains_object.only(Candidate_Final_State.only(Vegetation_urbaine)) & contains_object.only(Candidate_Final_State.only(Not(createSome.some(Remblais)))))
    ZoneEau.equivalent_to.append(Zone & contains_object.only(Candidate_Final_State.some(Eau)))

    AllDifferent([Elements, Evolution_Process, Image, State_Geo, Valid_Time])
    AllDifferent([Object_Geo, Pixel, Zone])

    AllDifferent([Eau, Espaces_agricoles, Espaces_forestiers_et_naturels, Surface_artificialisee, Inconnu])
    AllDifferent([Surface_en_eau_artificielle, Surface_en_eau_naturelle])
    AllDifferent([Bassin_artificiel, Canal])
    AllDifferent([Cours_deau, Etendue_deau])

    AllDifferent([Autre_vegetation_agricole,Element_boise_agricole,Parcelle_agricole])
    AllDifferent([Alignement_darbres_agricole, Groupe_darbres_agricole_sylviculture, Verger])
    AllDifferent([Autres_cultures, Surface_herbeuse_agricole, Vigne])
    AllDifferent([Espace_libre_naturel, Foret, Vegetation_autre, Zones_humides])
    
    AllDifferent([Autre_artificialisation, Infrastructure_de_transport, Vegetation_urbaine, Bati])
    AllDifferent([Cimetiere, Piscine_exterieure, Place, Terrain_de_Sport, Terrain_vacant, Zone_dextraction, Zone_sportif_loisir])
    AllDifferent([Autre_Bati, Bati_activite, Bati_residentiel])
    AllDifferent([Bâtiment_rural, Serre, Zone_industrielle_commerciale_ou_tertiaire])
    AllDifferent([Tu_continu, Tu_discontinu])
    AllDifferent([Tu_continu_individuel, Tu_continu_collectif])
    AllDifferent([Tu_discontinu_collectif, Tu_discontinu_individuel])
    AllDifferent([Equipement_transports, Voies_de_communication])
    AllDifferent([Carrefour, Echangeur, Ilot_de_circulation, Parking, Pont, Zone_aeroportuaire])
    AllDifferent([Autre_Route, Chemin, Chemin_de_fer, Route, Route_Grande_Vitesse])
    AllDifferent([Alignement_darbres_urbain, Arbre_urbain, Ensemble_darbres_urbain, Jardin, Parc, Pelouse])


    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

    onto.save(file = "./src/main/resources/onto_herelles.owl", format = "rdfxml")
    onto.save(file = "./onto_herelles.owl", format = "rdfxml")
    