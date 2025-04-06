

import random
import matplotlib.pyplot as plt
import streamlit as st

# Define the Person class
class Person:
    def __init__(self, age, gender, education, employment, income, social_status, relatives_abroad):
        self.age = age
        self.gender = gender
        self.education = education
        self.employment = employment
        self.income = income
        self.social_status = social_status
        self.relatives_abroad = relatives_abroad
        self.accommodation = None

    def choose_accommodation(self):
        """Determine housing based on income, education, and social status"""
        if self.income > 100000:
            self.accommodation = random.choice(['Luxury Apartment', 'House'])
        elif 18000 <= self.income <= 100000:
            self.accommodation = 'Standard Apartment'
        elif self.income < 18000 and self.social_status == 'Single':
            self.accommodation = random.choice(['Shared Housing', 'Public Housing'])
        elif self.social_status == 'Family' and self.income >= 18000:
            self.accommodation = 'House'
        elif self.income < 18000 and self.social_status == 'Family':
            self.accommodation = 'Public Housing'
        else:
            self.accommodation = 'Undefined'

# Function to generate persons and plot housing choices
def create_persons_and_plot(num_persons, education_probs, employment_probs, income_min, income_max, social_status_probs, relatives_abroad_prob):
    persons = []
    accommodation_counts = {key: 0 for key in ['Luxury Apartment', 'Standard Apartment', 'Shared Housing', 'House', 'Public Housing', 'Undefined']}

    for _ in range(num_persons):
        age = random.choices(['15-24', '25-34', '35-44', '45-54', '55+'], [0.48, 0.333, 0.194, 0.099, 0.087])[0]
        gender = random.choices(['Female', 'Male'], [0.496, 0.504])[0]
        education = random.choices(['No education', 'Primary', 'Secondary', 'Higher'], education_probs)[0]
        employment = random.choices(['Employed', 'Unemployed'], employment_probs)[0]
        income = random.randint(income_min, income_max)  # Random income within the range
        social_status = random.choices(['Single', 'Family'], social_status_probs)[0]
        relatives_abroad = random.choices(['Yes', 'No'], [relatives_abroad_prob, 1 - relatives_abroad_prob])[0]

        person = Person(age, gender, education, employment, income, social_status, relatives_abroad)
        person.choose_accommodation()
        accommodation_counts[person.accommodation] += 1
        persons.append(person)

    # Plot the accommodation distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(accommodation_counts.keys(), accommodation_counts.values(), color=['blue', 'green', 'red', 'purple', 'orange', 'gray'])
    ax.set_xlabel('Accommodation Type')
    ax.set_ylabel('Number of People')
    ax.set_title(f'Accommodation Choices of {num_persons} People')

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig)
    return persons, accommodation_counts

# Function to calculate total resource usage
def calculate_resource_usage(persons):
    accommodation_needs = {
        'Luxury Apartment': {'water': 125, 'electricity': 20, 'land': 134},
        'House': {'water': 100, 'electricity': 16, 'land': 120},
        'Standard Apartment': {'water': 95, 'electricity': 14, 'land': 32},
        'Shared Housing': {'water': 60, 'electricity': 12, 'land': 16},
        'Public Housing': {'water': 40, 'electricity': 10, 'land': 12},
        'Undefined': {'water': 0, 'electricity': 0, 'land': 0},
    }

    total_water = sum(accommodation_needs[person.accommodation]['water'] for person in persons)
    total_electricity = sum(accommodation_needs[person.accommodation]['electricity'] for person in persons)
    total_land = sum(accommodation_needs[person.accommodation]['land'] for person in persons)

    return total_water, total_electricity, total_land

# Function to plot remaining resources
def plot_remaining_resources(total_water, total_electricity, total_land):
    # Available resources
    max_water = 875765 # litres
    max_electricity = 66.45 * 1e6  # kWh (converted from GWh)
    max_land = 30 * 1e6  # sqm (converted from sqkm)

    # Calculate remaining resources and percentages
    remaining_water = max(0, max_water - total_water)
    remaining_electricity = max(0, max_electricity - total_electricity)
    remaining_land = max(0, max_land - total_land)

    resources = ['Water (L)', 'Electricity (kWh)', 'Land (sqm)']
    used = [total_water, total_electricity, total_land]
    remaining = [remaining_water, remaining_electricity, remaining_land]
    max_values = [max_water, max_electricity, max_land]

    percentages_remaining = [(r / m) * 100 for r, m in zip(remaining, max_values)]
    colors = ['green' if p > 50 else 'yellow' if p > 25 else 'red' for p in percentages_remaining]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(resources, percentages_remaining, color=colors)
    ax.set_ylabel('Remaining Resources (%)')
    ax.set_title('Resource Availability After Migration')

    for bar, percent in zip(bars, percentages_remaining):
        ax.annotate(f'{percent:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig)

# Streamlit UI
st.title('Ostrava Migrants')
st.subheader('Migrants arrived due to a new foreign company')

# Interactive sliders for dynamic control
num_persons = st.number_input('Number of Persons', min_value=1, step=1, value=10000)
income_min = st.number_input('Minimum Salary (kc)', min_value=0, value=18000)
income_max = st.number_input('Maximum Salary (kc)', min_value=0, value=100000)

# Education probabilities
education_probs = [
    st.slider('No Education Probability', 0.0, 1.0, 0.02),
    st.slider('Primary Education Probability', 0.0, 1.0, 0.04),
    st.slider('Secondary Education Probability', 0.0, 1.0, 0.24),
    st.slider('Higher Education Probability', 0.0, 1.0, 0.70)
]

# Employment probabilities
employment_probs = [
    st.slider('Employed Probability', 0.0, 1.0, 0.9),
    st.slider('Unemployed Probability', 0.0, 1.0, 0.1)
]

# Social Status probabilities
social_status_probs = [
    st.slider('Single Probability', 0.0, 1.0, 0.50),
    st.slider('Family Probability', 0.0, 1.0, 0.50)
]

# Relatives abroad probability
relatives_abroad_prob = st.slider('Relatives Abroad Probability', 0.0, 1.0, 0.50)

# Run the model when the button is pressed
if st.button('Run Model'):
    persons, _ = create_persons_and_plot(num_persons, education_probs, employment_probs, income_min, income_max, social_status_probs, relatives_abroad_prob)
    total_water, total_electricity, total_land = calculate_resource_usage(persons)

    # Display total usage
    st.write(f"Total Water Usage: {total_water:.2f} Litres/day")
    st.write(f"Total Electricity Usage: {total_electricity:.2f} kWh/day")
    st.write(f"Total Land Required: {total_land:.2f} sqm")

    # Plot remaining resources
    plot_remaining_resources(total_water, total_electricity, total_land)

