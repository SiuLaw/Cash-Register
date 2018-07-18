import os
import csv
import time
dir_path = os.path.dirname(__file__)
os.chdir(dir_path)
print(dir_path)
#os.chdir("/Users/Po/Desktop/Python/Convention")

file = open('Report.csv','a+') 

while True:
    print("Starting from top")
    
####################################################################################################
    
#Who is the seller
    while True:
        PersonFile = open('PersonInput.txt','r')
        PersonInput = input(PersonFile.read())
        PersonFile.close()
        
        os.system("clear")
        
        if PersonInput == "F":
            PersonInput = "Fork"
            os.system("clear")
            break
            
        if PersonInput == "L":
            PersonInput = "Lee"
            os.system("clear")
            break
            
        if PersonInput == "O":
            PersonInput = input("Type in name:")
            os.system("clear")
            break
    
        print("Unrecognised person, type 'O' for others")
    
    
####################################################################################################
    
#What is the Fandom
    
    while True:
        try:
            FandomFile = open('FandomInput.txt','r')
            FandomInput = int(input(FandomFile.read())) -1
            FandomFile.close()
            
            FandomFile = open('FandomInput.txt','r')
            FandomTable = []
            FandomCSV = csv.reader(FandomFile, delimiter=",")
            for line in FandomCSV:
                FandomTable.append(line)
        
            Fandom = str(FandomTable[FandomInput][1])
            os.system("clear")
            break
            
        except ValueError:
            os.system("clear")
            print("Oops! Choose a number.  Try again...")
            
        except IndexError:
            os.system("clear")
            print("Oops! Choose a valid number. Try again...")
    

    
####################################################################################################
    
#What Price
    
    PriceFile = open('PriceInput.txt','r')
    PriceTable = []
    PriceCSV = csv.reader(PriceFile, delimiter=",")
    for line in PriceCSV:
        PriceTable.append(line)
    PriceFile.close()
    
    
    
    while True:
        try:
            PriceFile = open('PriceInput.txt','r')
            PriceInput = input(PriceFile.read()+ "\n" + "\n" + "Or type 'O' for alternative pricing (e.g. sales)" +"\n" + "\n" + "\n" + "INPUT: ")
            PriceFile.close()
            if PriceInput == "O":
                os.system("clear")
                while True: #protection for not numeric input for "alternated pricing"
                    try:
                        NewPrice = input("Type in alternated pricing:")
                        Price = int(NewPrice)
                        break
                    except ValueError:
                        os.system("clear")
                        print("Oops! Choose a number.  Try again...")
                    
                
                while True: #protection for AFTER choosing a alternatied pricing, THEN the second time choosing a merch type
                    try:
                        PriceFile = open('PriceInput.txt','r')                
                        PriceInput = int( input("RESELECT:" + "\n" + "\n" + PriceFile.read() + "\n" + "\n" + "INPUT: "   ) ) - 1
                        Type = str(PriceTable[PriceInput][1])                     
                        PriceFile.close()
                        break
                    except ValueError:
                        os.system("clear")
                        print("Oops! Choose a number.  Try again...")
                    except IndexError:
                        os.system("clear")
                        print("Oops! Choose a valid number. Try again...")
                        
            else:
                PriceInput = int(PriceInput) - 1
                Price = int(PriceTable[PriceInput][2])
                Type = str(PriceTable[PriceInput][1])
                        
            PriceFile.close()
            os.system("clear")
            break
            
        except ValueError:
            os.system("clear")
            print("Oops! Choose a number.  Try again...")
            
        except IndexError:
            os.system("clear")
            print("Oops! Choose a valid number. Try again...")
         

    
####################################################################################################
    
#Merch
    MerchInput = input("Input details, e.g. Persona characters name, if not leave blank: ")
    os.system("clear")
    
####################################################################################################
    
#Time
    import time
    localtime = time.localtime(time.time())
    hour = str(localtime[3])
    
    if localtime[4] < 10:
        minute = "0" + str(localtime[4])
    else:
        minute = str(localtime[4])
        
    time = hour + ":" + minute
    
    
    output = time + ',' + PersonInput + ',' + Fandom + ',' + Type + ',' + MerchInput + ',' + str(Price)
    os.system("clear")
    
####################################################################################################
    
# print(output)
    
    print("Time:    " + time)
    print("Person:  " + PersonInput)
    print("Fandom:  " + Fandom)
    print("Type:    " + Type)
    print("Details: " + MerchInput )
    print("Price:   " + str(Price) )

    submit = input("Confirm record sales? Y/N")
    if submit == "Y":
        file.write( output + "\n" ) 
    else:
        os.system("clear")
        print("Sales not recorded, start again.")
        continue
    
    
    Check = input("Press Y to end, enter to continue")
   
    if Check == "Y":
        break
    os.system("clear")
    
file.close()
    
