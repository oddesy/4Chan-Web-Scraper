# imports the libraries needed to work with csv files
import csv
import os


# to run this program, type this into the anaconda prompt:
# python C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\CleanDataset.py




# removes all duplicates from a csv file
def remove_extra_whitespace():
    
    # opening the dataset file
    # reader_file = open(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'r', encoding='utf-8')

    # reading the CSV file
    # reader = csv.reader(reader_file)
    
    with open(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", encoding='utf-8') as input_file, open('vocab.csv', 'w', encoding='utf-8') as output_file:
        csv_input = csv.reader(input_file)
        csv_output = csv.writer(output_file)

        # loops through every row in the csv file
        for row in csv_input:
            
            # if the row isn't just blank whitespace, then write it to the output file
            if (str(row) != "[]"):
                csv_output.writerow(row)

    




# starts the program 
def main():

    print("Starting Program: \n\n") 
    remove_extra_whitespace()




if __name__=="__main__":
    main()




