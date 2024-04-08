import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.OWLReasonerRuntimeException;
import org.semanticweb.owlapi.reasoner.InconsistentOntologyException;
import org.semanticweb.owlapi.reasoner.InferenceType;
import org.semanticweb.owlapi.reasoner.SimpleConfiguration;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.NodeSet;

import org.semanticweb.owl.explanation.api.Explanation;
import org.semanticweb.owl.explanation.api.ExplanationException;
import org.semanticweb.owl.explanation.api.ExplanationGenerator;
import java.io.InputStream;
import java.util.Set;
import org.semanticweb.owlapi.reasoner.ConsoleProgressMonitor;
import org.semanticweb.owl.explanation.impl.blackbox.checker.InconsistentOntologyExplanationGeneratorFactory;

import uk.ac.manchester.cs.jfact.JFactFactory;


public class Test {
    public void loadOntology() throws OWLOntologyCreationException {
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        OWLDataFactory factory = manager.getOWLDataFactory();
        InputStream inputStream = getClass().getResourceAsStream("/onto_herelles.owl");
        OWLOntology onto = manager.loadOntologyFromOntologyDocument(inputStream);
        checkConsistencyAndInfer(onto, manager, factory);
    }

    public void checkConsistencyAndInfer(OWLOntology ontology, OWLOntologyManager manager, OWLDataFactory df) {
        OWLReasonerFactory reasonerFactory = new JFactFactory();

        ConsoleProgressMonitor cpm = new ConsoleProgressMonitor();
        OWLReasonerConfiguration config = new SimpleConfiguration(cpm);
        OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);    

        // try {
        //     Thread.sleep(5000);
        // } catch (InterruptedException e) {
        //     e.printStackTrace();
        // }
        //reasoner.precomputeInferences(InferenceType.DATA_PROPERTY_ASSERTIONS);


        if (reasoner.isConsistent()) {
            System.out.println("L'ontologie est cohérente.");
            Set<OWLClassAssertionAxiom> inferredAxioms = ontology.getAxioms(AxiomType.CLASS_ASSERTION);
            for (OWLClassAssertionAxiom axiom : inferredAxioms) {
                System.out.println("Inferred axiom: " + axiom);
            }
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
            //printSubclassesAndInstance(reasoner);
        } else {
            try{
                ExplanationGenerator<OWLAxiom> explainInconsistency = new InconsistentOntologyExplanationGeneratorFactory(reasonerFactory, df, () -> manager, 1000L).createExplanationGenerator(ontology);
                System.out.println(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()));
                Set<Explanation<OWLAxiom>> explanations = explainInconsistency.getExplanations(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()), 100);
                int x = 1;
                if (explanations != null && !explanations.isEmpty()){
                    for (Explanation<OWLAxiom> explanation : explanations){
                        System.out.println("Explanatin number : " + x);
                        for (OWLAxiom axiom : explanation.getAxioms()){
                            System.out.println("Axiom :" + axiom + "\n");
                        }
                        x = x + 1;
                    }
                }
            } catch(ExplanationException e){
                System.out.println("Erreur lors de la recuperation de l'explication pour l'inconsistance de l'ontologie.\nErreur : " + e);
            }
        }
        reasoner.dispose();
    }

    private void printSubclassesAndInstance(OWLReasoner reasoner) {
        // A voir plus tard
    }

    private void printInconsistentInstances(OWLReasoner reasoner) {
        // A voir plus tard
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
