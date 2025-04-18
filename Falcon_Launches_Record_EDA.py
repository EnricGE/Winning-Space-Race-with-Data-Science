
# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the SpaceX dataset
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# Display the first 5 rows of the dataframe
print("First 5 rows of the dataset:")
df.head(5)

# Visualize FlightNumber vs PayloadMass with launch outcome
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Pay load Mass (kg)", fontsize=20)
plt.title("Flight Number vs. Payload Mass")
plt.show()

# TASK 1: Visualize the relationship between Flight Number and Launch Site
sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.title("Flight Number vs. Launch Site")
plt.show()

# TASK 2: Visualize the relationship between Payload and Launch Site
sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df, aspect=5)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.title("Payload Mass vs. Launch Site")
plt.show()

# TASK 3: Visualize the relationship between success rate of each orbit type
# Group by Orbit and calculate the mean of Class column
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index()
orbit_success.columns = ['Orbit', 'Success Rate']

# Create bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Orbit', y='Success Rate', data=orbit_success)
plt.xlabel('Orbit Type', fontsize=15)
plt.ylabel('Success Rate', fontsize=15)
plt.title('Success Rate by Orbit Type', fontsize=20)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# TASK 4: Visualize the relationship between FlightNumber and Orbit type
sns.catplot(x="FlightNumber", y="Orbit", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.title("Flight Number vs. Orbit Type")
plt.show()

# TASK 5: Visualize the relationship between Payload and Orbit type
sns.catplot(x="PayloadMass", y="Orbit", hue="Class", data=df, aspect=5)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.title("Payload Mass vs. Orbit Type")
plt.show()

# TASK 6: Visualize the launch success yearly trend
# Extract years from the date
df['Year'] = df['Date'].apply(lambda date: date.split('-')[0])

# Group by Year and calculate success rate
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
yearly_success.columns = ['Year', 'Success Rate']

# Plot line chart
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Success Rate', data=yearly_success, marker='o')
plt.xlabel('Year', fontsize=15)
plt.ylabel('Success Rate', fontsize=15)
plt.title('Launch Success Rate by Year', fontsize=20)
plt.grid(True)
plt.show()

# Features Engineering
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
print("\nSelected features for prediction:")
features.head()

# TASK 7: Create dummy variables to categorical columns
# Use get_dummies() function on the categorical columns
features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])
print("\nOne-hot encoded features:")
features_one_hot.head()

# TASK 8: Cast all numeric columns to float64
# Cast the entire dataframe to float64
features_one_hot = features_one_hot.astype('float64')
print("\nFeatures with float64 data type:")
features_one_hot.head()

# Verify the data types
print("\nData types after conversion:")
features_one_hot.dtypes

# Export the processed data to CSV for the next section
# Uncomment the following line to save the features to a CSV file
# features_one_hot.to_csv('dataset_part_3.csv', index=False)

