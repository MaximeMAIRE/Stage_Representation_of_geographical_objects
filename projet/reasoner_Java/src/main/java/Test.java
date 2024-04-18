import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.SimpleConfiguration;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.NodeSet;
import org.semanticweb.owl.explanation.api.Explanation;
import org.semanticweb.owl.explanation.api.ExplanationException;
import org.semanticweb.owl.explanation.api.ExplanationGenerator;
import java.io.InputStream;
import java.lang.reflect.Array;

import org.semanticweb.owlapi.reasoner.ConsoleProgressMonitor;
import org.semanticweb.owl.explanation.impl.blackbox.checker.InconsistentOntologyExplanationGeneratorFactory;
import org.semanticweb.HermiT.ReasonerFactory;
import java.util.*;

/*Peut etre utiliser JFactFactory pour determiner les axioms qui sont inferer.
 * Il suffit de faire la difference entre le JFactFactory et ReasonerFactory.
 * Car JFactFactory ne peux pas inferer des valeurs, contrairement a ReasonerFactory.
 * Donc {Axioms ReasonerFactory} - {Axioms JFactFactory} = {Axioms infered}
 */

public class Test {
    /**
     * Load the ontology and call the function checkConsistencyAndInfer.
     * 
     * @return Nothing.
     */
    public void loadOntology() throws OWLOntologyCreationException {
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        OWLDataFactory dataFactory = manager.getOWLDataFactory();
        InputStream inputStream = getClass().getResourceAsStream("/onto_herelles.owl");
        OWLOntology onto = manager.loadOntologyFromOntologyDocument(inputStream);
        checkConsistencyAndInfer(onto, manager, dataFactory);
    }

    /**
     * Check if the ontology is consistant or not. If ontology is not it call the function 
     * printInconsistentExplanation, else it call the function printConsistantOntology.
     * 
     * @param ontology
     * @param manager Manger of the ontology to check.
     * @param df DataFactory, an interface for creating entities, class expressions and axioms.
     * 
     * @return Nothing.
     */
    public void checkConsistencyAndInfer(OWLOntology ontology, OWLOntologyManager manager, OWLDataFactory df) {
        OWLReasonerFactory reasonerFactory = new ReasonerFactory();
        ConsoleProgressMonitor cpm = new ConsoleProgressMonitor();
        OWLReasonerConfiguration config = new SimpleConfiguration(cpm);
        OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);

        if (reasoner.isConsistent()) {
            printConsistantOntology(reasoner, ontology);
        } else {
            printInconsistentExplanation(reasonerFactory, df, manager, reasoner, ontology);
        }
        reasoner.dispose();
    }
    /**
     * Print all axioms of the ontology, and each instance with their data properties.
     * 
     * @param reasoner Reasoner of the ontology, to infered some value.
     * @param ontology 
     * 
     * @return Nothing
     */
    private void printConsistantOntology(OWLReasoner reasoner, OWLOntology ontology) {
        for (OWLAxiom axiom : ontology.getAxioms()) {
            System.out.println(axiom);
        }
        System.out.println("L'ontologie est cohérente.");
        Set<OWLNamedIndividual> individuals = ontology.getIndividualsInSignature();
        Set<OWLObjectProperty> objProperties = ontology.getObjectPropertiesInSignature();
        for (OWLNamedIndividual individual : individuals) {
            System.out.println("\n\n\nINDIVIDU : "+ individual);
            Set<OWLClass> types = reasoner.getTypes(individual, false).getFlattened();
            if (!types.isEmpty()) {
                System.out.println("L'individu " + individual + " a les types suivants : " + types);
            }
            for(OWLObjectProperty objProperty : objProperties){
                NodeSet<OWLNamedIndividual> obj_prop = reasoner.getObjectPropertyValues(individual, objProperty);
                if(!obj_prop.isEmpty()){
                    System.out.println("L'individu " + individual + " a les props : " + obj_prop);    
                }
            }
        }
    }
    /**
     * Create a list of string of unique axioms and return it.
     * 
     * @param explanations a set of explanation
     * 
     * @return List of string of unique axioms.
     */
    private List<String> createListAxiom(Set<Explanation<OWLAxiom>> explanations){
        List<String> listAxiom = new ArrayList<>();
        if (explanations != null && !explanations.isEmpty()){
            for (Explanation<OWLAxiom> explanation : explanations){
                for (OWLAxiom axiom : explanation.getAxioms()){
                    String s = new String(axiom.toString());
                    if (!listAxiom.contains(s)){
                        listAxiom.add(s);
                    }
                }
            }
        }
        return listAxiom;
    }

    /**
     * Create, init and return a tab of int.
     * 
     * @param i size of the table.
     * 
     * @return tab of int equals to 0.
     */
    private int[] createTabOccurenceAxioms(int i){
        int [] intArray = new int[i];
        for (int nb : intArray){
            nb = 0;
        }
        return intArray;
    }
    /**
     * Compute the number of occurence of each unique axiom in every explanation. 
     * 
     * @param listAxiom a list of unique axiom.
     * @param intArray a table which represent the occurence of axiom.
     * @param explanations
     * 
     * @return Nothing
     */
    private void computeOccurenceAxiom(List<String> listAxiom, int[] intArray, Set<Explanation<OWLAxiom>> explanations){
        int i = 0;
        for(String s : listAxiom){
            for (Explanation<OWLAxiom> explanation : explanations){
                for (OWLAxiom axiom : explanation.getAxioms()){
                    if (axiom.toString().contains(s)){
                        intArray[i] = intArray[i]+1;
                    }
                }   
            }
            i = i+1;
        }
    }

    /**
     * Print all axioms, with their occurence.
     * 
     * @param listAxiom
     * @param intArray
     * 
     * @return Nothing
     */
    private void printAxiom(List<String> listAxiom, int[] intArray){
        int i = 0;
        for(String s : listAxiom){
            System.out.println(s + "  " +intArray[i]);
            i = i+1;
        }
    }

    /**
     * Print axioms which are in every explanations.
     * 
     * @param listAxiom
     * @param intArray
     * 
     * @return Nothing
     */
    private void printUniversalAxiom(List<String> listAxiom, int[] intArray){
        int i = 0;
        for(String s : listAxiom){
            if(intArray[i] == listAxiom.size()){
                System.out.println("Axiome : " + s);
            }
            i = i+1;
        }
    }

    /**
     * Return a list of Object_Geo and Zone who does not respect rule of the ontology.
     * 
     * @param listAxiom
     * 
     * @return list of Object_Geo and Zone who does not respect rule of the ontology.
     */
    private List<String> DetectionIndividualInconsistant(List<String> listAxiom){
        List<String> listObject = new ArrayList<>();
        for(String s : listAxiom){
            String[] list1 = new String[]{};
            if (s.contains("contains_object") && !s.contains("EquivalentClasses")){
                s = s.replace("http://test.org/onto_herelles.owl#","");
                s = s.replace("<","");
                s = s.replace(">","");
                s = s.replace("contains_object","");
                s = s.replace("ObjectPropertyAssertion","");
                s = s.replace("(","");
                s = s.replace(")","");
                list1 = s.split(" ");
            }
            for (String s2 : list1){
                if (!listObject.contains(s2)){
                    listObject.add(s2);
                }
            }
        }
        return listObject;
    }

    /**
     * Print all explanation of everything who are inconsistent.
     * 
     * @param reasonerFactory
     * @param df
     * @param manager
     * @param reasoner
     * @param ontology
     * 
     * @return Nothing
     */
    private void printInconsistentExplanation(OWLReasonerFactory reasonerFactory, OWLDataFactory df, OWLOntologyManager manager, OWLReasoner reasoner, OWLOntology ontology) {
        try{
            ExplanationGenerator<OWLAxiom> explainInconsistency = new InconsistentOntologyExplanationGeneratorFactory(reasonerFactory, df, () -> manager, 1000L).createExplanationGenerator(ontology);
            // System.out.println(df.getOWLClass("http://test.org/onto_herelles.owl#obj_1"));
            System.out.println(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()));
           
            Set<Explanation<OWLAxiom>> explanations = explainInconsistency.getExplanations(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()),100 );
            int x = 1;
            if (explanations != null && !explanations.isEmpty()){
                for (Explanation<OWLAxiom> explanation : explanations){
                    System.out.println("\n\n\nExplanatin number : " + x + "\n");
                    for (OWLAxiom axiom : explanation.getAxioms()){
                        System.out.println("Axiom :" + axiom);
                    }
                    x = x + 1;
                }
            }

            // ici on affiche les axiomes qui sont dans toutes les explications:
            System.out.println("\n\nExplications universelles :");
            List<String> listAxiom = createListAxiom(explanations);
            int[] intArray = createTabOccurenceAxioms(listAxiom.size());
            computeOccurenceAxiom(listAxiom, intArray, explanations);
            // printAxiom(listAxiom, intArray);

            // System.out.println("ICI SONT LES AXIOMS APPARTENANT A TOUS LES EXPLICATIONS :\n");
            // printUniversalAxiom(listAxiom, intArray);
            
            List<String> listObject = DetectionIndividualInconsistant(listAxiom);

            System.out.println("\n\nObjects inconsistants :");
            for (String s2 : listObject){
                System.out.println(s2);
            }

        } catch(ExplanationException e){
            System.out.println("Erreur lors de la recuperation de l'explication pour l'inconsistance de l'ontologie.\nErreur : " + e);
        }
    }

    public static void main(String[] args) {
        Test test = new Test();
        try {
            test.loadOntology();
        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }
    }
}
