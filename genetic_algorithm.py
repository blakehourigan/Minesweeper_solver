import random

class Individual:
    def __init__(self, board, mines, size):
        self.flags = set()  # Initialize flags
        self.board = board
        self.num_mines = mines
        self.grid_size = size
        self.initialize_random_flags()  # Call this method to place flags


    def initialize_random_flags(self):
        # Determine the number of flags to place
        num_flags = self.num_mines  # Use the first element of the tuple for row size
        while len(self.flags) < num_flags:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.flags.add((row, col))

    def __str__(self):
        return f"Flags: {self.flags}"


    def print_board_with_flags(self, individual):
        RED = '\033[91m'  # ANSI escape code for red
        YELLOW = '\033[93m'  # ANSI escape code for yellow
        RESET = '\033[0m'  # ANSI escape code to reset color

        print("Minesweeper Board with Flags:")
        for row in range(self.grid_size):
            row_str = ''
            for col in range(self.grid_size):
                cell = self.board[row][col]
                celltype = cell.get_type()

                if (row, col) in individual.flags:
                    row_str += YELLOW + 'F ' + RESET  # Yellow Flagged cell
                elif celltype == 'mine':
                    row_str += RED + 'M ' + RESET  # Red Mine
                elif cell.adjacent_mines > 0:
                    row_str += f'{cell.adjacent_mines} '  # Adjacent mines
                else:
                    row_str += 'E '  # Empty cell
            print(row_str)
        print()


    def calculate_fitness(self,individual):
        correct_flags = 0
        incorrect_flags = 0
        correct_opens = 0
        incorrect_opens = 0
        total_mines = self.num_mines

        for row in range(self.grid_size):
            for col in range(self.grid_size):
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

        # Calculate fitness
        fitness = (correct_flags * 50) - (incorrect_flags * 10) + correct_opens - (incorrect_opens * 5)

        # Penalize solutions that over-flag
        total_flags = len(individual.flags)
        if total_flags > total_mines:
            fitness -= (total_flags - total_mines) * 15

        return fitness
    
    def maximum_fitness(self):
        fitness = (self.num_mines * 50)  + ((self.grid_size ** 2) - self.num_mines)

        return fitness


    def mutate(self,individual):
        rows, cols = individual.grid_size, individual.grid_size
        total_mines = self.num_mines

        flags_list = list(individual.flags)

        # Remove a random number of flags
        num_flags_to_remove = random.randint(1, len(flags_list) // 2)
        flags_to_remove = random.sample(flags_list, num_flags_to_remove)
        for flag in flags_to_remove:
            individual.flags.discard(flag)

        # Add new flags, prioritizing cells near numbers
        potential_flags = []
        for row in range(rows):
            for col in range(cols):
                cell = self.board[row][col]
                if (row, col) not in individual.flags:
                    # Check if the cell is adjacent to a number
                    if self.is_adjacent_to_number(row, col):
                        potential_flags.append((row, col))

        # If there are not enough potential flags near numbers, consider all unflagged cells
        if len(potential_flags) < num_flags_to_remove:
            potential_flags.extend([(r, c) for r in range(rows) for c in range(cols) if (r, c) not in individual.flags and (r, c) not in potential_flags])

        # Randomly add flags up to the limit of total mines
        while len(individual.flags) < total_mines:
            new_flag = random.choice(potential_flags)
            individual.flags.add(new_flag)
            potential_flags.remove(new_flag)
            if new_flag not in individual.flags:
                individual.flags.add(new_flag)


    def is_adjacent_to_number(self,row, col):
        for r in range(max(0, row - 1), min(row + 2, self.grid_size)):
            for c in range(max(0, col - 1), min(col + 2, self.grid_size)):
                if self.board[r][c].get_type() != 'mine' and self.board[r][c].adjacent_mines > 0:
                    return True
        return False


    def crossover(self, parent1, parent2):
        # Create deep copies of the parent individuals to become the offspring
        offspring1 = Individual(self.board, self.num_mines, self.grid_size)
        offspring1.flags = parent1.flags.copy()
        offspring2 = Individual(self.board, self.num_mines, self.grid_size)
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


    def tournament_selection(self, population, tournament_size):
        selected_individuals = []

        while len(selected_individuals) < len(population):
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda individual: individual.fitness)
            selected_individuals.append(winner)

        return selected_individuals


    def aggregate_wisdom_of_crowds(self, population):
        # Select the best 5% of individuals
        top_individuals = sorted(population, key=lambda ind: ind.fitness, reverse=True)[:max(1, len(population) // 20)]

        # Aggregate flags from top individuals
        aggregated_flags = set()
        for individual in top_individuals:
            aggregated_flags.update(individual.flags)

        # Create a new individual with aggregated flags
        aggregated_individual = Individual(self.board, self.num_mines, population[0].grid_size)
        aggregated_individual.flags = aggregated_flags
        
        return aggregated_individual


    def genetic_algorithm(self, population_size, generations, tournament_size, mutation_rate, crossover_rate, total_mines, elitism_count):
        # Initialize the population

        population = [Individual(self.board, self.num_mines, self.grid_size) for _ in range(population_size)]

        # Evaluate the initial population
        for individual in population:
            individual.fitness = self.calculate_fitness(individual)

        best_fitness_per_generation = []
        
        for generation in range(generations):
            # Selection
            selected_individuals = self.tournament_selection(population, tournament_size)

            # Crossover
            next_generation = []
            while len(next_generation) < population_size:
                if random.random() < crossover_rate:  # Crossover occurs with a probability of crossover_rate
                    parent1, parent2 = random.sample(selected_individuals, 2)
                    offspring1, offspring2 = self.crossover(parent1, parent2)
                    next_generation.extend([offspring1, offspring2])
                else:
                    next_generation.extend(random.sample(selected_individuals, 2))  # Directly select individuals without crossover
                    
            # Mutation
            for individual in next_generation:
                if random.random() < mutation_rate:  # Mutation occurs with a probability of mutation_rate
                    self.mutate(individual)

            elites = sorted(population, key=lambda ind: ind.fitness, reverse=True)[:elitism_count]

            # Evaluate the new generation
            for individual in next_generation:
                while len(individual.flags) < total_mines:
                    # Add flags if any are missing
                    row = random.randint(0, individual.grid_size - 1)
                    col = random.randint(0, individual.grid_size - 1)
                    individual.flags.add((row, col))

                individual.fitness = self.calculate_fitness(individual)
                
            aggregated_individual = self.aggregate_wisdom_of_crowds(population)
            aggregated_individual.fitness = self.calculate_fitness(aggregated_individual)
            population[-20] = aggregated_individual  # Replace the least fit individual

            # Replace the old population with the new generation
            population = next_generation
            
            population[-elitism_count:] = elites

            best_fitness = max(individual.fitness for individual in population)
            best_fitness_per_generation.append(best_fitness)
            
        # Return the best solution found
        best_solution = max(population, key=lambda individual: individual.fitness)
        
        return max(population, key=lambda ind: ind.fitness), best_fitness_per_generation

    def run_multiple_ga_iterations(self, iterations, population_size, generations, tournament_size, mutation_rate, crossover_rate, total_mines, elitism_count):
        solutions = []
        for _ in range(iterations):
            solution, fitness_history = self.genetic_algorithm(population_size, generations, tournament_size, mutation_rate, crossover_rate, total_mines, elitism_count)
            solutions.append(solution)
            # Additional code for GIF creation goes here
        return solutions
