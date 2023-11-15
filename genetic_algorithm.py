import random

class Individual:
    def __init__(self, size):
        self.size = size  # settings size of the baord in both x,y directions to passed size param
        self.num_mines = mines
        self.flags = set()  # Initialize flags
        self.population_size = 500
        self.generations = 500
        self.tournament_size = 20
        self.mutation_rate = 0.3
        
        self.improvement = []
        
        self.initialize_random_flags()  # Call this method to place flags

    def initialize_random_flags(self):
        # Determine the number of flags to place
        num_flags = random.randint(5, self.size)  # Use the first element of the tuple for row size

        while len(self.flags) < num_flags:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size -1)
            self.flags.add((row, col))

    def __str__(self):
        """
        String representation of the individual's flagged positions.
        """
        return f"Flags: {self.flags}"

    def print_board_with_flags(self):
        print("Minesweeper Board with Flags:")
        for row in range(self.size):
            row_str = ''
            for col in range(self.size):
                cell = self.board[row][col]
                celltype = cell.get_type()

                if (row, col) in self.flags:
                    row_str += 'F '  # Flagged cell
                elif celltype == 'mine':
                    row_str += 'M '  # Mine
                elif cell.adjacent_mines > 0:
                    row_str += f'{cell.adjacent_mines} '  # Adjacent mines
                else:
                    row_str += 'E '  # Empty cell
            print(row_str)
        print()
        
    def calculate_fitness(self, individual):
        """
        Calculate the fitness of an individual based on the Minesweeper board.

        :param individual: The individual to be evaluated.
        :param minesweeper_board: The Minesweeper board (with bomb locations).
        :return: The fitness score of the individual.
        """
        correct_flags = 0
        incorrect_flags = 0
        correct_opens = 0
        incorrect_opens = 0
        

        for row in range(self.size):
            for col in range(self.size):
                cell = self.board[row][col]
                celltype = cell.get_type()
                is_flagged = (row, col) in individual.flags

                if celltype == "mine":
                    if is_flagged:
                        correct_flags += 1
                    else:
                        incorrect_opens += 1  # Missed mine
                else:
                    if is_flagged:
                        incorrect_flags += 1
                    else:
                        correct_opens += 1

        return correct_flags * 20 + correct_opens 

    def mutate(self, individual, mutation_rate):
        rows, cols = self.size, self.size
        num_flags_to_mutate = int(len(individual.flags) * mutation_rate)

        # Convert the set of flags to a list for random sampling
        flags_list = list(individual.flags)
        flags_to_remove = random.sample(flags_list, min(num_flags_to_mutate, len(flags_list)))

        individual.flags.difference_update(flags_to_remove)

        # Add new random flags until the total count is back to num_mines
        while len(individual.flags) < self.num_mines:
            new_row = random.randint(0, rows - 1)
            new_col = random.randint(0, cols - 1)
            individual.flags.add((new_row, new_col))

        return individual


    def crossover(self, parent1, parent2):
        # Create offspring with a combined set of flags from both parents
        offspring1 = Individual(parent1.size, self.num_mines)
        offspring2 = Individual(parent2.size, self.num_mines)

        # Combine flags from both parents and then randomly redistribute
        combined_flags = parent1.flags.union(parent2.flags)
        shuffled_flags = list(combined_flags)
        random.shuffle(shuffled_flags)

        # Distribute the flags between the offspring
        half = len(shuffled_flags) // 2
        offspring1.flags = set(shuffled_flags[:half])
        offspring2.flags = set(shuffled_flags[half:])

        # Ensure both offspring have the correct number of flags
        self.adjust_flag_count(offspring1)
        self.adjust_flag_count(offspring2)

        return offspring1, offspring2

    def tournament_selection(self, population, tournament_size):
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

    def genetic_algorithm(self, board):
        # Initialize the population
        population = [Individual(self.size, self.num_mines) for _ in range(self.population_size)]

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
            individual.fitness = self.calculate_fitness(individual, board)

        for generation in range(self.generations):
            # Selection
            selected_individuals = self.tournament_selection(population, self.tournament_size)

            # Crossover and Mutation
            next_generation = []
            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(selected_individuals, 2)
                offspring1, offspring2 = self.crossover(parent1, parent2)
                next_generation.extend([self.mutate(offspring1, board, self.num_mines, self.size), self.mutate(offspring2, board, self.num_mines, self.size)])

            # Evaluate the new generation
            for individual in next_generation:
                individual.fitness = self.calculate_fitness(individual, board)
                
                
            aggregated_individual = self.aggregate_wisdom_of_crowds(population)
            aggregated_individual.fitness = self.calculate_fitness(aggregated_individual, board)
            population[-1] = aggregated_individual  # Replace the least fit individual

            # Replace the old population with the new generation
            population = next_generation
            self.improvement.append(max(population, key=lambda individual: individual.fitness).fitness)

        # Return the best solution found
        best_solution = max(population, key=lambda individual: individual.fitness)
        
        return best_solution