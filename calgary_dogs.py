# calgary_dogs.py
# Bailey Collison
#
# A terminal-based application for computing and printing statistics based on given input.
import numpy as np
import pandas as pd

class CalgaryDogBreeds:
    '''
    A class used to compute and print analysis on Dog dataframe based on selected breed
    Initializes the CalgaryDogBreeds object with both a regular and multi index pandas data frame
    '''

    def __init__(self, data_frame):
        # Initialize the dataframe from the imported excel file
        self.data_frame = data_frame
        # Creat a multi index dataframe from the imported excel file using Year and Month as the indeces
        self.multi_index = self.data_frame.set_index(['Year', 'Month'])

    def breed_analysis(self, breed_selection):
        '''
        Method that analyzes both indexes for various statistical outputs and prints out results
        based on the dog breed selected using NumPy and Pandas methods

        Parameters:
            breed_selection (str): The selected dog breed to analyze

        No Returns

        '''
        # Selecting data for the breed on both dataframes
        selected_data = self.data_frame.loc[self.data_frame["Breed"] == breed_selection]
        selected_data_multi = self.multi_index.loc[self.multi_index["Breed"] == breed_selection]
        # Creating a list of years that the breed shows up in the selected data
        year_list = np.unique(list(selected_data["Year"]))
        print("The " + breed_selection + " was found in the top breeds for years:", *year_list)
        # Using NumPy sum method to get the total number of registrations for the selected data
        total_registrations = np.nansum(selected_data["Total"])
        print("There have been " + str(total_registrations) + " " + breed_selection + " dogs registered total.")
        # initializing idx to the pandas IndexSlice object
        idx = pd.IndexSlice
        for i in year_list:
            # Slicing the multi index to get the total registrations for each year
            total_year_data = self.multi_index.loc[idx[i, :], :]
            total_year_registrations = np.nansum(total_year_data["Total"])
            # Slicing the selected data multi index to get the registrations for the selected breed in each year
            breed_year_data = selected_data_multi.loc[idx[i, :], :]
            breed_year_registrations = np.nansum(breed_year_data["Total"])
            # Calculating and printing the percentage of registrations that were the selected breed for each year
            year_percentage = (breed_year_registrations / total_year_registrations) * 100
            print("The " + breed_selection + " was " + str(round(year_percentage, 6)) + "% of top breeds in " + str(i) + ".")
        # Calculating and printing the percentage of registrations that were the selected breed for all years
        all_year_registrations = np.nansum(self.multi_index["Total"])
        all_year_percentage = (total_registrations/all_year_registrations) * 100
        print("The " + breed_selection + " was " + str(round(all_year_percentage, 6)) + "% of top breeds across all years.")
        # Using a grouping method to count how many times each month appears in the data for the selected breed
        month_counts = selected_data_multi.groupby(level="Month").size()
        # Find the maximum count
        max_count = month_counts.max()
        # Identify and print the most popular months
        most_popular_months = month_counts[month_counts == max_count].index
        print("The most popular month(s) for " + breed_selection + " registrations are:", *most_popular_months)

def main():

    # Import data here
    # Importing excel spreadsheet and initialize data with CalgaryDogBreeds class
    data_frame = pd.read_excel('CalgaryDogBreeds.xlsx')
    breed_data = CalgaryDogBreeds(data_frame)

    print("ENSF 692 Dogs of Calgary")
    
    # User input stage
    # Using a while loop to check if the input is valid and raising a KeyError if it is not
    while True:
        try:
            breed_selection = input("Please enter a dog breed: ").upper()
            if breed_selection not in data_frame['Breed'].unique():
                raise KeyError("Dog breed not found in the data, please try again")
            else:
                break
        except KeyError as e:
            print(e)

    # Data anaylsis stage
    # Calling the breed_analysis method to analyze and print out all of the statistics
    breed_data.breed_analysis(breed_selection)

if __name__ == '__main__':
    main()
