#Alison Cameron and Cathy Guang
import csv
import sys

def print_usage():
    #print each line of usage.txt
    return 0

def search_authors(searchstring):
    #for each line in the csv, determine if the searchstring is
    #contained in the author column (case insensitive)
        #for each author where this is the case, keep track of
        #their books, and print them out at the end

    #if the searchstring isn't contained in any author names,
    #then print some kind of error message
    return 0

def search_titles(searchstring):
    #for each line in the csv, determine if the searchstring is
    #contained in the title column (case insensitive)
        #if it is contained, print out the full title and other info (?)

    #if the searchstring isn't contained in any titles,
    #then print some kind of error message
    return 0

def find_books_in_range(startyear, endyear):
    #for each line in the csv, determine if the publication year is
    #within the given range
        #if the book is contained within the range, print out title
        #and other info(?)

    #if there are no books within the range, print out some kind
    #of error message

    return 0

def are_valid_arguments(arg_list):
    valid = False
    if (len(arg_list) <= 1) or ('-d' in arg_list and len(arg_list) != 4):
        return valid

    operation_count = 0
    for arg in arg_list:
        if '-a' in arg or '--author' in arg:
            operation_count += 1
            if '=' in arg and len(arg.split('=')) == 2:
                valid = True
            else:
                print("The option -a must include a SEARCHSTRING")
                print("See below for proper command-line syntax \n\n")
                valid = False

        if '-d' in arg or '--daterange' in arg:
            operation_count += 1
            #do more checking

        if '-h' in arg or '--help' in arg:
            operation_count += 1
            valid = True

        if '-t' in arg or '--title' in arg:
            operation_count += 1
            if '=' in arg and len(arg.split('=')) == 2:
                valid = True
            else:
                print("The option -t must include a SEARCHSTRING")
                print("See below for proper command-line syntax \n\n")
                valid = False


    #users can only use one command at a time
    if operation_count != 1:
        valid = False

    return valid

def main():
    #parse command-line arguments
    arg_list = sys.argv
    print(sys.argv)
    if not(are_valid_arguments):
        print_usage()

    #verify that command-line arguments are valid
    #depending on the arguments, run the proper functions
    return 0

if __name__ == "__main__":
    main()
