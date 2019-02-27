import random

def main():
    noSteps = 100 #Number of steps in the production run
    noWorkerPairs = 6 #Number of teams of workers
    parts = ['A','B'] #Parts avaliable to the workers
    allowEmptyBeltSlot = True #Allow the belt to create an empty slot

    prodResult = runProduction(noSteps, parts, noWorkerPairs, allowEmptyBeltSlot)
    printResults(prodResult)

##Returns a random part from the list of inputed parts
def createNewPart(parts):
    return random.choice(parts)

## Moves the belt along one and adds a new part to the beginng
def beltMovePosition(currentBeltStatus, newComponent):
    lastBeltItem = currentBeltStatus[-1]
    currentBeltStatus.insert(0, newComponent)
    currentBeltStatus.pop()

    return currentBeltStatus, lastBeltItem

## Handles the worker logic
def workersWork(workers, beltPosition, parts):
    for workerLocation in workers:
        #if the belts empty allow workers to return completed products
        if beltPosition[workerLocation] == '':
            if all(elem in workers[workerLocation]['A'] for elem in parts):
                beltPosition[workerLocation] = 'P'

            elif all(elem in workers[workerLocation]['B'] for elem in parts):
                beltPosition[workerLocation] = 'P'
        else:
            #if the belt has items on it attempt to allow workers to pick it up
            for partId in parts:
                #check if the belt has a valid rpoduct on it
                if beltPosition[workerLocation] == partId:
                    # if the part is valid and the worker isnt currently holding
                    # one give it to him
                    if partId not in workers[workerLocation]['A']:
                        workers[workerLocation]['A'].insert(0, partId)
                        beltPosition[workerLocation] = ''
                        break

                    elif partId not in workers[workerLocation]['B']:
                        workers[workerLocation]['B'].insert(0, partId)
                        beltPosition[workerLocation] = ''
                        break

## Organise parts that reach the end of the production line into a map
def calculateLastItemNumbers(endProducts, lastBeltItem):
    if endProducts.get(lastBeltItem) == None:
        endProducts[lastBeltItem] = 0

    else:
        endProducts[lastBeltItem] += 1

    return endProducts

## create an empty belt for the workers to begin wroking on
def setupBelt(noWorkers):
    belt = []
    for i in range(noWorkers):
        belt.insert(0, '')

    return belt

##Setup avaliable parts
def setupParts(parts, allowBlank):
    if allowBlank == True:
        parts.insert(0, '')
    return parts

##Initualizes the worker pairs
def setupWorkers(noWorkerPairs):
    workers = {}
    for i in range(noWorkerPairs):
        workers[i] = {'A': [], 'B': []}

    return workers

##Setup and run production
def runProduction(noSteps, parts, noWorkerPairs, allowEmptyBeltSlot):
    productionParts = parts[:] #Avaliable parts for workers to chose from
    beltParts = setupParts(parts, allowEmptyBeltSlot) #Parts allowed on the belt
    beltPosition = setupBelt(noWorkerPairs) # Belt start position
    workerPairs = setupWorkers(noWorkerPairs) # Blank workers
    endProducts = {} #Blank number of end parts


    for i in range(noSteps):
        workersWork(workerPairs, beltPosition, productionParts)
        beltPosition, lastBeltItem = beltMovePosition(beltPosition,  createNewPart(beltParts))
        endProducts = calculateLastItemNumbers(endProducts, lastBeltItem)

    return endProducts

##Display the results of a production run
def printResults(endProducts):
    print(endProducts)
    print("Production finished with the following outcome: ")
    for i in endProducts:
        if i != '':
            print(str(i) + " Ended with " + str(endProducts[i]) + "")

main()