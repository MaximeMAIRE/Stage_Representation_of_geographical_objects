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
import java.util.Set;
import org.semanticweb.owlapi.reasoner.ConsoleProgressMonitor;
import org.semanticweb.owl.explanation.impl.blackbox.checker.InconsistentOntologyExplanationGeneratorFactory;
import uk.ac.manchester.cs.owl.owlapi.OWLDataFactoryImpl;
import org.semanticweb.HermiT.ReasonerFactory;

public class Test {
    public void loadOntology() throws OWLOntologyCreationException {
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        OWLDataFactory dataFactory = manager.getOWLDataFactory();
        OWLDataFactory dataFactoryImpl = new OWLDataFactoryImpl();
        InputStream inputStream = getClass().getResourceAsStream("/onto_herelles.owl");
        OWLOntology onto = manager.loadOntologyFromOntologyDocument(inputStream);

        checkConsistencyAndInfer(onto, manager, dataFactory);
    }

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

    private void printInconsistentExplanation(OWLReasonerFactory reasonerFactory, OWLDataFactory df, OWLOntologyManager manager, OWLReasoner reasoner, OWLOntology ontology) {
        try{
            ExplanationGenerator<OWLAxiom> explainInconsistency = new InconsistentOntologyExplanationGeneratorFactory(reasonerFactory, df, () -> manager, 1000L).createExplanationGenerator(ontology);
            System.out.println(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()));
            Set<Explanation<OWLAxiom>> explanations = explainInconsistency.getExplanations(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()));
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
    

    public static void main(String[] args) {
        Test test = new Test();
        try {
            test.loadOntology();
        } catch (OWLOntologyCreationException e) {
            e.printStackTrace();
        }
    }
}
