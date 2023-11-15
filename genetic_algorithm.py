import random


class Individual:
    def __init__(self, size, mines):
        # If size is an integer (square board), store it as a tuple (size, size)
        if isinstance(size, int):
            self.size = (size, size)
        else:
            self.size = size  # Assuming size is already a tuple
        self.flags = set()  # Initialize flags
        self.initialize_random_flags()  # Call this method to place flags


    def initialize_random_flags(self):
        # Determine the number of flags to place
        num_flags = random.randint(5, self.size[0])  # Use the first element of the tuple for row size

        while len(self.flags) < num_flags:
            row = random.randint(0, self.size[0] - 1)
            col = random.randint(0, self.size[1] - 1)
            self.flags.add((row, col))

    def __str__(self):
        """
        String representation of the individual's flagged positions.
        """
        return f"Flags: {self.flags}"



    """
    def print_board_with_flags(minesweeper_logic, individual):
        print("Minesweeper Board with Flags:")
        for row in range():
            row_str = ''
            for col in range(size):
                cell = minesweeper_logic.board[row][col]
                celltype = cell.get_type()

                if (row, col) in individual.flags:
                    row_str += 'F '  # Flagged cell
                elif celltype == 'mine':
                    row_str += 'M '  # Mine
                elif cell.adjacent_mines > 0:
                    row_str += f'{cell.adjacent_mines} '  # Adjacent mines
                else:
                    row_str += 'E '  # Empty cell
            print(row_str)
        print()
    """
    
    def calculate_fitness(self,individual, minesweeper_logic):
        """
        Calculate the fitness of an individual based on the Minesweeper board.

        :param individual: The individual to be evaluated.
        :param minesweeper_board: The Minesweeper board (with bomb locations).
        :return: The fitness score of the individual.
        """
        correct_flags = 0
        correct_opens = 0

        for row in range(self.size):
            for col in range(self.size):
                cell = minesweeper_logic.board[row][col]
                celltype = (cell).get_type()
                if celltype == "mine" and (row, col) in individual.flags:
                    correct_flags += 1
                elif not celltype == "mine" and (row, col) not in individual.flags:
                    correct_opens += 1

        return correct_flags * 20 + correct_opens 


    def mutate(self,individual, mutation_rate):
        """
        Mutate an individual by randomly redistributing a percentage of its flags.

        :param individual: The individual to be mutated.
        :param mutation_rate: The fraction of flags to be redistributed.
        """
        rows, cols = individual.size
        num_flags_to_mutate = int(len(individual.flags) * mutation_rate)

        # Convert the set of flags to a list for random sampling
        flags_list = list(individual.flags)

        # Randomly select a number of flags to remove
        if len(flags_list) >= num_flags_to_mutate:
            flags_to_remove = random.sample(flags_list, num_flags_to_mutate)
        else:
            flags_to_remove = flags_list.copy()

        # Remove the selected flags from the individual
        for flag in flags_to_remove:
            individual.flags.discard(flag)

        # Add new random flags
        while len(flags_to_remove) > 0:
            new_row = random.randint(0, rows - 1)
            new_col = random.randint(0, cols - 1)
            new_flag = (new_row, new_col)
            if new_flag not in individual.flags:
                individual.flags.add(new_flag)
                flags_to_remove.pop()  # Remove one flag from the list

        return individual


    def crossover(self,parent1, parent2):
        # Create deep copies of the parent individuals to become the offspring
        offspring1 = Individual(parent1.size)
        offspring1.flags = parent1.flags.copy()
        offspring2 = Individual(parent2.size)
        offspring2.flags = parent2.flags.copy()

        # Ensure there are flags to swap
        if len(offspring1.flags) > 0 and len(offspring2.flags) > 0:
            # Determine the crossover point (number of flags to swap)
            crossover_point = random.randint(1, min(len(offspring1.flags), len(offspring2.flags)))

            # Convert the sets of flags to lists for random sampling
            flags_list1 = list(offspring1.flags)
            flags_list2 = list(offspring2.flags)

            # Select flags from each parent to swap
            flags_to_swap1 = random.sample(flags_list1, crossover_point)
            flags_to_swap2 = random.sample(flags_list2, crossover_point)

            # Perform the swap
            offspring1.flags.difference_update(flags_to_swap1)
            offspring1.flags.update(flags_to_swap2)

            offspring2.flags.difference_update(flags_to_swap2)
            offspring2.flags.update(flags_to_swap1)

        return offspring1, offspring2

    def tournament_selection(self,population, tournament_size):
        """
        Select individuals from the population using tournament selection.

        :param population: The current population of individuals.
        :param tournament_size: The number of individuals to be included in each tournament.
        :return: Selected individuals for the next generation.
        """
        selected_individuals = []

        while len(selected_individuals) < len(population):
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda individual: individual.fitness)
            selected_individuals.append(winner)

        return selected_individuals


    def aggregate_wisdom_of_crowds(self,population):
        # Select the best 5% of individuals
        top_individuals = sorted(population, key=lambda ind: ind.fitness, reverse=True)[:max(1, len(population) // 20)]

        # Aggregate flags from top individuals
        aggregated_flags = set()
        for individual in top_individuals:
            aggregated_flags.update(individual.flags)

        # Create a new individual with aggregated flags
        aggregated_individual = Individual(population[0].size)
        aggregated_individual.flags = aggregated_flags
        
        return aggregated_individual


    def genetic_algorithm(self, selfminesweeper_logic, population_size, generations, tournament_size, mutation_rate):
        # Initialize the population
        population = [Individual(self.size) for _ in range(population_size)]

        """
        for i, individual in enumerate(population):
            print(f"Individual {i}:")
            print_board_with_flags(minesweeper_logic, individual)
            # You can limit the number of printed boards if the population is large
            if i >= 5:  # Change this number as needed
                break
        """
        
        # Evaluate the initial population
        for individual in population:
            individual.fitness = self.calculate_fitness(individual, self.minesweeper_logic)

        for generation in range(generations):
            # Selection
            selected_individuals = self.tournament_selection(population, tournament_size)

            # Crossover and Mutation
            next_generation = []
            while len(next_generation) < population_size:
                parent1, parent2 = random.sample(selected_individuals, 2)
                offspring1, offspring2 = self.crossover(parent1, parent2)
                next_generation.extend([self.mutate(offspring1, mutation_rate), self.mutate(offspring2, mutation_rate)])

            # Evaluate the new generation
            for individual in next_generation:
                individual.fitness = self.calculate_fitness(individual, self.minesweeper_logic)
                
            aggregated_individual = self.aggregate_wisdom_of_crowds(population)
            aggregated_individual.fitness = self.calculate_fitness(aggregated_individual, self.minesweeper_logic)
            population[-1] = aggregated_individual  # Replace the least fit individual

            # Replace the old population with the new generation
            population = next_generation

            # Optional: Store the most fit individual or perform other analyses

        # Return the best solution found
        best_solution = max(population, key=lambda individual: individual.fitness)
        
        return best_solution

"""
# Choose a difficulty level
difficulty = "Beginner"  # Example: "Beginner", "Intermediate", "Expert"


# Retrieve grid size and number of mines from config
grid_size = config.DIFFICULTIES[difficulty]["size"]
num_mines = config.DIFFICULTIES[difficulty]["mines"]

# Initialize the MinesweeperLogic with the specific game settings
minesweeper_logic = MinesweeperLogic(grid_size, num_mines)
minesweeper_logic.initialize_mines()

print("Initial Board State:")
minesweeper_logic.print_board()

# GA parameters
population_size = 500
generations = 500
tournament_size = 20
mutation_rate = 0.3

# Running the genetic algorithm
best_solution = genetic_algorithm(minesweeper_logic, population_size, generations, tournament_size, mutation_rate)
print("Best solution found:", best_solution)

print("Final Solution Board:")
print_board_with_flags(minesweeper_logic, best_solution)"""