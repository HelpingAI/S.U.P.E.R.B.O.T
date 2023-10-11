import requests

def get_exercise_recommendations(age, weight, height, muscle, gender):
    url = "https://exercises-by-api-ninjas.p.rapidapi.com/v1/exercises"
    querystring = {
        "muscle": muscle
    }
    headers = {
        "X-RapidAPI-Key": "3676876612msh9bbbdd6cf1021bfp13a2e1jsn220ba5c363c6",  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "exercises-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

def main():
    print("Welcome to the Gym Trainer Bot!")

    age = int(input("Enter your age: "))
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))
    muscle = input("Enter the target muscle (e.g., biceps): ")
    gender = input("Enter your gender (male/female): ")

    exercises_data = get_exercise_recommendations(age, weight, height, muscle, gender)

    print("\nRecommended Exercises:")
    for index, exercise in enumerate(exercises_data, start=1):
        print(f"{index}. Exercise: {exercise['name']}")

if __name__ == "__main__":
    main()
