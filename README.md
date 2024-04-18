# Stage

## reasoner_java :

### fait :
- Affichage de toutes les instances, avec leur(s) type(s) et leur(s) propriété(s), lorsque l'ontologie est consistante.

### à faire :
- Si l'ontologie est incohérente, afficher le/les raisonnements qui ont amené a une incohérence.

### Modifications :
- Afficher seulement ce qui inferred, et pas ce qui est asserted (ontologie consistante).


## Tester reasoner_java

### Complier :
- mvn package

### Executer :
- java -jar target/my-project-1.0-SNAPSHOT-jar-with-dependencies.jar

## Fichier - Projet :
Le fichier onto_test.ipynb appelle le code java pour les explications et le code CEO (venant du git CEO), pour récupérer les potentielles corrections.
Ne pas oublier de restart le kernel jupyter avant chaque "run all"
