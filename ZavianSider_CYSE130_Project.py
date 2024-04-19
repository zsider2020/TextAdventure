#!/usr/bin/env python
# coding: utf-8

# In[283]:


#imports
import os
import random

#Global vars
#Player related
#pos is the list, cord is actual cords
playerPosX = 0
playerPosY = 0
playerCordX = -1
playerCordY = 0
userInput = ""
gameover= False
ending = 0
activePlayer = None

#map of the game 
global gameMap 
gameMap = [
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Mountain", "Cave", "Mountain", "Mountain", "Mountain", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Mountain", "Mountain", "Mountain", "Mountain", "Mountain", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Mountain", "Mountain", "Mountain", "Mountain", "Mountain", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Mountain", "Mountain", "Mountain", "Warlock", "Mountain", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Mountain", "Mountain", "Mountain", "Mountain", "Mountain", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Swamp", "Swamp", "Swamp", "Swamp", "Swamp", "Forest", "Forest", "Forest", "Forest", "Forest", "Beach", "Beach", "Ocean", "Ocean", "Ocean", "Deadzone"],
["Deadzone", "Swamp", "Swamp", "Swamp", "Swamp", "Swamp", "Forest", "Forest", "Forest", "Forest", "Forest", "Beach", "Beach", "Ocean", "Temple", "Ocean", "Deadzone"],
["Deadzone", "Swamp", "Swamp", "Swamp", "Swamp", "Swamp", "Forest", "Forest", "City", "Forest", "Forest", "Beach", "Beach", "Ocean", "Ocean", "Ocean", "Deadzone"],
["Deadzone", "Witch", "Swamp", "Swamp", "Swamp", "Swamp", "Forest", "Forest", "Forest", "Forest", "Forest", "Beach", "Beach", "Ocean", "Ocean", "Ocean", "Deadzone"],
["Deadzone", "Swamp", "Swamp", "Swamp", "Swamp", "Swamp", "Forest", "Forest", "Forest", "Forest", "Forest", "Beach", "Boy", "Ocean", "Ocean", "Ocean", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Desert", "Desert", "Desert", "Desert", "Desert", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Desert", "Desert", "Desert", "Desert", "Desert", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Desert", "Desert", "Desert", "Oasis", "Desert", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Sinkhole", "Desert", "Desert", "Desert", "Desert", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Desert", "Desert", "Desert", "Desert", "Desert", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"],
["Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone", "Deadzone"]
]

enemies = ["goblin","slime", "zombie", "bandit", "demon", "Wyrm"]

        

    

    



# In[284]:


#main
def main():
    #run game
    gameStart()
    global userInput
    global activePlayer
    global gameover
    global ending
    gameover = activePlayer.healthCheck()
    print("You awaken in an unfamiliar land. The only thing you can remember is satifying the king at 0,0; whatever that means")
    while gameover ==False:
        #Game runs until fail
        userInput = ""
        while userInput != "m" and userInput!="s" and userInput !="l":
            userInput = input(f"What do you wish to do? Move(m) Save(s) Load(l)\nYou are currently at {playerCordX},{playerCordY}: {gameMap[playerPosY][playerPosX]}: ")
        match userInput:
            case "m":
                #movement
                userInput = input("\nWhich direction do you wish to go (North, South, East or West)? Input anything else to stay in place: ")
                if userInput!="0":
                    playerMovement(userInput.lower())
                else:
                    print("You decided not to move")
                gameEvent()
            case "s":
                #save
                saveGame(activePlayer)
        
            case "l":
                #load
                loadGame("saveData.txt")
        #These last parts basically just check if the game can end
        gameover = activePlayer.healthCheck()
        if activePlayer.playerQuest == 4:
            ending = 3
        if ending !=0:
            gameover =True
    if activePlayer.healthCheck():
        print("YOU DIED")
        saveGame(activePlayer)
        print("Make a new character to play again")
    else:
        #ENDINGS
        match ending:
            case 1:
                print("You decided to abandon the people of this land.... Your life is too valuable to risk.......")
                print("BAD ENDING")
            case 2:
                print("You've saved the king! You live the rest of your life in luxury in the city...........\n You can't help be feel like you missed something..... Oh well")
                print("GOOD ENDING")
            case 3:
                print("You've saved the land! You are forever remembered as a true hero in this land as you retire as the king")
                print("TRUE ENDING")


# In[285]:


def gameStart():
    #initializes game
    global userInput
    global playerPosX
    global playerPosY
    global playerCordX
    global playerCordY
    global activePlayer
    #asks if player wants to load. If they do it loads the save file, if not or it cant find the save then its gonna start another game.
    userInput = input("Do you want to load?(Y/N): ")
    if userInput.lower() == "y":
        if os.path.exists('./saveData.txt') is True:
            loadGame("saveData.txt")
        else:
            print("No save found. Starting new game")
            #Sets up a character at spawn
            playerPosX = 7
            playerPosY = 8
            playerCordX = -1
            playerCordY = 0
            while userInput.lower() != "archer" and userInput.lower() != "barbarian" and userInput.lower() != "wizard":
                userInput = input("Pick your class: Archer, Barbarian, Wizard: ")
            activePlayer = Player(userInput.lower())
            activePlayer.starterBuff()
            activePlayer.setWpn()
            saveGame(activePlayer)
            print(f"Player Created: {activePlayer.playerClass} with \n{activePlayer.playerAtk} Atk, \n{activePlayer.playerAgl} Agl, \n{activePlayer.playerInt} Int, \n{activePlayer.playerCon} Con, \n{activePlayer.playerCha} Cha, \n{activePlayer.playerHP} HP, \n{activePlayer.playerXP} XP, \n{activePlayer.playerLV} LV, \n{activePlayer.playerMoney} Money, \n{activePlayer.playerQuest} Quests Done, \n{activePlayer.playerInventory} Items")
    else:
        #Sets up a character at spawn
        playerPosX = 7
        playerPosY = 8
        playerCordX = -1
        playerCordY = 0
        while userInput.lower() != "archer" and userInput.lower() != "barbarian" and userInput.lower() != "wizard":
            userInput = input("Pick your class: Archer, Barbarian, Wizard: ")
        activePlayer = Player(userInput.lower())
        activePlayer.starterBuff()
        activePlayer.setWpn()
        saveGame(activePlayer)
        print(f"Player Created: {activePlayer.playerClass} with \n{activePlayer.playerAtk} Atk, \n{activePlayer.playerAgl} Agl, \n{activePlayer.playerInt} Int, \n{activePlayer.playerCon} Con, \n{activePlayer.playerCha} Cha, \n{activePlayer.playerHP} HP, \n{activePlayer.playerXP} XP, \n{activePlayer.playerLV} LV, \n{activePlayer.playerMoney} Money, \n{activePlayer.playerQuest} Quests Done, \n{activePlayer.playerInventory} Items")


# In[286]:


def playerMovement(userDirection):
    global playerPosX
    global playerPosY
    global playerCordX
    global playerCordY
    #move desired direction if the area you want to go to isnt a deadzone
    #changes the cord to look like real cords and changes pos to match the list
    if userDirection == "north" and gameMap[playerPosY-1][playerPosX]!= "Deadzone":
        if gameMap[playerPosY-1][playerPosX]=="Cave" and "Torch" not in activePlayer.playerInventory:
            print("You can't go over there. It's too dark to see")
        elif (gameMap[playerPosY-1][playerPosX]=="Swamp" or gameMap[playerPosY-1][playerPosX]=="Desert") and "Map" not in activePlayer.playerInventory:
            print("You are lost! It takes you 4x the amount of time to move forward")
            print(f"You are losing health from the environment! {-8 + activePlayer.playerCon} Damage recieved!")
            activePlayer.heal(-8 + activePlayer.playerCon)
            gameover = activePlayer.healthCheck()
            playerPosY = playerPosY-1
            playerCordY = playerCordY+1
        else:
            playerPosY = playerPosY-1
            playerCordY = playerCordY+1
    elif userDirection == "east" and gameMap[playerPosY][playerPosX+1]!= "Deadzone":
        if gameMap[playerPosY][playerPosX+1]=="Ocean" and "Raft" not in activePlayer.playerInventory:
            print("You can't go over there. The water is too deep")
        elif gameMap[playerPosY][playerPosX+1]=="Cave" and "Torch" not in activePlayer.playerInventory:
            print("You can't go over there. It's too dark to see")
        elif (gameMap[playerPosY][playerPosX+1]=="Swamp" or gameMap[playerPosY][playerPosX+1]=="Desert") and "Map" not in activePlayer.playerInventory:
            print("You are lost! It takes you 4x the amount of time to move forward")
            print(f"You are losing health from the environment! {-8 + activePlayer.playerCon} Damage recieved!")
            activePlayer.heal(-8 + activePlayer.playerCon)
            gameover = activePlayer.healthCheck()
            playerPosX = playerPosX+1
            playerCordX = playerCordX+1
        else:
            playerPosX = playerPosX+1
            playerCordX = playerCordX+1
    elif userDirection == "south" and gameMap[playerPosY+1][playerPosX]!= "Deadzone":
        if gameMap[playerPosY+1][playerPosX]=="Cave" and "Torch" not in activePlayer.playerInventory:
            print("You can't go over there. It's too dark to see")
        elif (gameMap[playerPosY+1][playerPosX]=="Swamp" or gameMap[playerPosY+1][playerPosX]=="Desert") and "Map" not in activePlayer.playerInventory:
            print("You are lost! It takes you 4x the amount of time to move forward")
            print(f"You are losing health from the environment! {-8 + activePlayer.playerCon} Damage recieved!")
            activePlayer.heal(-8 + activePlayer.playerCon)
            gameover = activePlayer.healthCheck()
            playerPosY = playerPosY+1
            playerCordY = playerCordY-1
        else:
            playerPosY = playerPosY+1
            playerCordY = playerCordY-1
    elif userDirection == "west" and gameMap[playerPosY][playerPosX-1]!= "Deadzone":
        if gameMap[playerPosY][playerPosX-1]=="Cave" and "Torch" not in activePlayer.playerInventory:
            print("You can't go over there. It's too dark to see")
        elif (gameMap[playerPosY][playerPosX-1]=="Swamp" or gameMap[playerPosY][playerPosX-1]=="Desert") and "Map" not in activePlayer.playerInventory:
            print("You are lost! It takes you 4x the amount of time to move forward")
            print(f"You are losing health from the environment! {-8 + activePlayer.playerCon} Damage recieved!")
            activePlayer.heal(-8 + activePlayer.playerCon)
            gameover = activePlayer.healthCheck()
            playerPosX = playerPosX-1
            playerCordX = playerCordX-1
        else:
            playerPosX = playerPosX-1
            playerCordX = playerCordX-1
    else:
        print("Can cannot travel over there! The terrain looks dangerous!")


# In[287]:


def gameEvent():
    global activePlayer
    global ending
    global gameover
    userDecisions = ""
    #random event based off of the number if not scripted event. 1 is enemy, 2 is encounter, 3 is nothing
    randomNumber = random.randint(1,3)
    #what happens in the city
    if gameMap[playerPosY][playerPosX]== "City":
        print("You enter the nice populated city. You wonder what to do next")
        while userDecisions!="0":
            userDecisions = input("There's a castle(1), a church(2) and a shop(3). Where do you wish to visit?(0 to leave): ")
            match userDecisions:
                case "1":
                    print("\nYou enter the castle")
                    print("King:'Help. I am bedridden due to a curse and cannot treat myself without a dragon's egg\nDo this for me and you'll be set for life'")
                    if "dragon_egg" in activePlayer.playerInventory:
                        print("Thank you kind soul, I can use this egg to heal myself. I hearby promote you to a noble")
                        activePlayer.loseItem("dragon_egg")
                        activePlayer.questComp()
                        ending = 2
                        gameover=True
                case "2":
                    print("\nYou walk into the church's courtyard and are approached by a resident")
                    print("Resident'You must help us! The witch of the west has cursed our land! You must defeat her!'")
                    if "witch_finger" in activePlayer.playerInventory:
                        print("Is that her finger? Wow! You have saved us from her terror!")
                        activePlayer.loseItem("witch_finger")
                        activePlayer.questComp()  
                case "3":
                    print("\nYou stop by the local shop")
                    discount = 1 + (activePlayer.playerCha/10)
                    userDecisions = input(f"Shopkeep: 'What do you want?'\nCurrent money: {activePlayer.playerMoney} \n Shop inventory: \n| Ration {int(15/discount)}g (1) |\n| Armor {int(50/discount)}g (2) |\n| Raft {int(250/discount)}g (3) |\n| Map {int(100/discount)}g (4) |: ")
                    match userDecisions:
                        case "1":
                            if activePlayer.playerMoney>=int(15/discount):
                                activePlayer.playerMoney=activePlayer.playerMoney - int(15/discount)
                                activePlayer.gainItem("Ration")
                            else:
                                print("Shopkeep: 'I don't like broke people'")
                        case "2":
                            if activePlayer.playerMoney>=int(50/discount):
                                activePlayer.playerMoney=activePlayer.playerMoney - int(50/discount)
                                activePlayer.gainItem("Armor")
                            else:
                                print("Shopkeep: 'I don't like broke people'")
                        case "3":
                            if activePlayer.playerMoney>=int(250/discount):
                                activePlayer.playerMoney=activePlayer.playerMoney - int(250/discount)
                                activePlayer.gainItem("Raft")
                            else:
                                print("Shopkeep: 'I don't like broke people'")
                        case "4":
                            if activePlayer.playerMoney>=int(100/discount):
                                activePlayer.playerMoney=activePlayer.playerMoney - int(100/discount)
                                activePlayer.gainItem("Map")
                            else:
                                print("Shopkeep: 'I don't like broke people'")
                        case _:
                                print("Shopkeep: 'What? We dont got that.'")
        print("You leave the city")
    elif gameMap[playerPosY][playerPosX]== "Warlock":
        print("\nYou find a creepy shack")
        while userDecisions!="0" and userDecisions!="1":
            userDecisions = input("Warlock:'Hmmm? Who goes there?! If you have no business here then leave!'(1 to approach)(0 to leave): ")
            match userDecisions:
                case "1":
                    print("So you insist on being a nuistance huh? Fine.\n I need something strange from the desert to continue my research")
                    if "sandworm_carcass" in activePlayer.playerInventory:
                        print("Thank you for doing that. Now I can finally complete my research")
                        activePlayer.loseItem("sandworm_carcass")
                        activePlayer.questComp() 
                case "0":
                    print("You leave the lair")
    elif gameMap[playerPosY][playerPosX]== "Boy":
        print("\nA boy runs up to you")
        while userDecisions!="0" and userDecisions!="1":
            userDecisions = input("Help! My heirloom was taken by a tentacle beast!'(1 to talk)(0 to leave): ")
            match userDecisions:
                case "1":
                    print("It got taken into the water! If you hurry you might still be able to find it!")
                    if "kraken_orb" in activePlayer.playerInventory:
                        print("Thank you! I'll always remember what you have done for me!")
                        activePlayer.loseItem("kraken_orb")
                        activePlayer.questComp()  
                case "0":
                    print("You leave the lair")
    elif gameMap[playerPosY][playerPosX]== "Oasis":
        print("\nYou see a wide ocean ahead of you")
        while userDecisions!="0" and userDecisions!="1":
            userDecisions = input("Do you investigate?(1 to approach)(0 to leave): ")
            match userDecisions:
                case "1":
                    print("You approach the oasis, but it takes you the entire day to realize that it was a mirage")
                    activePlayer.playerHP =  activePlayer.playerHP - abs((3*(activePlayer.playerCon-2))-1)
                    print(f"Suffered Dehydration\n {abs((3*(activePlayer.playerCon-2))-1)} damage recieved!\n current hp: {activePlayer.playerHP}")  
                case "0":
                    print("You decide not to pursue the possible illusion, and see that the Oasis was right behind you the whole time!")
                    activePlayer.heal(abs(1+(3*(activePlayer.playerCon+2))))
                    print(f"You drink from the water. You are healing!\n {abs(1+(3*(activePlayer.playerCon+2)))} damage healed!\n current hp: {activePlayer.playerHP}")
                    print("You found a torch!")
                    activePlayer.gainItem("Torch")
                    
    elif gameMap[playerPosY][playerPosX]== "Cave":
        print("\nYou encounter a Sleeping Dragon!")
        while userDecisions!="0" and userDecisions!="1":
            userDecisions = input("Do you attack or sneak?(1 to attack)(0 to sneak): ")
            match userDecisions:
                case "1":
                    print("You attack!")
                    print("You Encountered an Enemy!")
                    gameCombat("dragon")
                    if activePlayer.healthCheck()==False:
                        print("You got the dragon's egg")
                        activePlayer.gainItem("dragon_egg")
                    else:
                        print("You lost....")                    
                case "0":
                    print("You try to sneak around it")
                    sneak = random.randint(1,20) + activePlayer.playerAgl
                    if sneak >= 15:
                        print("You snuck passed it! You got its dragon egg!")
                        activePlayer.gainItem("dragon_egg")
                    else:
                        print("You tripped on a stone and woke it up!")
                        print("You Encountered an Enemy!")
                        gameCombat("dragon")
                        if activePlayer.healthCheck()==False:
                            print("You got the dragon's egg")
                            activePlayer.gainItem("dragon_egg")
                        else:
                            print("You lost....")                        
                        
    elif gameMap[playerPosY][playerPosX]== "Witch":
        print("\nYou found the Witch's Hut!")
        while userDecisions!="0" and userDecisions!="1":
            userDecisions = input("Do you attack directly or stratagize?(1 to attack)(0 to think): ")
            match userDecisions:
                case "1":
                    print("You barge in and attack!")
                    print("You Encountered an Enemy!")
                    gameCombat("witch")
                    if activePlayer.healthCheck()==False:
                        print("You got the witch's finger")
                        activePlayer.gainItem("witch_finger")
                    else:
                        print("You lost....")
                case "0":
                    print("You try to think of ways to beat the witch without a direct encounter")
                    think = random.randint(1,20) + activePlayer.playerInt
                    if think >= 15:
                        print("You discover that the witch's hut is not made of stone, it's made of thatch. Time to ignite!")
                        print("The witch and her hut turn into a giant bonfire\n You got the witch's finger")
                        activePlayer.gainItem("witch_finger")
                    else:
                        print("You decided to lure it outside!")
                        print("You Encountered an Enemy!")
                        gameCombat("witch")
                        if activePlayer.healthCheck()==False:
                            print("You got the witch's finger")
                            activePlayer.gainItem("witch_finger")
                        else:
                            print("You lost....")
    elif gameMap[playerPosY][playerPosX]== "Temple":
        print("You found the Kraken's Temple!")
        while userDecisions!="0" and userDecisions!="1":
            userDecisions = input("The kraken speaks to you in your mind: 'I can let you leave this island if you leave me be'?(1 to attack)(0 to leave): ")
            match userDecisions:
                case "1":
                    print("You attack!")
                    print("You Encountered an Enemy!")
                    gameCombat("kraken")
                    if activePlayer.healthCheck()==False:
                        print("You got the kraken's orb")
                        activePlayer.gainItem("kraken_orb")
                    else:
                        print("You lost....")
                case "0":
                    print("You decide that this place isn't worth it.")
                    ending = 1
                    gameover = True

    elif gameMap[playerPosY][playerPosX]== "Sinkhole":
        print("\nThe floor crumbles underneath you and you fall into the sandworm's lair")
        print("You Encountered an Enemy!")
        gameCombat("sandworm")
        if activePlayer.healthCheck()==False:
            print("You got the sandworm's carcass")
            activePlayer.gainItem("sandworm_carcass")
        else:
            print("You lost....")

                    
                    
    #Enemy/encounter
    else:
        if randomNumber == 1:
            print("\nYou Encountered an Enemy!")
            gameCombat(enemies[random.randint(0,5)])
            
        elif randomNumber == 2:
            print("\nYou see something ahead of you...")
            gameEncounter()


# In[288]:


def gameCombat(enemy):
    #turn based combat
    global activePlayer
    global gameover
    global userInput
    newEnemy = battleFoe(enemy)
    newEnemy.setStats()
    print(f"COMBAT START!\n You are fighting a {newEnemy.enemyName}")
    combatInProgress=True
    speedContest = 1
    if (random.randint(1,20) + newEnemy.enemyAgl) >= (random.randint(1,20) + activePlayer.playerAgl):
        speedContest = 0
    while(combatInProgress==True):
        match speedContest:
            #when enemy is faster
            case 0:
                print(f"Its {newEnemy.enemyName}'s Turn")
                #attack accuarcy = 1 - agl/10
                if newEnemy.attack(activePlayer.playerAgl):
                    #chance for crit
                    attackType = random.randint(1,10)
                    enemyDmg = -1*random.randint(1,3)*newEnemy.enemyAtk
                    if attackType == 10:
                        print(f"CRIT! You took {5*abs(enemyDmg)} damage\n")
                        activePlayer.heal(5*enemyDmg)
                    else:
                        print(f"Hit! You took {abs(enemyDmg)} damage\n")
                        activePlayer.heal(enemyDmg)
                    if activePlayer.healthCheck():
                        print("You suffered lethal damage!")
                        combatInProgress = False
                else:
                    print("They missed!\n")
                    
                if combatInProgress == True:
                    print(f"Its {activePlayer.playerClass}'s Turn")
                    userInput = ""
                    while userInput !="1"  and userInput !="2" and userInput !="3":
                        userInput = input("What do you wish to do? Attack(1), Heal(2), Run(3): ")
                        match userInput:
                            case "1":
                                #attack accuarcy = 1 - agl/10
                                if activePlayer.attack(newEnemy.enemyAgl):
                                #chance for crit
                                    attackType = random.randint(1,10)
                                    playerDmg = -1*random.randint(1,3)*activePlayer.playerWpn
                                    if attackType == 10:
                                        print(f"CRIT! You dealt {5*abs(playerDmg)} damage\n")
                                        newEnemy.heal(5*playerDmg)
                                    else:
                                        print(f"Hit! You dealt {abs(playerDmg)} damage\n")
                                        newEnemy.heal(1*playerDmg)
                                    if newEnemy.healthCheck():
                                        print("You have slayed the creature!")
                                        activePlayer.gainXP(newEnemy.enemyXP,newEnemy.enemyMoney)
                                        combatInProgress = False
                                else:
                                    print("You missed!")
                            #attempt to heal
                            case "2":
                                if "Ration" in activePlayer.playerInventory:
                                    activePlayer.loseItem("Ration")
                                    print(f"You healed: {10+activePlayer.playerCon}")
                                    activePlayer.heal(10+activePlayer.playerCon)
                                else:
                                    print("You have no rations! You wasted your time!\n")
                            #attempt to run              
                            case "3":
                                print("You try to GTFO")
                                if (random.randint(1,20) + newEnemy.enemyAgl) <= (random.randint(1,20) + activePlayer.playerAgl):
                                    print("You escaped!\n")
                                    combatInProgress = False
                                else:
                                    print("You couldn't lose the creature")
                    
            #when player is faster
            case 1:
                print(f"Its {activePlayer.playerClass}'s Turn")
                userInput = ""
                while userInput !="1"  and userInput !="2" and userInput !="3":
                    userInput = input("What do you wish to do? Attack(1), Heal(2), Run(3): ")
                    match userInput:
                        case "1":
                            #attack accuarcy = 1 - agl/10
                            if activePlayer.attack(newEnemy.enemyAgl):
                            #chance for crit
                                attackType = random.randint(1,10)
                                playerDmg = -1*random.randint(1,3)*activePlayer.playerWpn
                            
                                if attackType == 10:
                                    print(f"CRIT! You dealt {5*abs(playerDmg)} damage\n")
                                    newEnemy.heal(5*playerDmg)
                                else:
                                    print(f"Hit! You dealt {abs(playerDmg)} damage\n")
                                    newEnemy.heal(1*playerDmg)
                                if newEnemy.healthCheck():
                                    print("You have slayed the creature!")
                                    activePlayer.gainXP(newEnemy.enemyXP,newEnemy.enemyMoney)
                                    combatInProgress = False
                            else:
                                print("You missed!")
                        #attempt to heal
                        case "2":
                            if "Ration" in activePlayer.playerInventory:
                                activePlayer.loseItem("Ration")
                                print(f"You healed: {10+activePlayer.playerCon}")
                                activePlayer.heal(10+activePlayer.playerCon)
                            else:
                                print("You have no rations! You wasted your time!\n")
                        #attempt to run              
                        case "3":
                            print("You try to GTFO")
                            if (random.randint(1,20) + newEnemy.enemyAgl) <= (random.randint(1,20) + activePlayer.playerAgl):
                                print("You escaped!\n")
                                combatInProgress = False
                            else:
                                print("You couldn't lose the creature")
                if combatInProgress == True:
                    print(f"Its {newEnemy.enemyName}'s Turn")
                    #Enemy turn
                    #attack accuarcy = 1 - agl/10
                    if newEnemy.attack(activePlayer.playerAgl):
                        #chance for crit
                        attackType = random.randint(1,10)
                        enemyDmg = -1*random.randint(1,3)*newEnemy.enemyAtk
                        if attackType == 10:
                            print(f"CRIT! You took {5*abs(enemyDmg)} damage\n")
                            activePlayer.heal(5*enemyDmg)
                        else:
                            print(f"Hit! You took {abs(enemyDmg)} damage\n")
                            activePlayer.heal(enemyDmg)
                        if activePlayer.healthCheck():
                            print("You suffered lethal damage!")
                            combatInProgress = False
                    else:
                        print("They missed!")

    gameover = activePlayer.healthCheck()                    
                
    
    


# In[289]:


def gameEncounter():
    #Encounters
    global userInput
    global activePlayer
    userInput =''
    randEnc = random.randint(1,5)
    match randEnc:
        case 1:
            print("A peddler comes your way")
            while userInput !="1" and userInput!="0":
                userInput = input("Want to play a coin game? Gain double your money or lose it all(1 play) (0 leave): ")
                match userInput:
                    case "1":
                        if random.randint(1,2)==2:
                            print("YOU WINN!!!!!!")
                            activePlayer.playerMoney = activePlayer.playerMoney*2
                            print(f"Your new balance is: {activePlayer.playerMoney}")
                        else:
                            print("AHAHHAHAHAAH YOU LOST")
                            activePlayer.playerMoney = activePlayer.playerMoney*0
                            print(f"Your new balance is: {activePlayer.playerMoney}")
                    case "0":
                        print("you leave the scam")
        case 2:
            print("A traveler comes your way")
            while userInput !="1" and userInput!="0":
                userInput = input("Want to play a cup game? One is poison, one is not (1 play) (0 leave): ")
                match userInput:
                    case "1":
                        if random.randint(1,2)==2:
                            print("You feel healed!")
                            activePlayer.heal(15+activePlayer.playerCon)
                        else:
                            print("THAT WAS POISON!")
                            activePlayer.heal(-15+activePlayer.playerCon)
                    case "0":
                        print("you leave, not taking the chance")
        case 3:
            print("Bandits block your path!")
            while userInput !="1" and userInput!="0" and userInput!="2":
                userInput = input("Pay 5g or suffer (0 pay) (1 fight) (2 convince): ")
                match userInput:
                    case "2":
                        if (random.randint(1,20) + 2) <= (random.randint(1,20) + activePlayer.playerInt):
                            print("You manage to convince them that you are a new recruit just passing by")
                        else:
                            print("WHAT THE HELL?? YOU THINK WE'RE STUPID????")
                            gameCombat("bandit")
                    case "1":
                        print("Tough guy, huh. We'll teach you a lesson")
                        gameCombat("bandit")
                    case "0":
                        if activePlayer.playerMoney >= 5:
                            activePlayer.playerMoney = activePlayer.playerMoney - 5
                            print(f"pay, not willing to fight with them\nMoney: {activePlayer.playerMoney}")
                            
                        else:
                            print("YOURE BROKE AS HELL!!!!")
                            gameCombat("bandit")
        case 4:
            print("A lady calls for your help in the distance")
            while userInput !="1" and userInput!="0" and userInput!="2":
                userInput = input("Approach? (2 think) (1 help) (0 leave): ")
                match userInput:
                    case "2":
                        if (15 <= (random.randint(1,20) + activePlayer.playerInt)):
                            print("You recognize this as a trap and go the other direction\n You find some money along the way")
                            activePlayer.playerMoney = activePlayer.playerMoney+50
                            print(f"Money: {activePlayer.playerMoney}")
                        else:
                            print("Your thinking allows the creature to attack you")
                            gameCombat("goblin")
                    case "1":
                        print("You go towards the lady and feel a prick on your back")
                        print("You lose conciousness")
                        print("When you reawaken you realize you have lost money!")
                        activePlayer.playerMoney = activePlayer.playerMoney/2
                        print(f"Money: {activePlayer.playerMoney}")
                    case "0":
                        print("you leave, not taking the chance")
        case 5:
            print("A lady calls for your help in the distance")
            while userInput !="1" and userInput!="0" and userInput!="2":
                userInput = input("Approach? (2 think) (1 help) (0 leave): ")
                match userInput:
                    case "2":
                        if (15 <= (random.randint(1,20) + activePlayer.playerInt)):
                            print("You see creatures hidden in the environment and decide to scare them off with a howl\n She rewards you for the help")
                            activePlayer.playerMoney = activePlayer.playerMoney+20
                            print(f"Money: {activePlayer.playerMoney}")
                        else:
                            print("Your thinking allows the creature to attack her. Killing her on sight")
                            gameCombat("goblin")
                    case "1":
                        print("You go towards the lady and see the hidden creatures flee.\n She rewards you for the help")
                        activePlayer.playerMoney = activePlayer.playerMoney+20
                        print(f"Money: {activePlayer.playerMoney}")
                    case "0":
                        print("you leave, not taking the chance")


# In[290]:


def saveGame(savePlayer):
    global playerPosX
    global playerPosY
    global playerCordX
    global playerCordY
    #creates a save file with all of the user's stats and position
    saveFile = open("saveData.txt", "w") 
    #adds everything that the player knows
    saveFile.write(f"{playerPosX}\n")
    saveFile.write(f"{playerPosY}\n")
    saveFile.write(f"{playerCordX}\n")
    saveFile.write(f"{playerCordY}\n")
    for count in savePlayer.toString().split():
        saveFile.write(f"{count}\n")
    saveFile.close()
    print("save complete")

def loadGame(saveFile):
    global activePlayer
    global playerPosX
    global playerPosY
    global playerCordX
    global playerCordY    
    #uses the save file to load the game
    loadFile = open("saveData.txt", "r") 
    filelist = loadFile.readlines()
    #convert everything back to numbers/list
    playerPosX = eval(filelist[0])
    playerPosY = eval(filelist[1])
    playerCordX = eval(filelist[2])
    playerCordY = eval(filelist[3])
    activePlayer = Player(filelist[4].strip())
    inventory = eval(filelist[15]+filelist[16]+filelist[17]+filelist[18]+filelist[19])
    activePlayer.setStats(eval(filelist[5]),eval(filelist[6]),eval(filelist[7]),eval(filelist[8]),eval(filelist[9]),eval(filelist[10]),eval(filelist[11]),eval(filelist[12]),eval(filelist[13]),eval(filelist[14]),inventory)
    loadFile.close()
    print(f"Player Loaded: {activePlayer.playerClass} with \n{activePlayer.playerAtk} Atk, \n{activePlayer.playerAgl} Agl, \n{activePlayer.playerInt} Int, \n{activePlayer.playerCon} Con, \n{activePlayer.playerCha} Cha, \n{activePlayer.playerHP} HP, \n{activePlayer.playerXP} XP, \n{activePlayer.playerLV} LV, \n{activePlayer.playerMoney} Money, \n{activePlayer.playerQuest} Quests Done, \n{activePlayer.playerInventory} Items")


# In[291]:


#Player class
class Player:
    #Random stat generation
    playerAtk = random.randint(-2, 5)
    playerAgl = random.randint(-2, 5)
    playerInt = random.randint(-2, 5)
    playerCon = random.randint(-2, 5)
    playerCha = random.randint(-2, 5)
    playerHP = 20 + (playerCon * 5)
    playerXP = 0
    playerLV = 1
    playerMoney = 0
    playerQuest = 0
    playerInventory=["","","","",""]
    playerAbilities=[]
    playerWpn = 0
    #Set basic class
    def __init__(self, playerClass):
        self.playerClass = playerClass
        
    #This makes sure that your attack stat isnt negative at the start of the game
    def starterBuff(self):
        if self.playerClass =="archer" and self.playerAgl <= 0:
            self.playerAgl = 1
        if self.playerClass =="barbarian" and self.playerAtk <= 0:
            self.playerAtk = 1
        if self.playerClass =="wizard" and self.playerInt <= 0:
            self.playerInt = 1
            
    #this is basically the attack stat for classes
    def setWpn(self):
        if self.playerClass =="archer":
            self.playerWpn = self.playerAgl
        elif self.playerClass =="barbarian":
            self.playerWpn = self.playerAtk
        elif self.playerClass =="wizard":
            self.playerWpn = self.playerInt
            
    #loads stats
    def setStats(self, atkStat, aglStat, intStat, conStat, chaStat, hpStat, xpStat, lvStat, moneyStat, questStat, inventoryStat):
        self.playerAtk = atkStat
        self.playerAgl = aglStat
        self.playerInt = intStat
        self.playerCon = conStat
        self.playerCha = chaStat
        self.playerHP = hpStat
        self.playerXP = xpStat
        self.playerLV = lvStat
        self.playerMoney = moneyStat
        self.playerQuest = questStat
        self.playerInventory = inventoryStat
        self.setWpn()
    
    def gainXP(self,encounterXP,encounterMoney):
        #gain xp from encounter
        print(f"You gained {encounterXP} XP")
        self.playerXP = self.playerXP + encounterXP
        print(f"You gained {encounterMoney} Gold")
        self.playerMoney = self.playerMoney + encounterMoney
        print(f"Current Money: {self.playerMoney}g")
        self.checkLevelUp()
    
    def checkLevelUp(self):
        #Levels up if player has enough XP
        if self.playerXP >= ((self.playerLV+1)*(self.playerLV)*500):
            self.playerLV = self.playerLV+1
            self.playerCon = self.playerCon+1
            if self.playerClass == "archer":
                self.playerAgl = self.playerAgl+1
                self.playerWpn = self.playerAgl
            if self.playerClass == "barbarian":
                self.playerAtk = self.playerAtk+2
                self.playerWpn = self.playerAtk
            if self.playerClass == "wizard":
                self.playerInt = self.playerInt+1
                self.playerWpn = self.playerInt
            print(f"You Leveled Up! You are now Level {self.playerLV} and have become stronger")
        else:
            print(f"The XP required for a level up is {(self.playerLV+1)*(self.playerLV)*500}, you have {self.playerXP}")
    def gainItem(self,playerItem):
        #puts the item gained into the inventory slot the player wants
        #uses recursion if players wants to juggle inventory
        userInput = input(f"what slot do you want to put this item in?(1-5) Input anything else to discard\n Here is your current inventory:|{self.playerInventory[0]}|{self.playerInventory[1]}|{self.playerInventory[2]}|{self.playerInventory[3]}|{self.playerInventory[4]}|: ")
        match userInput:
            case "1":
                oldItem = self.playerInventory[0]
                self.playerInventory[0] = playerItem
                if oldItem !="":
                    userInput = input(f"Do you want to keep {oldItem}?(Y/N): ")
                    if userInput.lower() == "y":
                        self.gainItem(oldItem)
                    else:
                        print(f"{oldItem} discarded")
                
            case "2":
                oldItem = self.playerInventory[1]
                self.playerInventory[1] = playerItem
                if oldItem !="":
                    userInput = input(f"Do you want to keep {oldItem}?(Y/N): ")
                    if userInput.lower() == "y":
                        self.gainItem(oldItem)
                    else:
                        print(f"{oldItem} discarded")
                    
            case "3":
                oldItem = self.playerInventory[2]
                self.playerInventory[2] = playerItem
                if oldItem !="":
                    userInput = input(f"Do you want to keep {oldItem}?(Y/N): ")
                    if userInput.lower() == "y":
                        self.gainItem(oldItem)
                    else:
                        print(f"{oldItem} discarded")
            case "4":
                oldItem = self.playerInventory[3]
                self.playerInventory[3] = playerItem
                if oldItem !="":
                    userInput = input(f"Do you want to keep {oldItem}?(Y/N): ")
                    if userInput.lower() == "y":
                        self.gainItem(oldItem)
                    else:
                        print(f"{oldItem} discarded")
            case "5":
                oldItem = self.playerInventory[4]
                self.playerInventory[4] = playerItem
                if oldItem !="":
                    userInput = input(f"Do you want to keep {oldItem}?(Y/N): ")
                    if userInput.lower() == "y":
                        self.gainItem(oldItem)
                    else:
                        print(f"{oldItem} discarded")
            case _:
                print(f"{playerItem} has been discarded and lost")
        if playerItem == "Armor":
            self.armorCheck()
                
    def toString(self):
        #return everything the player knows
        return f"{self.playerClass} {self.playerAtk} {self.playerAgl} {self.playerInt} {self.playerCon} {self.playerCha} {self.playerHP} {self.playerXP} {self.playerLV} {self.playerMoney} {self.playerQuest} {self.playerInventory}"
            
                
    def heal(self, numberHealth):
        self.playerHP = self.playerHP + numberHealth
        self.healthCheck()
        print(f"you are at {self.playerHP} health")
        
    def armorCheck(self):
        if "Armor" in self.playerInventory:
            self.playerCon = self.playerCon + 2
        else:
            self.playerCon = self.playerCon - 2
        
    def healthCheck(self):
        #detemine if dead
        if self.playerHP > (20 + (self.playerCon*5)):
            self.playerHP = (20 + (self.playerCon*5))
            return False
        elif self.playerHP <=0:
            self.playerHP = 0
            return True
        else:
            return False
    def questComp(self):
        self.playerQuest=self.playerQuest+1
        print("QUEST COMPLETE")

    #returns true if hits target
    def attack(self,accuracy):
        #1-agl/10
        randHit = random.randint(1,10)/10.0
        if randHit>=(accuracy/15.0):
            return True
        else:
            return False
        
        
    def loseItem(self, playerItem):
        itemLoc = self.playerInventory.index(playerItem)
        self.playerInventory[itemLoc] = ""
        if playerItem == "Armor":
            self.armorCheck()


# In[292]:


class battleFoe:
    #Random stat generation for enemies
    enemyAtk = random.randint(1, 4)
    enemyAgl = random.randint(-3, 3)
    enemyInt = random.randint(-3, 3)
    enemyCon = random.randint(-3, 3)
    enemyHP = 16 + (enemyCon * 5)
    enemyXP = random.randint(1,3)*200
    enemyMoney = random.randint(0,4)*15

    #Set basic class
    def __init__(self, enemyName):
        self.enemyName = enemyName
        
        
    #loads stats depending if its a boss
    def setStats(self):
        if(self.enemyName =="dragon"):
            self.enemyAtk = 15
            self.enemyAgl = 8
            self.enemyCon = 15
            self.enemyHP = 16 + (self.enemyCon * 5)
            self.enemyXP = 10000
        if(self.enemyName =="witch"):
            self.enemyAtk = 5
            self.enemyAgl = 6
            self.enemyCon = 5
            self.enemyHP = 16 + (self.enemyCon * 5)
            self.enemyXP = 2500
        if(self.enemyName =="sandworm"):
            self.enemyAtk = 7
            self.enemyAgl = 5
            self.enemyCon = 7
            self.enemyHP = 16 + (self.enemyCon * 5)
            self.enemyXP = 2500
        if(self.enemyName =="Kraken"):
            self.enemyAtk = 10
            self.enemyAgl = 8
            self.enemyCon = 10
            self.enemyHP = 16 + (self.enemyCon * 5)
            self.enemyXP = 5000
            
    def heal(self, numberHealth):
        self.enemyHP = self.enemyHP + numberHealth
        self.healthCheck()
        print(f"Enemy is at {self.enemyHP} health")
        
    def healthCheck(self):
        #detemine if dead
        if self.enemyHP > (20 + (self.enemyCon*5)):
            self.enemyHP = (20 + (self.enemyCon*5))
            return False
        elif self.enemyHP <=0:
            self.enemyHP = 0
            return True
        else:
            return False

    #returns true if hits target
    def attack(self,accuracy):
        #1-agl/10
        randHit = random.randint(1,10)/10.0
        if randHit>=(accuracy/15.0):
            return True
        else:
            return False


# In[ ]:





# In[236]:


main()


# In[ ]:




