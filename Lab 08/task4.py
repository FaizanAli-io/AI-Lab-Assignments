import numpy as np

states = ['Sunny', 'Cloudy', 'Rainy']

transition_matrix = np.array([
    [0.7, 0.2, 0.1],  
    [0.3, 0.4, 0.3],  
    [0.2, 0.5, 0.3]   
])

def simulate_weather(start_state, days=10):
    current_state = start_state
    weather_sequence = [current_state]
    
    for _ in range(days - 1):
        current_state_index = states.index(current_state)
        current_state = np.random.choice(states, p=transition_matrix[current_state_index])
        weather_sequence.append(current_state)
    
    return weather_sequence

np.random.seed(42)  
weather_sequence = simulate_weather('Sunny', 10)
for day, weather in enumerate(weather_sequence, start=1):
    print(f"Day {day}: {weather}")

rainy_days = weather_sequence.count('Rainy')
print("Number of rainy days:", rainy_days)

def simulate_multiple_runs(runs=10000, days=10, min_rainy_days=3):
    print(f"\nRunning {runs} simulations...")
    count_at_least_3_rainy_days = 0
    
    for _ in range(runs):
        weather_sequence = simulate_weather('Sunny', days)
        if weather_sequence.count('Rainy') >= min_rainy_days:
            count_at_least_3_rainy_days += 1
    
    probability = count_at_least_3_rainy_days / runs
    return probability

probability = simulate_multiple_runs()
print("Probability of having at least 3 rainy days in 10 days:", probability)
