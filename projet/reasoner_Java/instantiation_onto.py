from owlready2 import *
import pandas as pd
import skimage
import numpy as np
import xml.etree.ElementTree as ET
from skimage import measure, morphology, color, segmentation
import matplotlib.pyplot as plt
from collections import Counter
from shapely.geometry import Polygon, Point


def fonctionF(final_type, str_state, onto):
    match final_type:
        case "Eau":
            jardin = onto.Eau(str_state)
        case "Surface_en_eau_artificielle":
            jardin = onto.Surface_en_eau_artificielle(str_state)
        case "Bassin_Artificiel":
            jardin = onto.Bassin_Artificiel(str_state)
        case "Canal":
            jardin = onto.Canal(str_state)
        case "Cours_deau":
            jardin = onto.Cours_deau(str_state)
        case "Etendue_deau":
            jardin = onto.Etendue_deau(str_state)

        case "Espaces_agricoles":
            jardin = onto.Espaces_agricoles(str_state)
        case "Autre_vegetation_agricole":
            jardin = onto.Autre_vegetation_agricole(str_state)
        case "Haie":
            jardin = onto.Haie(str_state)
        case "Element_boise_agricole":
            jardin = onto.Element_boise_agricole(str_state)
        case "Alignement_darbre_agricole":
            jardin = onto.Alignement_darbre_agricole(str_state)
        case "Groupe_darbres_agricole_sylviculture":
            jardin = onto.Groupe_darbres_agricole_sylviculture(str_state)
        case "Parcelle_agricole":
            jardin = onto.Parcelle_agricole(str_state)
        case "Autres_cultures":
            jardin = onto.Autres_cultures(str_state)
        case "Surface_herbeuse_agricole":
            jardin = onto.Surface_herbeuse_agricole(str_state)
        case "Vigne":
            jardin = onto.Vigne(str_state)

        case "Espaces_forestiers_et_naturels":
            jardin = onto.Espaces_forestiers_et_naturels(str_state)
        case "Espace_libre_naturel":
            jardin = onto.Espace_libre_naturel(str_state)
        case "Sable":
            jardin = onto.Sable(str_state)
        case "Foret":
            jardin = onto.Foret(str_state)
        case "Vegetation_autre":
            jardin = onto.Vegetation_autre(str_state)
        case "Surface_herbeuse_naturelle":
            jardin = onto.Surface_herbeuse_naturelle(str_state)
        case "Zones_humides":
            jardin = onto.Zones_humides(str_state)

        case "Ignorer":
            jardin = onto.Ignorer(str_state)
        case "Inconnu":
            jardin = onto.Inconnu(str_state)

        case "Surface_artificialisee":
            jardin = onto.Surface_artificialisee(str_state)
        case "Autre_artificialisation":
            jardin = onto.Autre_artificialisation(str_state)
        case "Cimetiere":
            jardin = onto.Cimetiere(str_state)
        case "Piscine_exterieure":
            jardin = onto.Piscine_exterieure(str_state)
        case "Place":
            jardin = onto.Place(str_state)
        case "Terrain_de_Sport":
            jardin = onto.Terrain_de_Sport(str_state)
        case "terrain_vacant":
            jardin = onto.terrain_vacant(str_state)
        case "Zone_dextraction":
            jardin = onto.Zone_dextraction(str_state)
        case "Zone_sportif_loisir":
            jardin = onto.Zone_sportif_loisir(str_state)
        case "Bati":
            jardin = onto.Bati(str_state)
        case "Autre_bati":
            jardin = onto.Autre_bati(str_state)
        case "Bati_activite":
            jardin = onto.Bati_activite(str_state)
        case "Batiment_rural":
            jardin = onto.Batiment_rural(str_state)
        case "Serre":
            jardin = onto.Serre(str_state)
        case "Zone_Industrielle_commerciale_ou_tertiaire":
            jardin = onto.Zone_Industrielle_commerciale_ou_tertiaire(str_state)
        case "Bati_residentiel":
            jardin = onto.Bati_residentiel(str_state)
        case "Tu_continu_collectif":
            jardin = onto.Tu_continu_collectif(str_state)
        case "Tu_continu_individuel":
            jardin = onto.Tu_continu_individuel(str_state)
        case "Tu_discontinu":
            jardin = onto.Tu_discontinu(str_state)
        case "Tu_discontinu_collectif":
            jardin = onto.Tu_discontinu_collectif(str_state)
        case "Tu_discontinu_individuel":
            jardin = onto.Tu_discontinu_individuel(str_state)
        case "Infrastructure_de_transport":
            jardin = onto.Infrastructure_de_transport(str_state)
        case "Equipement_transports":
            jardin = onto.Equipement_transports(str_state)
        case "Carrefour":
            jardin = onto.Carrefour(str_state)
        case "Echangeur":
            jardin = onto.Echangeur(str_state)
        case "Ilot_de_circulation":
            jardin = onto.Ilot_de_circulation(str_state)
        case "Parking":
            jardin = onto.Parking(str_state)
        case "Pont":
            jardin = onto.Pont(str_state)
        case "Zone_aeroportuaire":
            jardin = onto.Zone_aeroportuaire(str_state)
        case "Voies_de_communication":
            jardin = onto.Voies_de_communication(str_state)
        case "Autre_Route":
            jardin = onto.Autre_Route(str_state)
        case "Chemin":
            jardin = onto.Chemin(str_state)
        case "Chemin_de_fer":
            jardin = onto.Chemin_de_fer(str_state)
        case "Route":
            jardin = onto.Route(str_state)
        case "Route_Grande_Vitesse":
            jardin = onto.Route_Grande_Vitesse(str_state)
        case "Vegetation_urbaine":
            jardin = onto.Vegetation_urbaine(str_state)
        case "Alignement_darbres_urbain":
            jardin = onto.Alignement_darbres_urbain(str_state)
        case "Arbre_urbain":
            jardin = onto.Arbre_urbain(str_state)
        case "Ensemble_darbres_urbain":
            jardin = onto.Ensemble_darbres_urbain(str_state)
        case "Jardin":
            jardin = onto.Jardin(str_state)
        case "Parc":
            jardin = onto.Parc(str_state)
        case "Pelouse":
            jardin = onto.Pelouse(str_state)

        case _:
            print("je suis final_type: ", final_type, "et je n'appartient pas aux cas precedent !")
            jardin = onto.Ignorer(str_state)

    return jardin


def extract_coordinates(kml_file):
    tree = ET.parse(kml_file)
    root = tree.getroot()

    ns = {'kml': 'http://www.opengis.net/kml/2.2', 'gx': 'http://www.google.com/kml/ext/2.2'}
    coordinates_element = root.find('.//gx:LatLonQuad/kml:coordinates', ns)

    if coordinates_element is not None:
        coordinates_text = coordinates_element.text.strip()
        coordinates_list = coordinates_text.split()
        coordinates_list = [coord.strip() for coord in coordinates_list]

        coordinates = []

        for coord in coordinates_list:
            lon_lat = coord.split(',')
            lon_lat_tuple = tuple(map(float, lon_lat))
            coordinates.append(lon_lat_tuple)

        return coordinates
    else:
        raise ValueError("Pas de coordinates dans le fichier kml.")
    

def calcul_droite(p1, p2):
    a = (p2[1]-p1[1]) / (p2[0]-p1[0])
    x = p1[0]
    y = p1[1]

    b = -a*x + y
    return y, a, x, b


def calcul_point_droite(a, x, b, p1, p2, nb_point):
    nb = (p2[0] - p1[0]) / nb_point
    tab = []
    for i in range(nb_point):
        x1 = x + i*nb
        y1 = a*x1 + b
        tab.append((x1,y1))

    return tab


def print_fig(tab, coords):
    fig, ax = plt.subplots()
    polygon = Polygon(coords)

    for j in tab :
        for i in j:
            point = Point(i[0], i[1])
            ax.plot(point.x, point.y, marker='.', color='blue')


    ax.plot(*polygon.exterior.xy, color='red')
    plt.show()

def max(tab):
    compteur = Counter(tab)
    nombre_frequent = compteur.most_common(1)[0][0]  
    return nombre_frequent

def import_image(name_file, size_col):
    tree = ET.parse(name_file)
    root = tree.getroot()
    tab_test = []
    tab = []
    tab_cluster = []
    nb_cluster = 0

    for i in root:
        if (i.tag == 'classes'):
            for j in i:
                tab_cluster.append(j.attrib["name"])
                nb_cluster = nb_cluster+1
        elif (i.tag == 'values'):
            for k in range(len(i)) :
                tab_test.append(int(i[k].text)+1)
                if((k+1) % size_col == 0) :
                    tab.append(tab_test)
                    tab_test = []
    image = np.array(tab)

    return image, tab_cluster

def delete_artifacts_from_image(image):
    objects, num = measure.label(image, background=0, connectivity=2, return_num = True)
    large_objects = morphology.remove_small_objects(objects, min_size=10, connectivity=3)

    small_objects = objects ^ large_objects
    large_objects2 = np.copy(large_objects)
    neighborhood_size = 1
    sortie = 1

    while(sortie):
        sortie = 0
        for y in range(small_objects.shape[0]):
            for x in range(small_objects.shape[1]):
                if small_objects[y, x] != 0:
                    tab_tab = []
                    for dy in range(-neighborhood_size, neighborhood_size + 1):
                        for dx in range(-neighborhood_size, neighborhood_size + 1):
                            ny = y + dy
                            nx = x + dx
                            if 0 <= ny < large_objects.shape[0] and 0 <= nx < large_objects.shape[1]:
                                if large_objects[ny, nx] != 0:
                                    tab_tab.append(large_objects[ny, nx])
                    if len(tab_tab) != 0:
                        large_objects[y, x] = max(tab_tab)
                        small_objects[y, x] = 0
                    else:
                        sortie = 1

    final_objects = large_objects

    return large_objects2, final_objects

def reconstitute_image(image,large_objects2,final_objects):
    tab_m = []
    tab_jhj = []

    for i in range(len(large_objects2)):
        for j in range(len(large_objects2[i])):
            if large_objects2[i][j] != 0:
                if not(large_objects2[i][j] in tab_jhj):
                    tab_m.append((large_objects2[i][j],image[i][j]))
                    tab_jhj.append(large_objects2[i][j])

    for i in range(len(final_objects)):
        for j in range(len(final_objects[i])):
            for k in tab_m:
                if final_objects[i][j] == k[0]:
                    final_objects[i][j] = k[1]
                    break

    return final_objects

def view_image(final_objects, image):
    image_finale = []
    for i in range(len(final_objects)):
        temp = []
        for j in range(len(final_objects[i])):
            match final_objects[i][j]:
                case 1:
                    temp.append([255,200,200])
                case 2:
                    temp.append([255,0,0])
                case 3:
                    temp.append([255,0,170])
                case 4:
                    temp.append([255,170,0])
                case 5:
                    temp.append([0,100,0])
                case 6:
                    temp.append([164,84,34])
                case 7:
                    temp.append([0,255,255])
                case 8:
                    temp.append([0,0,150])
                case 9:
                    temp.append([0,255,0])
                case 10:
                    temp.append([100,0,100])
                case _:
                    temp.append([255,255,255])
                    print(final_objects[i][j])
        image_finale.append(temp)

    image_finale = np.array(image_finale)

    image_original = []
    for i in range(len(image)):
        temp = []
        for j in range(len(image[i])):
            match image[i][j]:
                case 1:
                    temp.append([255,200,200])
                case 2:
                    temp.append([255,0,0])
                case 3:
                    temp.append([255,0,170])
                case 4:
                    temp.append([255,170,0])
                case 5:
                    temp.append([0,100,0])
                case 6:
                    temp.append([164,84,34])
                case 7:
                    temp.append([0,255,255])
                case 8:
                    temp.append([0,0,150])
                case 9:
                    temp.append([0,255,0])
                case 10:
                    temp.append([100,0,100])
                case _:
                    print(image[i][j])
        image_original.append(temp)

    image_original = np.array(image_original)

    labels = segmentation.slic(image_finale, compactness=30, n_segments=500, start_label=0, enforce_connectivity=False)

    ### affichage (pas utile)
    fig, ax = plt.subplots(1,2, sharex=True, sharey=True, figsize=(15, 10))
    ax[0].imshow(image_finale)
    ax[1].imshow(image_original)
    plt.tight_layout()
    plt.show()


def image_enhancement(name_file, size_col):
    image, tab_name_cluster = import_image(name_file, size_col)
    large_objects2, final_objects = delete_artifacts_from_image(image)
    final_objects = reconstitute_image(image,large_objects2,final_objects)

    view_image(final_objects,image)

    return final_objects, tab_name_cluster


def image_to_data(name_file, size_col):
    tab, tab_name_cluster = image_enhancement(name_file, size_col)

    labels, num = skimage.measure.label(tab, background=-1, return_num= True, connectivity=2)
    regions = skimage.measure.regionprops(labels)

    return tab, regions, tab_name_cluster


def extract_zone(kml_file, plu_file):
    tab_extracted_area = []
    label_of_zone = []

    df = pd.read_json(plu_file)

    df['coordinates'] = df['geo_shape'].apply(lambda x: x['geometry']['coordinates'])

    # df_5000 = df.loc[df['echelle'] == '1/2000']
    coords = extract_coordinates(kml_file)
    polygon_image = Polygon(coords)
    #######
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(15, 10))


    # for i in df_5000.index:
    for i in df.index:
        liste_coords = df["coordinates"][i]
        liste_coords = liste_coords[0]

        polygon_temp = Polygon(liste_coords)
        x = polygon_temp.intersection(polygon_image)

        if(x):
            tab_extracted_area.append(liste_coords)
            label_of_zone.append(df["type"][i])
            ### afichage (inutile)
            ax.plot(*polygon_temp.exterior.xy, color='blue')

    ### afichage (inutile)
    ax.plot(*polygon_image.exterior.xy, color='red')
    plt.show()



    return tab_extracted_area, label_of_zone

def detect_obj_in_zone(zone, region, big_tab, tab_obj):

    poly = Polygon(zone)
    res = []
    for i in range(len(region)):
        for j in region[i].coords:
            p = Point(big_tab[j[0]][j[1]])
            if(p.covered_by(poly)):
                res.append(tab_obj[i])
                break

    return res


def instantiation_ontologie(kml_file, plu_file, name_file, nb_col, nb_ligne):
    coords_point = extract_coordinates(kml_file)

    y, a, x, b = calcul_droite(coords_point[0],coords_point[3])
    tabb1 = calcul_point_droite(a, x, b, coords_point[0], coords_point[3], nb_ligne)

    y, a, x, b = calcul_droite(coords_point[1],coords_point[2])
    tabb2 = calcul_point_droite(a, x, b, coords_point[1], coords_point[2], nb_ligne)

    big_tab = []

    for i in range(len(tabb1)):
        y, a, x, b = calcul_droite(tabb1[i],tabb2[i])
        tabbx = calcul_point_droite(a, x, b, tabb1[i], tabb2[i], nb_col)
        big_tab.append(tabbx)

    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()

    with onto:
        tab, regions, tab_name_cluster = image_to_data(name_file, nb_col)

        k = 0
        k2 = 0
        tab_obj = []
        for i in range(len(regions)):
            px_tab = []

            str_state = "State_jardin_" + str(k2)

            for j in range(len(regions[i].coords)):
                str_pixel = "Px_" + str(k)
                x = int(regions[i].coords[j][0])
                y = int(regions[i].coords[j][1])
                val = tab[x][y]
                # px = onto.Pixel(str_pixel, hasPostitionX = [big_tab[x][y][0]], hasPostitionY = [big_tab[x][y][1]], hasValueClust = [int(val)])
                # px_tab.append(px)
                k = k+1

            final_type = tab_name_cluster[val-1]
            jardin = fonctionF(final_type, str_state, onto)

            str_obj = "obj_" + str(k2)
            obj1 = onto.Object_Geo(str_obj, has_pixels = px_tab, Candidate_Final_State = [jardin])
            tab_obj.append(obj1)
            k2 = k2+1


        tab_extracted_area, label_of_zone = extract_zone(kml_file, plu_file)
        # print("je suis :", tab_extracted_area, len(tab_extracted_area))
        tab_of_zone = []
        for i in range(len(tab_extracted_area)):
            name_zone = "zone_" + label_of_zone[i]+ "_" + str(i)
            list_link_zone = detect_obj_in_zone(tab_extracted_area[i], regions, big_tab, tab_obj)

            match label_of_zone[i]:
                case "A1":
                    z = onto.ZoneA1(name_zone, contains_object = list_link_zone)
                case _:
                    z = onto.ZoneArticle1(name_zone, contains_object = list_link_zone)

            tab_of_zone.append(z)
            
        img_1 = onto.Image("Img", composed_by = tab_obj)
        img_2 = onto.Image("Img2", has_rules= tab_of_zone)


        # t1 = onto.Valid_Time("t1")
        # Bati_indu = onto.Zone_industrielle_commerciale_ou_tertiaire("bati_industrielle", has_time = t1)
        # bati_act = onto.Bati_activite("bati_act", has_time = t1)
        # EA_1 = onto.Espaces_agricoles("EA_1", has_time = t1)
        # V1 = onto.Vigne("Vigne_1", has_time = t1)
        # C1 = onto.Canal("Canal_2", has_time = t1)
        # inc = onto.Inconnu("inc_1", has_time = t1)

        # # Pixel
        # px1 = onto.Pixel("Px_1", has_state = [Bati_indu])
        # px2 = onto.Pixel("Px_2", has_state = [V1])
        # px3 = onto.Pixel("Px_3", has_state = [EA_1])
        # px4 = onto.Pixel("Px_4", has_state = [C1])
        # # Object
        # obj1 = onto.Object_Geo("obj_1", has_pixels = [px1], has_state = [Bati_indu], Candidate_Final_State = [Bati_indu])
        # obj2 = onto.Object_Geo("obj_2", has_pixels = [px2], has_state = [V1], Candidate_Final_State = [V1])
        # obj3 = onto.Object_Geo("obj_3", has_pixels = [px3], has_state = [Bati_indu], Candidate_Final_State = [inc])
        # obj4 = onto.Object_Geo("obj_4", has_pixels = [px4], has_state = [C1], Candidate_Final_State = [C1])

        # ### Zone
        # z1 = onto.ZoneArticle1("zone_1", z_has_pixels = [px1], contains_object = [obj1])
        # z2 = onto.ZoneEA("zone_2", z_has_pixels = [px1, px2], contains_object = [obj1, obj2])
        # z3 = onto.ZoneEA("zone_3", z_has_pixels = [px3, px4], contains_object = [obj3, obj4])

        # ### Image creation :
        # img_1 = onto.Image("Img", composed_by = [obj1, obj2, obj3, obj4])
        # img_2 = onto.Image("Img2", has_rules= [z1, z2])

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