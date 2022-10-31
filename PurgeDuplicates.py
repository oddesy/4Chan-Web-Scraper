# imports the libraries needed to work with csv files
import csv
import os



# to run this program, type this into the anaconda prompt:
# python C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\PurgeDuplicates.py




# removes all duplicates from a csv file
def purge_duplicates():
    
    # opening the dataset file
    # reader_file = open(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'r', encoding='utf-8')

    # reading the CSV file
    # reader = csv.reader(reader_file)
    
    

    file_name = r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv"
    file_name_output = "my_csv.csv"

    inFile = open(file_name, 'r', encoding='utf8')

    outFile = open(file_name_output, 'w', encoding='utf8')

    listLines = []

    for line in inFile:

        if line in listLines:
            continue

        else:
            outFile.write(line)
            listLines.append(line)

    outFile.close()

    inFile.close()




# starts the program 
def main():

    print("Starting Program: \n\n") 
    purge_duplicates()




if __name__=="__main__":
    main()




