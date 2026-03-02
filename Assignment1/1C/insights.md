## Insights from feedback:
* Research question / Hypothesis (answer this in the conclusion)
* Baseline - Use 0 obstacles
* Report metric for all obstacle configurations (quantitative data)
* Clear Results and Conclusion sections (Clearly compare 0 obstacles with other obstacle configurations)
* Tweak parameters (*add more cells* so we can observe collective cell migration, change ACT to get the cells moving more (should be 80 and not 20??), more Monte Carlo steps...)
* Chaotic results. Screnshots + videos did not align (not the same setup). Figure titles, videos, links, and descriptions at the wrong place. Some misspecifications...
* Cite original paper of CPM

## Maybe:
* Motivation for the number of cells and obstacles?
* Table with parameters
* Try and keep it 3-4 pages
* Let it run longer???

## Pros
* Metrics
* Good overall report
* Visualizations - look good, clear, there are many

## Inspirations from other people's papers!

* We should include relevant equations
* a graph showing how speed changes with number of cells & obstacles
* We should probably have a table with all chosen parameters and justify the important ones
* We need a proper research question that is posed and answered
* > Does the answer mention the alignment of directions in the scenario without obstacles, which is disturbed when obstacles are present? I don't think ours does
* Implement Migration of cells: the correct choice was maxact=80; see ex 1.3
* > Is it clear which statements are factual observations (“the cells did X in context Y”) and which are interpretations thereof (“these findings suggest that obstacles do X”)? I don't think we really do that either
* > Are the methods described sufficiently well that you could reproduce the work without looking at the code? This means the report should include:
    • All the relevant parameters used, including the temperature T and boundary conditions
    • If adhesion values J are given in a matrix, it should be clear which celltypes are in the rows and columns;
    • Densities of cells and obstacles (or numbers, but then the size of the simulation field should be included) No
* Are there any other reasons why results may not be reproducible? Yes
* Group 2: Interesting equations for basic things like max_act and delta H
* Group 2: Ideal parameter overview of the obstacles and cells
* Group 2 has a very good overall paper already! Good to copy from hehe.
* Group 16: Display Speed of cells over time across different experiments.
* We should probably justify why we use a CPM in the first place
* Lecture: After some X density of cells, they all start moving in the same direction (flock/swarm behavior in cell migration).