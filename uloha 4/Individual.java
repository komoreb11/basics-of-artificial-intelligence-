package bi.zum.lab3;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import cz.cvut.fit.zum.data.Edge;
import cz.cvut.fit.zum.data.StateSpace;
import cz.cvut.fit.zum.util.Pair;
import java.util.concurrent.ThreadLocalRandom;


import java.util.Iterator;
import java.util.List;
import java.util.Random;


/**
 * @author Your Name
 */
public class Individual extends AbstractIndividual {

    private double fitness = 0.0D / 0.0;
    private AbstractEvolution evolution;
    public boolean[] genome;

    
    // @TODO Declare your genotype
    

    /**
     * Creates a new individual
     * 
     * @param evolution The evolution object
     * @param randomInit <code>true</code> if the individual should be
     * initialized randomly (we do wish to initialize if we copy the individual)
     */
    public Individual(AbstractEvolution evolution, boolean randomInit) {
        this.evolution = evolution;
        Random random = new Random();
        this.genome = new boolean[evolution.getNodesCount()];
        if (randomInit) {
            for(int i = 0; i < evolution.getNodesCount(); i++) {
                this.genome[i] = random.nextBoolean();
            }

            this.repair();
        }

    }

    @Override
    public boolean isNodeSelected(int j) {
        
        // @TODO Implement based on your individual's genotype
        return this.genome[j];
    }

    /**
     * Evaluate the value of the fitness function for the individual. After
     * the fitness is computed, the <code>getFitness</code> may be called
     * repeatedly, saving computation time.
     */
    @Override
    public void computeFitness() {
        
        
        // @TODO: Implement fitness based on your implementation
        // Hint: use the StateSpace object
        double result = (double)StateSpace.nodesCount();

        for(int i = 0; i < this.genome.length; ++i) {
            if (this.genome[i]) {
                --result;
            }
        }

        this.fitness = result;
    }
    
    public int score(AbstractIndividual other){
        int sc = 0;
        int i =0;
        Individual oth = (Individual)other;
        for(Boolean a: this.genome)
            if(a && oth.genome[i])
                sc++;
            i++;
        return sc;
    }
    
    /**
     * Only return the computed fitness value
     *
     * @return value of fitness function
     */
    @Override
    public double getFitness() {
        return this.fitness;
    }

    /**
     * Does random changes in the individual's genotype, taking mutation
     * probability into account.
     * 
     * @param mutationRate Probability of a bit being inverted, i.e. a node
     * being added to/removed from the vertex cover.
     */
    @Override
    public void mutate(double mutationRate) {
        
        
        // TODO: Implement mutation of the genotype

        for(int i = 0; i < this.genome.length; ++i) {
            Random random = new Random();
            if (2*random.nextDouble() < mutationRate) {
                this.genome[i] = !this.genome[i];
            }
        }

        this.repair();
        
        
    }
    
    /**
     * Crosses the current individual over with other individual given as a
     * parameter, yielding a pair of offsprings.
     * 
     * @param other The other individual to be crossed over with
     * @return A couple of offspring individuals
     */
    @Override
    public Pair crossover(AbstractIndividual other) {

        Pair<Individual,Individual> result = new Pair();

        // @TODO implement your own crossover
        Random r = new Random();
        int p1 = r.nextInt(this.genome.length);
        int p2 = ThreadLocalRandom.current().nextInt(p1, this.genome.length);
        Individual o1 = new Individual(this.evolution, false);
        Individual o2 = new Individual(this.evolution, false);
        
        int i;
        for(i = 0; i < p1; ++i) {
            o1.genome[i] = this.genome[i];
            o2.genome[i] = other.isNodeSelected(i);
        }
        
        for(i = p1; i < p2; ++i){
            o1.genome[i] = other.isNodeSelected(i);
            o2.genome[i] = this.genome[i];
        }

        for(i = p2; i < this.genome.length; ++i) {
            o1.genome[i] = this.genome[i];
            o2.genome[i] = other.isNodeSelected(i);
        }
        
        
        o1.repair();
        o2.repair();
        result.a = o1;
        result.b = o2;
        
        return result;
    }

    
    /**
     * When you are changing an individual (eg. at crossover) you probably don't
     * want to affect the old one (you don't want to destruct it). So you have
     * to implement "deep copy" of this object.
     *
     * @return identical individual
     */
    @Override
    public Individual deepCopy() {
        Individual newOne = new Individual(evolution, false);
       

        // TODO: at least you should copy your representation of search-space state

        // for primitive types int, double, ...
        // newOne.val = this.val;

        // for objects (String, ...)
        // for your own objects you have to implement clone (override original inherited from Objcet)
        // newOne.infoObj = thi.infoObj.clone();

        // for arrays and collections (ArrayList, int[], Node[]...)
        /*
         // new array of the same length
         newOne.pole = new MyObjects[this.pole.length];		
         // clone all items
         for (int i = 0; i < this.pole.length; i++) {
         newOne.pole[i] = this.pole[i].clone(); // object
         // in case of array of primitive types - direct assign
         //newOne.pole[i] = this.pole[i]; 
         }
         // for collections -> make new instance and clone in for/foreach cycle all members from old to new
         */
        
        
        System.arraycopy(this.genome, 0, newOne.genome, 0, this.genome.length);
        newOne.fitness = this.fitness;
        return newOne;
    }

    private void repair() {
        for(Edge e: StateSpace.getEdges()){
            if(!this.genome[e.getFromId()] && !this.genome[e.getToId()] ){
            Random random = new Random();
            if(random.nextBoolean())
                this.genome[e.getFromId()] = true;
            else
                this.genome[e.getToId()] = true;
            }
        }
    }
    
    

    /**
     * Return a string representation of the individual.
     *
     * @return The string representing this object.
     */
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();

        boolean first = true;

        for(int i = 0; i < this.genome.length; ++i) {
            if (this.genome[i]) {
                if (first) {
                    first = false;
                } else {
                    sb.append(":");
                }

                sb.append(i);
            }
        }

        return sb.toString();
    }
}


