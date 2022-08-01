#Daimler Technical code 
#Author: Miguel Moreno Mardones
#Date: 28/05/2022

#Libraries imported
import pandas as pd

#Input JSON file to read in this script
#We use pandas library so we can read it
#CAUTION = JSON file must be in the same directory as this file
file = pd.read_json('Daimler-test-data.json')

#Input keyboard sku code

#While loop: User must introduce an sku code between 1 and 20000, otherwise an exception will raise
#We have defined two types of Exceptions ValueError and TypeError
while True:
    try:
        value = int(input('Introduce an sku code number between 1 and 20000\n'))
        if value < 1 or value > 20000:
            raise TypeError
        value = 'sku-' + str(value)
        print('\n Your sku code is: {}'.format(value))
        break
    except ValueError: 
        print('Exception generated: sku code must be a number and integer\n')
    except TypeError:
        print('Exception generated: sku code must be between 1 and 20000\n')
        

#Extraction of sku Values given by input sku code
skuValues = list(file[value])

#we define a dataset that associates each position with its sku value, otherwise it will show a NaN value
df2 = file[file.isin(skuValues)]

#We drop sku code values that doesnt match the pattern
df2.dropna(axis = 0, how = 'all', inplace = True)

#We use Transpose to improve readability and replace NaN values with zeros
df2 = df2.T
df2 = df2.fillna('0')

#Definition of two empty lists so we can use them later
prox = []
match = []

#For loop that allows us to:
for i in range(len(df2)): #for every element in dataframe
    #First row as list
    row = list(df2.iloc[i])
    #Lambda Function that counts elements of row that are not equal to zero
    count = sum(map(lambda x : x != '0', row))
    #We append every count value through the loop to our empty list
    match.append(count)


#Creation of similar loop to facilitate concepts

#For loop that allows us to:
for i in range(len(df2)):
    #First row as list
    row = list(df2.iloc[i])
    #Lambda Function that extract elements of row that are not equal to zero
    letters = (list(filter(lambda x: x != '0', row)))
    #empty string
    a = ""
    #Fro loop to iterate through row 'att-..' values of every cell
    for z in range(len(letters)):
        #Transform them to string
        let = str(letters[z])
        #extracting 4 character whic is the letter that follows -
        let = let[4]
        #Adding this single letter to empty string and then so we can concatenate the rest 
        a += let
    #We append string of letters as a list to our empty list
    prox.append([a])


#Creation of two new columns that references number of matches and proximity for every row 
df2['matches'] = match
df2['proximity'] = prox


#Convertion of column proximity which is a list of lists to a string column that contains only strings (letters)
df2['proximity'] = [','.join(map(str, l)) for l in df2['proximity']]


#We can now order our dataset with Number of matches and proximity
#First condition will be number of matches, if two rows got the same number of matches, we will sort them by proximity
sorted_values = df2.sort_values(by = ['matches','proximity'], ascending=[False,True])


#New Object Output that extract first 10 values
Output = (file[list(sorted_values.head(11).index)])
#Cast to dictionary so we can make a correct output
Output = Output.to_dict()

#Final output
for i in Output:
    if i == str(list(Output.keys())[0]):
        print(str(i) + ' ' + str(Output[i]) + ' is more similar to\n')
    if i == str(list(Output.keys())[-1]):
        print(str(i) + ' ' + str(Output[i])) 
    if (i != str(list(Output.keys())[0]) and i != str(list(Output.keys())[-1])):
        print(str(i) + ' ' + str(Output[i]) + ' than to\n')


#Aditional ways to implement this algorithm 

#Definitely the realization of this solution has not been an easy task, I modified on Saturday 28th the whole way of interpreting the algorithm, 
#because instead of sorting by number of matches and then by alphabetical order, 
#I had established a weighting system based on the non-zero position of each row, giving higher values for the leftmost positions.

#That is why a priori the statement seemed to me a bit ambiguous, and although it is true that applying my method the output obtained was 
#90% similar to the original one, it did not work correctly.

#I still think that the scoring system or weights for recommendations can be a great algorithm when it comes to establishing recommendation criteria. 
#It can be used both in a sentiment analysis of a product, giving high weights to positive ratings and words and negative ones to the opposite. 
#The improvement I would implement involves not only the referrer letter of each row, but also its value following the '-'. 
#Thus, a cell with value 'att-a1' would have a higher weight than one that was 'att-a123'. 

#The recommendation for both cases would be correct, since the column 'att-a' is similar to this value, 
#but the cell 'att-a1' would have more weight because it has a shorter string value or a string value closer to the original one. 

#Thank you so much for your time!
#¡Gracias por su tiempo!