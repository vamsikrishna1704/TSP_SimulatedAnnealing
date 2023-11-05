import random
import matplotlib.pyplot as plt
import math

# Calculate distance between two points
def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Calculate the total distance of a path
def total_distance(path, places):
    d = 0
    for i in range(len(path) - 1):
        d += distance(places[path[i]], places[path[i + 1]])
    d += distance(places[path[-1]], places[path[0]])
    return d

# Make an initial path
def make_initial(num):
    return random.sample(range(num), num)

# Simulated Annealing Algorithm
def simulated_annealing(num, places, initial_temperature, final_temperature, cooling_rate, num_iterations):
    current_path = make_initial(num)
    current_distance = total_distance(current_path, places)
    
    best_path = current_path
    best_distance = current_distance
    
    temperatures = []  # Store temperatures
    distances = []  # Store best distances
    
    for iteration in range(num_iterations):

        temperature = initial_temperature / (1 + iteration)

        if temperature < final_temperature:
            break
        
        # Generate a neighboring solution by swapping two random cities
        new_path = current_path.copy()
        i, j = random.sample(range(num), 2)
        new_path[i], new_path[j] = new_path[j], new_path[i]
        new_distance = total_distance(new_path, places)
        
        # Calculate the change in distance
        delta_distance = new_distance - current_distance
        
        # If the new path is better or accepted with a certain probability, update the current path
        if delta_distance < 0 or random.random() < math.exp(-delta_distance / temperature):
            current_path = new_path
            current_distance = new_distance
        
        # Update the best path if needed
        if current_distance < best_distance:
            best_path = current_path
            best_distance = current_distance
        
        # Store temperature and best distance
        temperatures.append(temperature)
        distances.append(best_distance)
    
    return best_path, best_distance, temperatures, distances

# Main part
def main(num, initial_temperature,final_temperature, cooling_rate, num_iterations):
    places = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num)]
    
    best_path, best_distance, temperatures, distances = simulated_annealing(num, places, initial_temperature,final_temperature, cooling_rate, num_iterations)
    
    return best_path, best_distance, temperatures, distances,places

# Draw the best path
def draw(path, places):
    x = [places[i][0] for i in path]
    y = [places[i][1] for i in path]
    x.append(places[path[0]][0])
    y.append(places[path[0]][1])
    
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title("Best Path")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()

# Ask for input and run the program
num = int(input("Number of places: "))
initial_temperature = float(input("Initial temperature: "))
final_temperature = float(input("Final temperature: "))
cooling_rate = float(input("Cooling rate: "))
num_iterations = int(input("Number of iterations: "))

best_path, best_distance, temperatures, distances, places = main(num, initial_temperature,final_temperature, cooling_rate, num_iterations)

print("Best Path:", best_path)
print("Distance:", best_distance)

draw(best_path, places)

plt.figure()
plt.plot(temperatures, distances, marker='o', linestyle='-', color='r')
plt.title("Best Distance at Different Temperatures")
plt.xlabel("Temperature")
plt.ylabel("Best Distance")
plt.grid(True)
plt.show()