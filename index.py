import requests
import os
import numpy as np

def isNotAssociatedCard(cardCode):
    # Exclude Petty Officer edge case (thanks Riot)
    return not cardCode[-2] == 'T' and not cardCode == '02BW008T02'

def getSetResource(setNumber):
    # Get the raw JSON from Riot's servers
    response = requests.get(f"https://dd.b.pvp.net/latest/set{setNumber}/en_us/data/set{setNumber}-en_us.json")
    response.raise_for_status()
    jsonResponse = response.json()
    
    # Filter each card down to their card code
    for index, cardData in enumerate(jsonResponse):
        jsonResponse[index] = cardData['cardCode']
        
    # Filter out associated cards
    filteredCards = filter(isNotAssociatedCard, jsonResponse)
    
    validCards = [card for card in filteredCards]
    return validCards

def getExistingCards():
    cardCodes = []
    
    # Add all existing png files into a list
    for i, file in enumerate(os.listdir('./cards/')):
        if file.endswith(".png"):
            cardCodes.append(os.path.basename(file))
            
    # Parse out the file extensions
    cardCodes = [ file.split('.')[0] for file in cardCodes ]
    return cardCodes

def arrayToString(missingCards):
    result = ""
    for code in missingCards:
        result += f"{code}\n" 
    return result

def getMissingCards():
  # Get set data
  set1Data = getSetResource(1)
  set2Data = getSetResource(2)
  set3Data = getSetResource(3)
  
  # Combine all of it into single list
  setData = np.concatenate((np.concatenate((set1Data, set2Data)), set3Data))
  existingCards = getExistingCards()
  
  missingCards = []
  # For every card that isn't found in the cards folder, add them to the missing cards array
  for i, code in enumerate(setData):
      if not code in existingCards:
          missingCards.append(code)
  
  # Write the missing cards to a file
  f = open("./response/missingCards.txt","w")
  f.write(arrayToString(missingCards))
  f.close()
  
getMissingCards()