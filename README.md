# Stage

# Tester la consistance d'une ontologie avec Java

## Dossier reasonner_java

- Vérifier qu'il existe une ontologie dans **src/main/resources** (fichier **onto_herelles.owl**)
- Vérifier que tout les requierments sont installer (pas encore fait, mais un Requierments.txt sera fait)
- Vérifier qu'il existe le fichier **pom.xml**

### Compiler (avec maven)
```bash
- mvn package
```
### Exécuter
```bash
- java -jar target/my-project-1.0-SNAPSHOT-jar-with-dependencies.jar
```

# Créer - Instancier - Tester - Corriger une ontologie

## Dossier reasonner_java

- Vérifier bien qu'il existe le dossier **CEO2**, **src** et les 5 fichiers .py :
    - **main**
    - **create_onto**
    - **instantiation_onto**
    - **test_inconsistance**
    - **compute_counterfactual**

### Exécuter le code
```bash
- python3 main.py
```
#### Dans le terminal
- Choisissez les correctifs via le terminal pour chaque objet lorsque cela vous est demandé.
- Il existe les types `Inconnu` et `Ignorer`, `Inconnu` créera automatiquement des inconsistance qu'il faudra corriger. Cependant, si vous ne souhaitez pas affirmer le type d'un objet, vous pouvez simplement mettre le correctif `Ignorer` (en mettant son numéro dans les correctifs proposés).