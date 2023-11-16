# Minesweeper: Genetic Algorithm and Wisdom of Crowds Solution

## Description
This project aims to leverage the power of genetic algorithms combined with the wisdom of crowds approach to solve minesweeper, which is a NP-complete problem. The genetic algorithm simulates natural evolutionary processes to iteratively improve solutions, while the wisdom of crowds approach aggregates diverse perspectives to enhance decision-making and predictions.

## Features
- **Genetic Algorithm Core**: Implements a robust genetic algorithm for optimization.
- **Crowd Wisdom Integration**: Harnesses crowd-sourced data/input to guide the evolutionary process.

## Getting Started

### Dependencies
```
et-xmlfile==1.1.0
openpyxl==3.1.2
```

### Installing
- Clone the repository: 
  ```
  git clone https://github.com/blakehourigan/Minesweeper_solver.git
  ```
- Install dependencies:
  ```
  pip install -r requirements.txt

  ```

### Executing Program
- There are two options to run the program:
  ```
  1) Navigate to project folder, manually execute main.py using python.
  2) Execute main.exe on a windows machine. 
  ```

## How It Works  
**Genetic Algorithm**  
  
*Class setup*
- Represents a solution to the randomly generated Minesweeper board.
- Randomly places flags, equal to the total number of mines, at the inception of each individual

*Mutation function*
- Introduces variability by first removing a random subset of flags within the individual then adding new flags preferentially to cells with mines surrounding them
- Ensures that the amount of flags that are removed and then added equals the total number of mines on the board

*Elitism*
- Guarantees that the best-performing individuals from the current generation are carried over directly to the next generation without being altered by crossover or mutation events
- These elites replace the least fit individuals in the newest generation


*Crossover function*  
  
- Mixes and matches characteristics from two parent individuals to generate new offspring which inherit a combination of flag positions 
- A crossover point is randomly selected to determine the amount of flags that will be swapped. Flags are then randomly selected from each offspring based on this crossover point and exchanged between the two

*Selection process*
- A tournament selection process was introduced in order to choose individuals which are more likely to produce better offspring for the next generation
- A subset of individuals is randomly chosen from the population and have their fitness values evaluated. After this, the most fit individual is selected as the winner, this is done until the population is filled with individuals that won each tournament 

**Wisdom of Crowds**  
  
*WOTC Function*  
- WOTC functionality focused on creating a new solution based on some of the best solutions in the current generation
- The top 5% of highest fitness individuals were selected and their flag positions were aggregated in order to make a better solution
- Flags which were placed by multiple of the top individuals were given precedent when passing on these flags to the new solution
- This new solution replaced the lowest fitness individual in the current generation and then passed on to the next generation


## Authors and Acknowledgment
- Blake Hourigan - Game logic implementation, GUI development
- Bricker Oxley - Genetic Algorithm / Wisdom of Crowds devloment
- Adam Van Zant - Genetic Algorithm / Wisdom of Crowds develoment, main author project paper
- Robert Walden


## License
This project is licensed under the MIT License - see LICENSE.txt for details.

## Project Future  
*Moving away from Genetic Algorithm approach*  

While genetic algorithms can be great for some applications, and are very useful and accurate for small problems, other methods will be explored to implement a more complete and accurate solution to every difficulty level, not just the beginner level.

## Contact
- Blake Hourigan - Blakehourigan.com
- Project Link: https://github.com/blakehourigan/Minesweeper_solver
