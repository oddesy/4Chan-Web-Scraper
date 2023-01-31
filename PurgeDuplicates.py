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
    


    # opens the files
    with open(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\Pol_Forum_Dataset.csv", 'r', encoding='utf-8') as input_file, open(r"C:\Users\Jackson\Documents\Coding\4Chan-Web-Scraper\vocab.csv", 'w', encoding='utf-8') as output_file:
        
        # creates these objects to work with the files
        csv_input = csv.reader(input_file)
        csv_output = csv.writer(output_file)

        # holds the list of new rows
        list_of_new_rows = []

        # loops through every row in the csv file
        for row in csv_input:
            
            # print(row)

            # if the row isn't just blank whitespace, then write it to the output file
            if (str(row) != "['', 'United States', '2023-01-25 14:23:59', '']" and str(row) != "[]"):
                
                # adds the row to the list_of_new_rows
                list_of_new_rows.append(row)

        print(str(len(list_of_new_rows)) + "rows added (twice that if you count whitespace)")
        
        # writes the list_of_new_rows to the output csv file
        csv_output.writerows(list_of_new_rows)





# starts the program 
def main():

    print("Starting Program: \n\n") 
    purge_duplicates()




if __name__=="__main__":
    main()












"""

file_name = 
file_name_output = "vocab.csv"

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

"""