# AI-Based Planner Implementation

## Overview
This project involves implementing a general-purpose AI planner, showcasing different algorithms for planning and heuristic functions. The primary focus is on solving specified problems using state-space search methods. The project covers both backward and forward state-space search, and it incorporates heuristic strategies to optimize the process.

## Objectives
- Implement a general-purpose AI planner.
- Execute the planner on provided domains and print the results.
- Incorporate and implement the following elements:
  - **Backward State-Space Search**
  - **Forward State-Space Search**
  - **Ignore Preconditions Heuristic**
  - **Ignore Delete Lists Heuristic**

## Details of Implementation
### Planner
- Implement a comprehensive planner capable of handling both backward and forward state-space searches.
- Develop heuristic methods to improve the efficiency of the forward state-space search.
- Output the solution and compute the time taken to solve the problem.

### Heuristics
- **Ignore Preconditions Heuristic**: Simplifies the problem by overlooking preconditions during state evaluations.
- **Ignore Delete Lists Heuristic**: Focuses on goal achievement without considering delete effects.

### Domains to Model
The project requires modeling and running the planner on the following domains:
1. **Spare Tire Domain**: Refer to pages 370 (3rd edition) and 364 (4th edition) of the specified textbook.
2. **Blocks World Domain**: Consult the same page references as the Spare Tire domain for more details.
3. **Monkey and Bananas Domain**: Refer to the provided link for additional resources.
4. **Dinner-Date Domain**: Check the article referenced on pages 3 to 5 for detailed information.
5. **Link-Repeat Domain**: Define actions and states using the format \( A_i \) with preconditions and effects as outlined.

## Requirements
- Ensure compliance with the PDDL (Planning Domain Definition Language) conventions while modeling the problems.

## Resources
- [STRIPS Planning Guide](http://idm-lab.org/intro-to-ai/supplements/strips.pdf)
- [AI Planning Magazine Article](https://ojs.aaai.org/index.php/aimagazine/article/download/1459/1358%20PDF)

## License
This project is open-source and available under the MIT License.
