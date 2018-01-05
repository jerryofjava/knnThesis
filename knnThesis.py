import csv
import random
import math
import operator
import time

#Loads attributes based from the input 
def loadAttributes(filename, location, month, year):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset)-1):
            if str(dataset[x][17]) == location and str(dataset[x][18]) == month and str(dataset[x][19]) == year:
                loadAttributes.maxT=float(dataset[x][0])
                loadAttributes.minT=float(dataset[x][1])
                loadAttributes.meanT=float(dataset[x][2])
                loadAttributes.dryBulb=float(dataset[x][3])
                loadAttributes.wetBulb=float(dataset[x][4])
                loadAttributes.dewPt=float(dataset[x][5])
                loadAttributes.rh=float(dataset[x][6])
                loadAttributes.vp=float(dataset[x][7])
                loadAttributes.mslp=float(dataset[x][8])
                loadAttributes.cloud=float(dataset[x][9])
                loadAttributes.wind=float(dataset[x][10])
                loadAttributes.banana=float(dataset[x][11])
                loadAttributes.coconut=float(dataset[x][12])
                loadAttributes.corn=float(dataset[x][13])
                loadAttributes.palay=float(dataset[x][14])
                loadAttributes.sugarcane=float(dataset[x][15])
                loadAttributes.actual=str(dataset[x][16])
                break

#Calculates the accuracy by counting the number of correct predictions from the testing dataset, returns the accuracy 
def get_accuracy(filename):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        accuracy = 0
        for x in range(len(dataset)-1):
            maxT=float(dataset[x][0])
            minT=float(dataset[x][1])
            meanT=float(dataset[x][2])
            dryBulb=float(dataset[x][3])
            wetBulb=float(dataset[x][4])
            dewPt=float(dataset[x][5])
            rh=float(dataset[x][6])
            vp=float(dataset[x][7])
            mslp=float(dataset[x][8])
            cloud=float(dataset[x][9])
            wind=float(dataset[x][10])
            banana=float(dataset[x][11])
            coconut=float(dataset[x][12])
            corn=float(dataset[x][13])
            palay=float(dataset[x][14])
            sugarcane=float(dataset[x][15])
			
            k = 5
            split = 0.67
            training_set = main.training_set
            neighbors = list()
            distances = list()
            classes = main.classes
            attributes = 15
			
            test_instance = [maxT, minT, meanT, dryBulb, wetBulb, dewPt, rh, vp, mslp, cloud, wind, banana, coconut, corn, palay, sugarcane]

            find_euclidean_distance(test_instance, training_set, attributes, distances)

            find_neighbors(distances, neighbors, k, 'noprint')
			
            index, value = find_response(neighbors, classes)
			
            if classes[index] == str(dataset[x][16]):
                accuracy+=1
		
        accuracy = accuracy / (x+1)
        return accuracy

#Function for recording test cases in a specific .csv file		
def writeToCsv(location,month,year,result):
    myFields = ['Location', 'Month','Year','Crop']
	#Edit the file location with the a similar format as the one below.
    myFile = open('C:/Users/Jerry/Documents/Python Workspace/FolderForHistory/history.csv', 'w', newline='')  
    with myFile:   
        writer = csv.DictWriter(myFile, fieldnames=myFields)    
        writer.writeheader()
        writer.writerow({'Location' : location, 'Month' : month, 'Year' : year, 'Crop' : result})

#Extracts training cases based from split        
def load_data_set(filename, training_set, split):
    with open(filename, newline='') as iris:
        data_reader = csv.reader(iris, delimiter=' ')
        for line in data_reader:
            if random.random() < split:
                main.training_set.append((','.join(line)).split(','))

#Gets the classes for classification
def get_classes(training_set, classes):
    for instance in training_set:
        if instance[16] not in classes:
            main.classes.append(instance[16])

#Calculates the Euclidean Distance for each training case to the test case, and sorts the distances in ascending order
def find_euclidean_distance(sample, training_set, attributes, distances):
    dist = 0
    for ctr in range(len(training_set)):
        for x in range(attributes):
            dist += (float(training_set[ctr][x]) - sample[x]) ** 2
        distances.append((training_set[ctr], math.sqrt(dist)))
        dist = 0
    distances.sort(key=operator.itemgetter(1))

#Finds the nearest neighbors based from the top k shortest Euclidean Distances
def find_neighbors(distances, neighbors, k, noprint):
    for ctr in range(k):
        neighbors.append(distances[ctr])
        if noprint != 'noprint':
            print('>'+str(neighbors[ctr][0][16])+', Euclidean Distance: '+str(neighbors[ctr][1]))

#Counts the number of votes for each class based from its k neighbors to classify the test case's class
def find_response(neighbors, classes):
    votes = [0, 0, 0, 0, 0]
    for instance in neighbors:
        neighbor = instance.__getitem__(0)
        for ctr in range(len(classes)):
            if neighbor[16] == classes[ctr]:
                votes[ctr] += 1
    return max(enumerate(votes), key=operator.itemgetter(1))

#Main function of the program
def main():
    location=input('Choose a location(Apari, Baler, Cabanatuan, Dagupan, Vigan): ')
    month=input('Input a month: ')
    year=input('Choose a year(2003-2020): ')
    print('')
	
    start_time = time.time()
	
	#load the attributes
    loadAttributes('fullDataset.csv', location, month, year)
	
	#assign the attributes
    maxT = loadAttributes.maxT
    minT = loadAttributes.minT
    meanT = loadAttributes.meanT
    dryBulb = loadAttributes.dryBulb
    wetBulb = loadAttributes.wetBulb
    dewPt = loadAttributes.dewPt
    rh = loadAttributes.rh
    vp = loadAttributes.vp
    mslp = loadAttributes.mslp
    cloud = loadAttributes.cloud
    wind = loadAttributes.wind
    banana = loadAttributes.banana
    coconut = loadAttributes.coconut
    corn = loadAttributes.corn
    palay = loadAttributes.palay
    sugarcane = loadAttributes.sugarcane
    actual = loadAttributes.actual
	
	#Edit these based from what k, split, attributes, and filename of the training dataset needed
    k = 5
    split = 0.67
    main.training_set = list()
    neighbors = list()
    distances = list()
    main.classes = list()
    file = 'training.csv'
    attributes = 15

    # load the Iris data set
    load_data_set(file, main.training_set, split)

    # generate response classes from data set
    get_classes(main.training_set, main.classes)
	
    print('MaxT='+str(maxT)+', MinT='+str(minT)+', MeanT='+str(meanT)+', DryBulb='+str(dryBulb)+', WetBulb='+str(wetBulb)+', DewPT='+str(dewPt)+', RH='+str(rh)+', VP='+str(vp))
    print('MSLP='+str(mslp)+', Cloud='+str(cloud)+', Wind='+str(wind)+', Banana='+str(banana)+', Coconut='+str(coconut)+', Corn='+str(corn)+', Palay='+str(palay)+', Sugarcane='+str(sugarcane))
    print('')
    # test data
    test_instance = [maxT, minT, meanT, dryBulb, wetBulb, dewPt, rh, vp, mslp, cloud, wind, banana, coconut, corn, palay, sugarcane]
	
    # calculate distance from each instance in training data
    find_euclidean_distance(test_instance, main.training_set, attributes, distances)

    print('Neighbors:')
    # find k nearest neighbors
    find_neighbors(distances, neighbors, k, 'print')
    print('')
		
    # get the class with maximum votes
    index, value = find_response(neighbors, main.classes)
    print('The actual class was: '+ actual)
    print('The predicted class is : ' + main.classes[index])
    print('Number of votes : ' + str(value) + ' out of ' + str(k))
	
    accuracy = get_accuracy('testing.csv')
    print('Accuracy: '+str(accuracy*100)+'%')
	
	#Erase the '#' below to start recording test cases in a specific .csv file
    #writeToCsv(location,month,year,main.classes[index])
    print("--- %s seconds ---" % (time.time() - start_time))
    exit=input('Press any key to exit...')

main()