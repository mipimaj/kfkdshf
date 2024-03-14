from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import asyncio
import random
import requests
import json

identifiant = "gelani"
mot_de_passe = ""
mise = [0.1, 0.3, 0.8, 2.4, 7.2]
# mise = [0.1, 0.205, 0.42, 0.861, 1.766, 3.62, 7,42, 15.22]
duration = 36000
nombreSuccessive = 8

webhook = ""
numberClock = 0
color = ""
mise_i = 0
rendement = 0
chooseColor = random.randint(0, 1)
countColor = 0
partie = 0
perteMax = 0
timePlay3min = 0

winMise1 = 0
winMise2 = 0
winMise3 = 0
winMise4 = 0
winMise5 = 0
winMise6 = 0
winMise7 = 0
winMise8 = 0

looseMise1 = 0
looseMise2 = 0
looseMise3 = 0
looseMise4 = 0
looseMise5 = 0
looseMise6 = 0
looseMise7 = 0
looseMise8 = 0

redColorSameLance = 0
greenColorSameLance = 0

isActive = False


lien = "https://m.xtb-usdt.com/game/guessMain?gameName=RG1M&returnUrl=%2Fhome"

options = Options()

mobile_emulation = {
   "deviceMetrics": {"width": 540, "height": 900, "pixelRatio": 3.0},
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
}

options.add_experimental_option("mobileEmulation", mobile_emulation)


driver = webdriver.Chrome(
   service=ChromeService(ChromeDriverManager().install()),
   options=options
   )


driver.get(lien)

time.sleep(10)

username_field = driver.find_element(By.CSS_SELECTOR, '[placeholder="Please enter the username"]')
username_field.send_keys(identifiant)

password_field = driver.find_element(By.CSS_SELECTOR, '[placeholder="Please enter the password"]')
password_field.send_keys(mot_de_passe)

time.sleep(2)

button = driver.find_element(By.CLASS_NAME, 'loginBtn')
button.click()

time.sleep(10)

driver.get(lien)

def time_string_to_seconds(timestring):
   pt = datetime.strptime(timestring, '%H:%M:%S')

   total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
   return total_seconds

time.sleep(15)

No = driver.find_elements(By.CLASS_NAME, 'issue')
wallet = driver.find_element(By.CLASS_NAME, 'balance')
start_wallet = wallet.text
print(No[0].text)
print(No[0].text[10:])

# def loopToGetNumber50or100():
#    global No
#    IsActive = False
#    for i in range(0, 1000, 50):
#       if i != 1000 and i != 50:
#          if str(i) == str(No[0].text[10:]):
#             print("le script commence au No " + str(i))
#             IsActive = True
#             break
#       else:
#          count_i = "000" if i == 1000 else "050"
#          if str(count_i) == str(No[0].text[10:]):
#             print("le script commence au No " + str(i))
#             IsActive = True
#             break
   
#    time.sleep (3)

#    if IsActive == False:
#       print("en attente No actuelle: " + str(No[0].text[10:]))
#       loopToGetNumber50or100()

data = {
      "content": "Le script vient d'être executer ! (voir les résultat de vos mises en dessous de ce message)"
   }

response = requests.post(webhook, json=data)

def sendDataToDiscordWebhook(winOrLoose):
   global webhook
   data = {
      "username": "Data Mise",
      "embeds": [
         {
               "title": "Statistiques de Mises",
               "description": "Voici les statistiques de vos mises :",
               "fields": [
                  {"name": "Nombre de partie jouer au total", "value": f"{partie}", "inline": False},
                  {"name": "Partie actuelle", "value": f"{str(No[1].text)}\nCouleur selectionnée: {color}\n{winOrLoose}\nprochaine mise: {str(mise[mise_i])}", "inline": False},
                  {"name": "Mises gagnantes", "value": f"Mise 1: {round(winMise1, 3)}\nMise 2: {round(winMise2, 3)}\nMise 3: {round(winMise3, 3)}\nMise 4: {round(winMise4, 3)}\nMise 5: {round(winMise5, 3)}\nMise 6: {round(winMise6, 3)}\nMise 7: {round(winMise7, 3)}\nMise 8: {round(winMise8, 3)}", "inline": False},
                  {"name": "Mises perdues", "value": f"Mise 1: {round(looseMise1, 3)}\nMise 2: {round(looseMise2, 3)}\nMise 3: {round(looseMise3, 3)}\nMise 4: {round(looseMise4, 3)}\nMise 5: {round(looseMise5, 3)}\nMise 6: {round(looseMise6, 3)}\nMise 7: {round(looseMise7, 3)}\nMise 8: {round(looseMise8, 3)}", "inline": False},
                  {"name": "Rendement", "value": f"{rendement:.2f} USDT", "inline": False},
                  {"name": "Wallet au début de l'execution", "value": f"{start_wallet}", "inline": False},
                  {"name": "Wallet actuellement", "value": f"{wallet.text}", "inline": False}
               ],
               "color": 0x03b2f8
         }
      ]
   }

   # Envoie l'embed via le webhook
   response = requests.post(webhook, json=data)

   if response.status_code == 204:
      pass
      # print("Webhook envoyé avec succès !")
   else:
      pass
      # print(f"Erreur lors de l'envoi du webhook. Code de réponse : {response.status_code}")


async def stopBot():
   global duration, isActive
   for i in range(0, duration):
      if i + 1 == duration:
         if isActive == True:
            for i in range(380):
               if isActive == False:
                  driver.close()
                  exit()
         else:
            driver.close()
            exit()
      await asyncio.sleep(1)

async def obtenir_temps():
   global chooseColor, numberClock, timePlay3min
   timeclock = driver.find_element(By.CLASS_NAME, 'timeBar')
   numberClock = time_string_to_seconds(timeclock.text)
   for i in range(9000000):
      if numberClock >= 1:
         numberClock -= 1
      else:
         timeclock = driver.find_element(By.CLASS_NAME, 'timeBar')
         numberClock = time_string_to_seconds(timeclock.text)
         # if timePlay3min == 3:
         #    pass
         # else:
         #    timePlay3min += 1
         #    print(timePlay3min)
      await asyncio.sleep(1)

def winRate():
   global winMise1, winMise2, winMise3, winMise4, winMise5, winMise6, mise

   if mise[mise_i] == mise[0]:
      winMise1 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[1]:
      winMise2 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[2]:
      winMise3 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[3]:
      winMise4 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[4]:
      winMise5 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[5]:
      winMise6 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[6]:
      winMise7 += (mise[mise_i] * 1.95) - mise[mise_i]
   elif mise[mise_i] == mise[7]:
      winMise8 += (mise[mise_i] * 1.95) - mise[mise_i]

def looseRate():
   global looseMise1, looseMise2, looseMise3, looseMise4, looseMise5, looseMise6, mise

   if mise[mise_i] == mise[0]:
      looseMise1 += mise[mise_i]
   elif mise[mise_i] == mise[1]:
      looseMise2 += mise[mise_i]
   elif mise[mise_i] == mise[2]:
      looseMise3 += mise[mise_i]
   elif mise[mise_i] == mise[3]:
      looseMise4 += mise[mise_i]
   elif mise[mise_i] == mise[4]:
      looseMise5 += mise[mise_i]
   elif mise[mise_i] == mise[5]:
      looseMise6 += mise[mise_i]
   elif mise[mise_i] == mise[6]:
      looseMise7 += mise[mise_i]
   elif mise[mise_i] == mise[7]:
      looseMise8 += mise[mise_i]

async def perteMaxUpdate():
   global rendement, perteMax
   for i in range(100000000):
      await asyncio.sleep(1800)
      if perteMax < rendement:
         if rendement > 1:
            perteMax = rendement
      await asyncio.sleep(1800)

async def autre_partie_du_programme():
   global perteMax, start_wallet, wallet, partie, chooseColor, countColor, rendement, mise, mise_i, color, numberClock, timePlay3min, redColorSameLance, greenColorSameLance, nombreSuccessive, isActive, No
   showSold = False
   winActive = False
   looseActive = False
   for i in range(18000000):
      # print(numberClock)
      if numberClock == 40:
         
         redCircle = driver.find_element(By.CSS_SELECTOR, '#redCircle')
         # print(redCircle.get_attribute("style"))

         greenCircle = driver.find_element(By.CSS_SELECTOR, '#greenCircle')
         # print(greenCircle.get_attribute("style"))

         purpleCircle = driver.find_element(By.CLASS_NAME, 'purpleCircle')
         # print(purpleCircle.get_attribute("style"))

         if greenColorSameLance > nombreSuccessive: # pour rouge
            if redCircle.get_attribute("style") == "display: block;":
               print("gagner: " + str((mise[mise_i] * 1.95) - mise[mise_i]))
               rendement = rendement + ((mise[mise_i] * 1.95) - mise[mise_i])
               redColorSameLance = 0
               greenColorSameLance = 0
               isActive = False
               countColor = 0
               winActive = True
               winRate()
               

               mise_i = 0

               showSold = True
            else:
               print("perdu: " + str(mise[mise_i]))
               rendement = rendement - mise[mise_i]
               looseRate()
               showSold = True
               looseActive = True

               if mise_i <= len(mise) - 2:
                  mise_i += 1
               else:
                  mise_i = 0


         if redColorSameLance > nombreSuccessive: # pour vert
            if greenCircle.get_attribute("style") == "display: block;":
               print("gagner: " + str((mise[mise_i] * 1.95) - mise[mise_i]))
               rendement = rendement + ((mise[mise_i] * 1.95) - mise[mise_i])
               greenColorSameLance = 0
               redColorSameLance = 0
               isActive = False
               countColor = 0
               winActive = True
               winRate()

               mise_i = 0

               showSold = True
            else:
               print("perdu: " + str(mise[mise_i]))
               rendement = rendement - mise[mise_i]
               looseRate()
               showSold = True
               looseActive

               if mise_i <= len(mise) - 2:
                  mise_i += 1                 
               else:
                  mise_i = 0
         
         if showSold == True:
            print("Totale gagné: " + str(round(rendement, 3)))
            print(str(No[1].text))
            print("Solde du wallet: " + wallet.text)
            print("prochaine mise: " + str(mise[mise_i]))
            if winActive == True:
               sendDataToDiscordWebhook(f'gagner: {str((mise[mise_i] * 1.95) - mise[mise_i])}')
            elif looseActive == True:
               sendDataToDiscordWebhook(f'perdu: {str(mise[mise_i])}')
            showSold = False

         if isActive == False:
            if redCircle.get_attribute("style") == "display: block;":
               redColorSameLance += 1
               greenColorSameLance = 0
               print(".")
               print("Couleur rouge d'affiler: " + str(redColorSameLance))

            if greenCircle.get_attribute("style") == "display: block;":
               greenColorSameLance += 1
               redColorSameLance = 0
               print(".")
               print("Couleur verte d'affiler: " + str(greenColorSameLance))

         # isActive = True

      if numberClock == 30:
         if rendement <= perteMax - 5:
            print("Script arrété trop de perte !")
            print("Wallet au début du script: " + start_wallet)
            print("Wallet à la fin du script: " + wallet.text)
            exit()
         
         if redColorSameLance > nombreSuccessive or greenColorSameLance > nombreSuccessive:
            partie += 1
            print(".")
            print(".")
            print("Partie N°" + str(partie))
            color = "red" if chooseColor == 0 else "green"
            # color = "green"
            if redColorSameLance > nombreSuccessive:
               greenButton = driver.find_elements(By.CLASS_NAME, 'betDiv')
               greenButton[2].click()
               color = "green"
               isActive = True
            if greenColorSameLance > nombreSuccessive:
               redButton = driver.find_elements(By.CLASS_NAME, 'betDiv')
               redButton[0].click()
               color = "red"
               isActive = True

            if isActive == True:
               time.sleep(1)

               inputAmount = driver.find_element(By.CSS_SELECTOR, '[placeholder="Amount Per Option"]')
               inputAmount.send_keys(str(mise[mise_i]))

               time.sleep(1)

               confirmButton = driver.find_element(By.CLASS_NAME, 'betBtn')
               confirmButton.click()

               time.sleep(2)

               reConfirmButton = driver.find_element(By.CLASS_NAME, 'btn-submit')
               reConfirmButton.click()

               time.sleep(1)

            print("Couleur selectionnée: " + color)

            # isActive = False

      await asyncio.sleep(1)

async def main():
   # loopToGetNumber50or100()
   task1 = asyncio.create_task(obtenir_temps())
   task2 = asyncio.create_task(autre_partie_du_programme())
   task3 = asyncio.create_task(perteMaxUpdate())
   task4 = asyncio.create_task(stopBot())
   await task1
   await task2
   await task3
   await task4

loop = asyncio.get_event_loop()
loop.run_until_complete(main())