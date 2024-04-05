import org.semanticweb.owlapi.reasoner.OWLReasoner;
import org.semanticweb.owlapi.reasoner.OWLReasonerFactory;
import org.semanticweb.owlapi.reasoner.OWLReasonerConfiguration;
import org.semanticweb.owlapi.reasoner.OWLReasonerRuntimeException;
import org.semanticweb.owlapi.reasoner.InconsistentOntologyException;
import org.semanticweb.owlapi.reasoner.SimpleConfiguration;
import org.semanticweb.owlapi.reasoner.structural.StructuralReasonerFactory;
import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.Node;
import org.semanticweb.owlapi.reasoner.NodeSet;

import org.semanticweb.owl.explanation.api.Explanation;
import org.semanticweb.owl.explanation.api.ExplanationException;
import org.semanticweb.owl.explanation.api.ExplanationGenerator;
import java.io.InputStream;
import java.util.Set;
import org.semanticweb.owlapi.reasoner.ConsoleProgressMonitor;
import java.io.File;

import org.semanticweb.owl.explanation.impl.blackbox.checker.InconsistentOntologyExplanationGeneratorFactory;

import uk.ac.manchester.cs.jfact.JFactFactory;
import org.semanticweb.owlapi.model.OWLOntologyManager;

import org.semanticweb.HermiT.Reasoner.ReasonerFactory;
import com.clarkparsia.owlapi.explanation.DefaultExplanationGenerator;
import com.clarkparsia.owlapi.explanation.util.ExplanationProgressMonitor;
import com.clarkparsia.owlapi.explanation.util.*;
import com.clarkparsia.owlapi.explanation.MultipleExplanationGenerator;
import com.clarkparsia.owlapi.explanation.BlackBoxExplanation;
import org.semanticweb.owl.explanation.impl.blackbox.*;

import java.util.List;
import java.util.ArrayList;


public class Test {
    public void loadOntology() throws OWLOntologyCreationException {
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        OWLDataFactory factory = manager.getOWLDataFactory();
        InputStream inputStream = getClass().getResourceAsStream("/onto_herelles.owl");
        OWLOntology onto = manager.loadOntologyFromOntologyDocument(inputStream);
        checkConsistencyAndInfer(onto, manager, factory);
    }

    public void checkConsistencyAndInfer(OWLOntology ontology, OWLOntologyManager manager, OWLDataFactory df) {
        // OWLReasonerFactory reasonerFactory = new StructuralReasonerFactory();
        // OWLReasonerFactory reasonerFactory = new ReasonerFactory();
        OWLReasonerFactory reasonerFactory = new JFactFactory();

        ConsoleProgressMonitor cpm = new ConsoleProgressMonitor();
        OWLReasonerConfiguration config = new SimpleConfiguration(cpm);
        OWLReasoner reasoner = reasonerFactory.createReasoner(ontology,config);
        // BlackBoxExplanation explanationGenerator = new BlackBoxExplanation(ontology, reasonerFactory, reasoner);
        
        
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
                ExplanationGenerator<OWLAxiom> explainInconsistency = new InconsistentOntologyExplanationGeneratorFactory(reasonerFactory, 1000L).createExplanationGenerator(ontology);
                System.out.println(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()));
                Set<Explanation<OWLAxiom>> explanations = explainInconsistency.getExplanations(df.getOWLSubClassOfAxiom(df.getOWLThing(), df.getOWLNothing()));
                System.out.println("TestExplanation.main() " + explanations);
            } catch(ExplanationException e){
                System.out.println("Erreur lors de la recuperation de l'explication pour l'inconsistance de l'ontologie.\nErreur : " + e);
            }
            // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // Ne m affiche absolument rien...
            // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // try {
            //     Set<OWLAxiom> explanation2 = explanationGenerator.getExplanation(ontology.getOWLOntologyManager().getOWLDataFactory().getOWLThing());
                
            //     System.out.println("Explication pour l'inconsistance de l'ontologie :");
            //     for (OWLAxiom axiom : explanation2) {
            //         System.out.println(axiom);
            //     }
            // } catch (InconsistentOntologyException e) {
            //     System.out.println("Erreur lors de la recuperation de l'explication pour l'inconsistance de l'ontologie.\nErreur : " + e);
            // }
            // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
            // ICI je créé une nouvvelle onto contenant tous les axioms de l ontologie de base qui est inconsistante
            // Pour une raison qui m echappe, la nouvelle ontologie est consistante
            // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // boolean inconsistentAxiomFound = false;
            // for (OWLAxiom axiom : ontology.getAxioms()) {
            //     OWLOntologyManager tempManager = OWLManager.createOWLOntologyManager();
            //     try {
            //         OWLOntology tempOntology = tempManager.createOntology();
            //         tempManager.addAxiom(tempOntology, axiom);
            //         System.out.println("Axiom ajouté à l'ontologie temporaire : " + axiom);
            //         OWLReasoner tempReasoner = reasonerFactory.createReasoner(tempOntology, config);
            //         if (!tempReasoner.isConsistent()) {
            //             System.out.println("Axiom inconsistant trouvé : " + axiom);
            //             inconsistentAxiomFound = true;
            //         }
            //         tempReasoner.dispose();
            //     } catch (OWLOntologyCreationException e) {
            //         System.err.println("Erreur lors de la création de l'ontologie temporaire : " + e.getMessage());
            //     }
            // }
            // if (!inconsistentAxiomFound) {
            //     System.out.println("Aucun axiome inconsistant trouvé dans l'ontologie.");
            // }
            /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

            /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            

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
