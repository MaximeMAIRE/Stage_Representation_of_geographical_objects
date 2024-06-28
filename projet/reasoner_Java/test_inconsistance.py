import subprocess
from owlready2 import *


def test_consistency():
    mvn_command = ['mvn', 'install']
    java_command = ['java', '-jar', 'target/my-project-1.0-SNAPSHOT-jar-with-dependencies.jar']

    try:
        subprocess.check_call(mvn_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)

    try:
        output = subprocess.check_output(java_command, stderr=subprocess.STDOUT).decode()
        print("Result :", output)
    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)

    if("COHERENTE" in output):
        return True, output
    else:
        return False, output
    
def clean_output_cons(txt):
    clean_output = txt.split("Objects inconsistants :")
    clean_output = clean_output[1].split("\n")
    clean_output = list(filter(None, clean_output))

    list_zone = []
    list_obj = []

    for i in clean_output:
        i = i.replace("ObjectPropertyAssertion(<http://test.org/onto_herelles.owl#contains_object> ","")
        i = i.replace("<http://test.org/onto_herelles.owl#","")
        i = i.replace(">","")
        i = i.replace("<","")
        i = i.replace(")","")
        i = i.split(" ")
        for j in i:
            if ("obj" in j): # | ("remblais" in j):
                if not(j in list_obj):
                    list_obj.append(j)
            else:
                list_zone.append(j)

    return list_zone, list_obj
