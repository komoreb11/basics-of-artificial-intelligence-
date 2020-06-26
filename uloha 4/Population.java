package bi.zum.lab3;

import cz.cvut.fit.zum.api.ga.AbstractEvolution;
import cz.cvut.fit.zum.api.ga.AbstractIndividual;
import cz.cvut.fit.zum.api.ga.AbstractPopulation;
import cz.cvut.fit.zum.data.StateSpace;
import cz.cvut.fit.zum.util.Pair;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Collections;
import java.util.Comparator;

/**
 * @author Your name
 */
public class Population extends AbstractPopulation {

    public Population(AbstractEvolution evolution, int size) {
        individuals = new Individual[size];
        for (int i = 0; i < individuals.length; i++) {
            individuals[i] = new Individual(evolution, true);
            individuals[i].computeFitness();
        }
    }
    /*
    public int compare(final Pair<Integer, Double> o1, final Pair<Integer, Double> o2) {
        return Double.compare(o1.b, o2.b);
    }
    */

    /**
     * Method to select individuals from population
     *
     * @param count The number of individuals to be selected
     * @return List of selected individuals
     */
    public List<AbstractIndividual> selectIndividuals(int count) {
        ArrayList<AbstractIndividual> selected = new ArrayList<AbstractIndividual>();

        // example of random selection of N individuals
        /*
        AbstractIndividual individual = individuals[r.nextInt(individuals.length)];
        while (selected.size() < count) {
            selected.add(individual);
            individual = individuals[r.nextInt(individuals.length)];
        }
        */

        // TODO: implement your own (and better) method of selection
        for(int i = 0; i < count; ++i) {
            double bestFitness = -1.0D / 0.0;
            AbstractIndividual winner = null;
            Random r = new Random();
            for(int k = 0; k < 10; ++k) {
                AbstractIndividual candidate = this.individuals[r.nextInt(this.individuals.length)];
                if (candidate.getFitness() > bestFitness) {
                    winner = candidate;
                    bestFitness = candidate.getFitness();
                }
            }

            selected.add(winner);
        }

       /*
        ArrayList < Pair <Integer, Double> > all = new ArrayList<Pair <Integer, Double>>();
        double sumFitness = 0;
        for(int k = 0; k < this.individuals.length; ++k) {
                AbstractIndividual candidate = this.individuals[k];
                Pair <Integer, Double> p = new Pair<Integer, Double>();
                p.a = k;
                sumFitness+=candidate.getFitness();
                p.b = candidate.getFitness();
                all.add(p);
        }
        for(Pair<Integer, Double> c : all) {
            c.b/=sumFitness;
            c.b*= 1000;
        }
        all.sort(new Comparator<Pair<Integer, Double>>() {
        @Override
        public int compare(Pair<Integer, Double> p1, Pair<Integer, Double> p2) {
            return Double.compare(p2.b, p1.b);
        }
        });
        if(this.selected != null)
        while(count > this.selected.size()){
            for(int k = 0; k < all.size(); ++k){
                Boolean f = false;
                for(int id : this.selected){
                    if (all.get(k).a == id){
                        f = true;
                        break;
                    }
                }
                if(!f){
                    selected.add(this.individuals[all.get(k).a]);
                    this.selected.add(all.get(k).a);
                }
            }
        }
        */
        return selected;
    }
}
