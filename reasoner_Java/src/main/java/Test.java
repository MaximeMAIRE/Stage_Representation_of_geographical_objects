import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.SimpleConfiguration;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;

import org.semanticweb.HermiT.Reasoner.ReasonerFactory;

import java.io.InputStream;

public class Test {
    public void loadOntology() throws OWLOntologyCreationException {
        OWLOntologyManager om = OWLManager.createOWLOntologyManager();
        InputStream inputStream = getClass().getResourceAsStream("/onto_herelles.owl");
        OWLOntology pressInnovOntology = om.loadOntologyFromOntologyDocument(inputStream);
        checkConsistencyAndInfer(pressInnovOntology);
    }

    public void checkConsistencyAndInfer(OWLOntology ontology) {
        OWLReasonerFactory reasonerFactory = new ReasonerFactory();
        OWLReasonerConfiguration config = new SimpleConfiguration();
        OWLReasoner reasoner = reasonerFactory.createReasoner(ontology, config);

        try {
            reasoner.precomputeInferences();
            System.out.println("L'ontologie est cohérente.");

            for (OWLClass cls : ontology.getClassesInSignature()) {
                NodeSet<OWLClass> subClasses = reasoner.getSubClasses(cls, true);
                for (Node<OWLClass> subClassNode : subClasses) {
                    for (OWLClass subClass : subClassNode.getEntities()) {
                        System.out.println("Classe " + cls.getIRI().getShortForm() + " a pour sous-classe : " + subClass.getIRI().getShortForm());
                    }
                }
            }
        } catch (OWLRuntimeException e) {
            System.err.println(e.getMessage());
        }

        
        // for (OWLClass cls : ontology.getClassesInSignature()) {
        //     if (!reasoner.isSatisfiable(cls)) {
        //         System.out.println("Classe incohérente : " + cls.getIRI().getShortForm());
        //     }
        // }
        // System.out.println("Inférences :");


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