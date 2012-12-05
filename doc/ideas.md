<h1>Analysis of the GA approach to solving the TSP</h1>

[TBI] = TO BE IMPLEMENTED

<h2>General Guidelines</h2>

Whenever we measure the influence of one parameter we shall:
-Average over 10 to 30 runs. (The rationale must be explained in the report).
-Evaluate the progression of the different algorithms in terms of fitness evolution vs cpu_time AND fitness_evolution vs generations (this is necessary to cope with the fact that some algorithms attain good results faster in terms of generations BUT might take longer time to compute e.g ERX takes long!)

<h2>Representations</h2>

-Compare adjacent representation [TBI] vs path representation
I propose to drop adjacent representation after this and just explain that we are more interested in the influence of crossover, mutation etc (Note: look up in the book the reasons why adjacent representation is no good and use that in the report).

<h2>Parent Selection Comparison</h2>

<li>Try roulette wheel (toolbox)</li>
<li>Boltzman tournament (modify the T parameter) [TBI]</li>
<li>k,q tournament (see session 3 of exercises) Remember to do runs with limit values then progress e.g K=1 to K = 20 or more [TBI]</li>

For each method measure the improvements when playing with the corresponding parameters AND measure the impact of the elitism! (ok?)

I propose to measure the influence of parent selection fixing OX crossover and no mutation. (Any better idea Hugo?)

I think after this we could fix the parent comparison values

<h2>Crossover (no Mutation)</h2>
<li>PMX</li>
<li>OX</li>
<li>ERX</li>
<li>SCX[TBI]</li>

Individually: Check the influence of any adjustable parameters if any.
Together: compare which one performs better for same parameters

<h2>Mutation</h2>

Without any crossover
<li>simple inversion</li>
<li>inversion</li>
<li>insertion</li>
<li>index shuffling</li>

Individually: Check the influence of any adjustable parameters, mainly the probability of mutation.
-loop removal? Can we add this on top of other operators and evaluate it separately?

Together: compare which one performs better for same parameters

<h2>Mutation Combined with crossover</h2>

Combine all Crossover with all mutations (I propose to do this with the parameters around the optimal parameters already found) find out about best combination (fix the parent selection)

Find out the overall combination. 