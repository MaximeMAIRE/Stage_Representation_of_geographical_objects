from owlready2 import *
import pandas as pd
import skimage
import numpy as np
import xml.etree.ElementTree as ET

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point


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


def image_to_data(name_file, size_col):
    tree = ET.parse(name_file)
    root = tree.getroot()
    tab_test = []
    tab = []
    nb_cluster = 0
    for i in root:
        if (i.tag == 'classes'):
            for j in i:
                nb_cluster = nb_cluster +1
        elif (i.tag == 'values'):
            for k in range(len(i)) :
                tab_test.append(i[k].text)
                if((k+1) % size_col == 0) :
                    tab.append(tab_test)
                    tab_test = []
    tab = np.array(tab)
    labels, num = skimage.measure.label(tab, background=-1, return_num= True, connectivity=2)
    regions = skimage.measure.regionprops(labels)

    return tab, regions


def extract_zone(kml_file, plu_file):
    tab_extracted_area = []
    
    df = pd.read_json(plu_file)

    df['coordinates'] = df['geo_shape'].apply(lambda x: x['geometry']['coordinates'])

    df_5000 = df.loc[df['echelle'] == '1/2000']
    coords = extract_coordinates(kml_file)
    polygon_image = Polygon(coords)

    for i in df_5000.index:
        liste_coords = df["coordinates"][i]
        liste_coords = liste_coords[0]

        polygon_temp = Polygon(liste_coords)
        x = polygon_temp.intersection(polygon_image)
        if(x):
            tab_extracted_area.append(liste_coords)

    return tab_extracted_area

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

def instantiation_ontologie():
    kml_file = 'result.kml'
    plu_file = 'plu_decoupage.json'

    coords_point = extract_coordinates(kml_file)

    y, a, x, b = calcul_droite(coords_point[0],coords_point[3])
    tabb1 = calcul_point_droite(a, x, b, coords_point[0], coords_point[3], 180)

    y, a, x, b = calcul_droite(coords_point[1],coords_point[2])
    tabb2 = calcul_point_droite(a, x, b, coords_point[1], coords_point[2], 180)

    big_tab = []

    for i in range(len(tabb1)):
        y, a, x, b = calcul_droite(tabb1[i],tabb2[i])
        tabbx = calcul_point_droite(a, x, b, tabb1[i], tabb2[i], 140)
        big_tab.append(tabbx)

    onto = get_ontology("./src/main/resources/onto_herelles.owl").load()

    with onto:
        tab, regions = image_to_data("fodomust_clusturing.xml", 140)

        k = 0
        k2 = 0
        tab_obj = []
        for i in range(len(regions)):
            px_tab = []

            str_state = "State_jardin" + str(k2)
            
            if(i == 38) | (i ==108):
                jardin = onto.Zone_industrielle_commerciale_ou_tertiaire(str_state)
            else:
                jardin = onto.Jardin(str_state)

            for j in range(len(regions[i].coords)):
                str_pixel = "Px_" + str(k)
                x = int(regions[i].coords[j][0])
                y = int(regions[i].coords[j][1])
                val = tab[x][y]
                # px = onto.Pixel(str_pixel, hasPostitionX = [big_tab[x][y][0]], hasPostitionY = [big_tab[x][y][1]], hasValueClust = [int(val)])
                # px_tab.append(px)
                k = k+1

            str_obj = "obj_" + str(k2)
            obj1 = onto.Object_Geo(str_obj, has_pixels = px_tab, Candidate_Final_State = [jardin])
            tab_obj.append(obj1)
            k2 = k2+1


        tab_extracted_area = extract_zone(kml_file, plu_file)
        print("je suis :", tab_extracted_area, len(tab_extracted_area))
        tab_of_zone = []
        for i in range(len(tab_extracted_area)):
            name_zone = "zone_" + str(i)
            list_link_zone = detect_obj_in_zone(tab_extracted_area[i], regions, big_tab, tab_obj)
            if(i == 4):
                z = onto.ZoneSA(name_zone, contains_object = list_link_zone)
            else:
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