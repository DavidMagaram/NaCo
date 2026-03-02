## Applying insights:

  Must-do

  ~~1. Add an explicit research question in the introduction.
  Something like: "How do obstacles affect the collective
  migration behaviour of cells in a Cellular Potts Model?" Then
  echo it in the conclusion.~~
  2. Add the Hamiltonian equation (ΔH) and the activity
  constraint equation. Put these in a short "Model" subsection
  at the start of Methodology, or in the Introduction when you
  introduce the CPM.
  3. Add references. At minimum: Graner & Glazier (1992) for the
   CPM, and the Artistoo paper/framework. Add a \bibliography or
   \begin{thebibliography} section.
  4. Report the Vicsek order parameter. You mention computing it
   in the methods (line 114) but never show it. Either add a
  column/row to your tables or a separate small table, and
  discuss what it shows about alignment. This directly addresses
   the feedback form question about alignment being disrupted by
   obstacles.
  5. Justify the choice of Max_act=60. Add a sentence in
  Methodology explaining that Max_act=20 (from ex 1.3) produced
  stationary clusters without persistent migration, so you
  increased it to 60 which successfully reproduced collective
  migration with sustained directional movement.
  6. Justify why you use a CPM — one or two sentences in the
  introduction (e.g., CPMs capture cell shape, adhesion, and
  motility on a lattice, making them suitable for studying
  collective migration).
  7. Add timestamps to figure captions — state at which MCS each
   row of screenshots was taken (e.g., "Top row: MCS 500,
  middle: MCS 1000, bottom: MCS 2000").

  Should-do

  8. Add a graph plotting average speed (or distance) vs. number
   of obstacles, with both parameter series as separate lines.
  This is much more readable than the tables alone for showing
  the trend.
  9. Separate observations from interpretations in the Results
  section. State what you measured first ("Average speed
  decreased from X to Y"), then interpret ("This suggests
  that...").
  10. Explicitly discuss alignment disruption. When presenting
  Vicsek data, note that without obstacles cells align in a
  shared direction, and that obstacles progressively disturb
  this alignment.
  11. Acknowledge stochasticity more explicitly in the
  Discussion — you ran each condition once, so the quantitative
  values are single-run estimates. Say this clearly as a
  limitation.

  Cleanup

  12. Fix "Quantative" → "Quantitative" (line 137)
  13. Fix Table 3 caption: "Speed distance" → "Speed and
  distance"
  14. Remove duplicate \usepackage{booktabs} and
  \usepackage{subcaption} (lines 13/17 and 12/17)
  15. Remove the commented-out table (lines 81–102)
  16. Remove the empty \begin{appendices}\end{appendices} block,
   or move the figures inside it
  17. Fix duplicate \label names (e.g., fig:img1g used twice) —
  these cause broken cross-references
  18. Add a period at end of the Discussion paragraph (line 203)
  19. Move figures to before \end{document} and inside the
  appendix if you want them there, or remove the appendix
  wrapper entirely


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