
from collections import defaultdict

from math import radians, cos, sin, asin, sqrt

import random


POPULATION_SIZE = 250

GENES = "01"


def reproduce(population, limit_planes, budgets, budget):
	
	new_generation = []
	temp_cost = 0
	s = POPULATION_SIZE
	percentile_90 = int(s*9/10)
	mean = 0
	list = []
	count = 0
	temp = int(population[len(population)-1].fitness)
	while(1):
		temp = temp / 10
		if(temp < 20):
			break
		count += 1
	divide_num = 10**count
	for j in range(percentile_90):
		list.extend([s-j-1] * int(int(population[s-j-1].fitness) / divide_num)**2)
	if not list:
		return list
	for i in range(percentile_90):
		choice1 = random.choice(list)
		choice2 = random.choice(list)
		parent1 = population[choice1]
		parent2 = population[choice2]
		child = parent1.mate(parent2, limit_planes, budgets, i, budget)
		new_generation.append(child)
	new_generation.extend(population[-(s-percentile_90):])

	return new_generation


def haversine(lon1, lat1, lon2, lat2):
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
	c = 2 * asin(sqrt(a))
	r = 6371
	return c * r


def check_fitness(gnome):

	total = 0
	count = 0
	for i in range(len(gnome)):
		for j in range(len(gnome[i])):
			dist = haversine(float(airports[gnome[i][j][0]][2]), float(airports[gnome[i][j][0]][1]), float(airports[gnome[i][j][1]][2]), float(airports[gnome[i][j][1]][1]))
			if not passengers[airports[gnome[i][j][0]][0]][airports[gnome[i][j][1]][0]]:
				num_passenger = passengers[airports[gnome[i][j][1]][0]][airports[gnome[i][j][0]][0]][1]
			else:
				num_passenger = passengers[airports[gnome[i][j][0]][0]][airports[gnome[i][j][1]][0]][0]
			num_aircraft = aircrafts[i][1]
			profit = int(aircrafts[i][3]) * dist * int(num_passenger)
			loss = int(aircrafts[i][3]) * dist * (int(num_aircraft) - int(num_passenger))
			cost = int(aircrafts[i][2])
			total_profit = profit - loss - cost
			total += total_profit

	return total


class Individual(object):

	def __init__(self, chromosome, buge):
		self.chromosome = chromosome
		self.fitness = self.cal_fitness()
		self.cost = buge

	@classmethod
	def mutated_genes(self):
		global GENES
		gene = random.choice(GENES)
		return gene

	@classmethod
	def create_gnome(self, len1, len2, limit_planes, budgets, i, budget):

		gnome = []
		gnome_len = (len1 * len1) - len1
		gnome_len_len = len2
		count2 = 0
		chance = 0
		chance1 = 0
		chance2 = 0

		for j in range(len2):
			gnome.append([])

		count = 0
		min_aiplane = budget
		for j in range(len(aircrafts)):
			min_aiplane = min(int(aircrafts[j][2]), min_aiplane)
		while(1):
			if((not any(limit_planes[i])) or (budgets[i]+min_aiplane >= budget)):
				break
			gene = self.mutated_genes()
			if (int(gene)):
				chance = random.randint(0, len(limit_planes[i])-1)
				if limit_planes[i][chance] and (budgets[i]+int(aircrafts[chance][2]) < budget):
					while(1):
						chance1 = random.randint(0, len(airports)-1)
						chance2 = random.randint(0, len(airports)-1)
						if(chance1 != chance2):
							break
					if([chance1, chance2] not in gnome[chance]):
						gnome[chance].append([chance1, chance2])
						limit_planes[i][chance] -= 1
						budgets[i] += int(aircrafts[chance][2])
						count += 1

		return gnome, budgets[i]

	def mate(self, par2, limit_planes, budgets, i, budget):

		gnome = []
		count2 = 0
		chance = 0
		chance1 = 0
		chance2 = 0
		child_chromosome = []

		for j in range(len(limit_planes[i])):
			child_chromosome.append([])

		count = 0
		min_aiplane = budget
		for j in range(len(aircrafts)):
			min_aiplane = min(int(aircrafts[j][2]), min_aiplane)


		count2 = 0
		for j in range(len(self.chromosome)):
			listg = []
			for z in range(len(self.chromosome[j])):
				prob = random.random()
				if prob < 0.45:
					if (limit_planes[i][j] > int(int(aircrafts[j][5])/20)) and (budgets[i]+int(aircrafts[j][2]) < budget):
						child_chromosome[j].append(self.chromosome[j][z])
						limit_planes[i][j] -= 1
						budgets[i] += int(aircrafts[j][2])

		for j in range(len(par2.chromosome)):
			listg = []
			for z in range(len(par2.chromosome[j])):
				prob = random.random()
				if prob < 0.45:
					if (par2.chromosome[j][z] not in child_chromosome[j]):
						if (limit_planes[i][j] > int(int(aircrafts[j][5])/20)) and (budgets[i]+int(aircrafts[j][2]) < budget):
							child_chromosome[j].append(par2.chromosome[j][z])
							limit_planes[i][j] -= 1
							budgets[i] += int(aircrafts[j][2])

		for j in range(len(child_chromosome)):
			listg = []
			for z in range(len(child_chromosome[j])):
				if(z >= len(child_chromosome[j])):
					break
				prob = random.random()
				if prob < 0.05:
					del child_chromosome[j][z]
					limit_planes[i][j] += 1
					budgets[i] -= int(aircrafts[j][2])


		while(1):

			if((not any(limit_planes[i])) or (budgets[i]+min_aiplane >= budget)):
				break
			gene = self.mutated_genes()
			if (int(gene)):
				chance = random.randint(0, len(limit_planes[i])-1)
				if limit_planes[i][chance] and (budgets[i]+int(aircrafts[chance][2]) < budget):
					while(1):
						chance1 = random.randint(0, len(airports)-1)
						chance2 = random.randint(0, len(airports)-1)
						if(chance1 != chance2):
							break
					if([chance1, chance2] not in child_chromosome[chance]):
						child_chromosome[chance].append([chance1, chance2])
						limit_planes[i][chance] -= 1
						budgets[i] += int(aircrafts[chance][2])
						count += 1

		return Individual(child_chromosome, budgets[i])

	def cal_fitness(self):
		fitness = 0

		fitness = check_fitness(self.chromosome)

		return fitness



def read_airports():
	airports = []
	with open("airports.txt", "r") as file:
		airport = file.readline()
		while airport:
			airport = airport.split()
			airports.append(airport)
			airport = file.readline()
	file.close()
	return airports


def read_aircrafts():
	aircrafts = []
	with open("aircrafts.txt", "r") as file:
		aircraft = file.readline()
		while aircraft:
			aircraft = aircraft.split()
			aircrafts.append(aircraft)
			aircraft = file.readline()
	file.close()
	return aircrafts


def read_passengers():
	passengers = defaultdict(lambda: defaultdict(list))
	with open("passengers.txt", "r") as file:
		passenger = file.readline()
		while passenger:
			passenger = passenger.split()
			passengers[passenger[0]][passenger[1]].append(passenger[2])
			passengers[passenger[0]][passenger[1]].append(passenger[3])
			passenger = file.readline()
	file.close()
	return passengers


airports = read_airports()
aircrafts = read_aircrafts()
passengers = read_passengers()

import copy


def find_best_flight_schedule():
	budget = int(input("Enter the Budget : "))

	limit_plane = []
	limit_planes = []
	budgets = []
	for i in range(len(aircrafts)):
		limit_plane.append(int(aircrafts[i][5]))
	for i in range(POPULATION_SIZE):
		budgets.append(0)
		limit_planes.append(copy.copy(limit_plane))
	

	generation = 1

	found = False
	population = []


	# create initial population
	for i in range(POPULATION_SIZE):
		gnome, buge = Individual.create_gnome(len(airports), len(aircrafts), limit_planes, budgets, i, budget)
		population.append(Individual(gnome, buge))

	last_gen = 0
	this_gen = 0
	more = 0
	max_fitness = 0
	max_chromosome = []
	count = 0
	flag_no_budget = 0

	while not found:
		population = sorted(population, key=lambda x: x.fitness)

		this_gen = population[len(population)-1].fitness
		if(max_fitness < this_gen):
			max_fitness = this_gen
			max_chromosome = copy.copy(population[len(population)-1].chromosome)

		if(population[len(population)-1].fitness >= budget*1000 or generation > 250):
			if(last_gen == this_gen):
				count += 1
			else:
				count = 0
			if(count > 10 or generation > 150):
				found = True
				break

		new_generation = []

		limit_planes.clear()
		budgets.clear()
		for i in range(POPULATION_SIZE):
			budgets.append(0)
			limit_planes.append(copy.copy(limit_plane))
		new_generation = reproduce(population, limit_planes, budgets, budget)
		if not new_generation:
			flag_no_budget = 1
			break


		population = new_generation

		last_gen = this_gen

		generation += 1



	if flag_no_budget:
		print("0")
		print("0")
		return


	print(population[len(population)-1].cost)
	print(population[len(population)-1].fitness)
	temp_print_list = defaultdict(lambda: defaultdict(list))
	print_list = defaultdict(lambda: defaultdict(list))
	airplanes = []

	for i in range(len(population[len(population)-1].chromosome)):
		for j in range(len(population[len(population)-1].chromosome[i])):
			airplanes = population[len(population)-1].chromosome[i][j]
			temp_print_list[airplanes[0]][airplanes[1]].append(aircrafts[i][0])


	for i in range(len(airports)):
		for j in range(i, len(airports)):
			if i==j: continue
			if temp_print_list[i][j] or temp_print_list[j][i]:
				temp_print_list[i][j].extend(list(temp_print_list[j][i]))


	for i in range(len(airports)):
		for j in range(i, len(airports)):
			if i==j: continue
			if temp_print_list[i][j]:
				print_list[i][j].extend(list(sorted(temp_print_list[i][j])))



	for i in range(len(airports)):
		for j in range(i, len(airports)):
			if i==j: continue
			if print_list[i][j]:
				print("{} {} ".format(airports[i][0], airports[j][0]), end='')
				flag_count = 0
				count = 1
				count2 = 0
				for z in range(len(print_list[i][j])):
					while(1):
						if(z != len(print_list[i][j])-1):
							if print_list[i][j][z] == print_list[i][j][z+1]:
								flag_count = 1
								break
							else:
								break
						else:
							break
					if flag_count:
						flag_count = 0
						continue
					if z == len(print_list[i][j])-1:
						print("{} {}".format(print_list[i][j][z], print_list[i][j].count(print_list[i][j][z])), end='')
					else:
						print("{} {}, ".format(print_list[i][j][z], print_list[i][j].count(print_list[i][j][z])), end='')
				print("")


def main():
	find_best_flight_schedule()


if __name__ == '__main__':
	main()
