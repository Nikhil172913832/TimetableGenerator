# genetic_algorithm.py
import random
from entities import Timetable

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, generations, batches, teachers, classrooms, time_slots):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.batches = batches
        self.teachers = teachers
        self.classrooms = classrooms
        self.time_slots = time_slots
        self.population = []

    def initialize_population(self):
        for _ in range(self.population_size):
            timetable = Timetable(self.batches, self.teachers, self.classrooms, self.time_slots)
            timetable.initialize_random()
            timetable.calculate_fitness()
            self.population.append(timetable)

    def evaluate_population(self):
        for timetable in self.population:
            timetable.calculate_fitness()

    def select_parents(self, tournament_size=3):
        parents = []
        for _ in range(2):
            tournament = random.sample(self.population, tournament_size)
            parent = max(tournament, key=lambda t: t.fitness)
            parents.append(parent)
        return parents

    def crossover(self, parent1, parent2):
        child1 = Timetable(self.batches, self.teachers, self.classrooms, self.time_slots)
        child2 = Timetable(self.batches, self.teachers, self.classrooms, self.time_slots)

        for key in parent1.schedule.keys():
            if random.random() < 0.5:
                child1.schedule[key] = parent1.schedule[key]
                child2.schedule[key] = parent2.schedule[key]
            else:
                child1.schedule[key] = parent2.schedule[key]
                child2.schedule[key] = parent1.schedule[key]

        return child1, child2

    def mutate(self, timetable):
        for key in timetable.schedule.keys():
            if random.random() < self.mutation_rate:
               
                new_time_slot = random.randint(0, self.time_slots - 1)
                timetable.schedule[key]['time_slot'] = new_time_slot

                
                subject = key[1]
                timetable.schedule[key]['teacher'] = timetable.get_teacher_for_subject(subject, new_time_slot)
                timetable.schedule[key]['classroom'] = timetable.get_available_classroom(
                    next(b.size for b in timetable.batches if b.batch_id == key[0]),
                    new_time_slot
                )

    def evolve(self):
        self.initialize_population()

        for generation in range(self.generations):
            print(f"Generation {generation + 1}")
            self.evaluate_population()

          
            self.population.sort(key=lambda t: t.fitness, reverse=True)

            
            next_generation = self.population[:int(0.1 * self.population_size)]

       
            while len(next_generation) < self.population_size:
                parent1, parent2 = self.select_parents()
                if random.random() < self.crossover_rate:
                    offspring1, offspring2 = self.crossover(parent1, parent2)
                else:
                    offspring1 = parent1
                    offspring2 = parent2

                self.mutate(offspring1)
                self.mutate(offspring2)

                offspring1.calculate_fitness()
                offspring2.calculate_fitness()

                next_generation.extend([offspring1, offspring2])

            self.population = next_generation[:self.population_size]

            best_fitness = self.population[0].fitness
            print(f"Best Fitness: {best_fitness}")
            if best_fitness == 0:
                print("Optimal timetable found.")
                break


        best_timetable = max(self.population, key=lambda t: t.fitness)
        return best_timetable
