import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.OWLReasonerRuntimeException;
import org.semanticweb.owlapi.reasoner.SimpleConfiguration;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;
import java.util.List;
import java.util.ArrayList;

import org.semanticweb.HermiT.Reasoner.ReasonerFactory;

import java.io.InputStream;
import java.util.Set;

public class Test {
    public void loadOntology() throws OWLOntologyCreationException {
        OWLOntologyManager om = OWLManager.createOWLOntologyManager();
        InputStream inputStream = getClass().getResourceAsStream("/onto_herelles.owl");
        OWLOntology onto = om.loadOntologyFromOntologyDocument(inputStream);
        checkConsistencyAndInfer(onto);
    }

    public void checkConsistencyAndInfer(OWLOntology ontology) {
        OWLReasonerFactory reasonerFactory = new ReasonerFactory();
        OWLReasoner reasoner = reasonerFactory.createReasoner(ontology);


        if (reasoner.isConsistent()) {
            System.out.println("L'ontologie est cohérente.");

            /*
            Ca ne donne que les axiomes qui existent deja dans l'ontologie, je souhaite récuperer les axiomes inferrer
            sans avoir les aximes de base.
            */

            //Pas de doublons dans les Set :
            //Set<OWLClassAssertionAxiom> inferredAxioms = ontology.getAxioms(AxiomType.CLASS_ASSERTION);
            //peut avor des doublons dans les listes :
            List<OWLClassAssertionAxiom> inferredAxioms = new ArrayList<>(ontology.getAxioms(AxiomType.CLASS_ASSERTION));

            for (OWLClassAssertionAxiom axiom : inferredAxioms) {
                System.out.println("Inferred axiom: " + axiom);
            }
            printSubclassesAndInstance(reasoner);
        } else {
            System.out.println("L'ontologie est inconsistante. Voici les instances à l'origine de cette inconsistence :");
            printInconsistentInstances(reasoner);
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
