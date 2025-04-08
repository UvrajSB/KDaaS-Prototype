import pandas as pd

# Load the dataset from the uploaded file
try:
    df = pd.read_csv('uploaded_file.csv')
except FileNotFoundError:
    print("The file 'uploaded_file.csv' was not found.")
    exit()

# Define a function to determine the age range for each individual
def get_age_range(age):
    if 0 <= age < 10:
        return "0 to 9"
    elif 10 <= age < 20:
        return "10 to 19"
    elif 20 <= age < 30:
        return "20 to 29"
    elif 30 <= age < 40:
        return "30 to 39"
    elif 40 <= age < 50:
        return "40 to 49"
    elif 50 <= age < 60:
        return "50 to 59"
    elif 60 <= age < 70:
        return "60 to 69"
    else:
        return "70 or older"

# Apply the function to create a new column 'AgeRange'
df['AgeRange'] = df['Age'].apply(get_age_range)

# Group by 'AgeRange' and count the number of diabetic people
age_ranges_with_counts = df.groupby('AgeRange')['Outcome'].sum().reset_index()

# Find the age range with the maximum number of diabetic people
max_diabetic_count = age_ranges_with_counts['Outcome'].max()
max_diabetic_age_range = age_ranges_with_counts[age_ranges_with_counts['Outcome'] == max_diabetic_count]['AgeRange'].values[0]

# Print the result for the age range with the maximum number of diabetic people
print(f"The age range with the maximum number of diabetic people is: {max_diabetic_age_range}")
print("Statistics for all other age ranges:")
print(age_ranges_with_counts)

# Save the updated DataFrame to a new CSV file if needed
df.to_csv('age_distribution.csv', index=False)