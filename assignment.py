import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"
page = requests.get(url)
soup_result = BeautifulSoup(page.text, "html.parser")

currency = soup_result.find_all("td")
currency_list = []
for value in currency:
  currency_list.append(value.string)

country_list = []
for i in range(0, len(currency_list)):
  if i % 4 == 1:
    country_list.append(currency_list[i-1].capitalize())

# 개선필요
del country_list[8]
del country_list[181]
del country_list[219]

code_list = []      
for i in range(0, len(currency_list)):
    if i % 4 == 1:
      if not currency_list[i+1] == None:
        code_list.append(currency_list[i+1]) 

def main():
  print('Hello! Please choose select a country by number:')
  for i in range(0, len(country_list)):
    print('# '+str(i)+' '+country_list[i])
  get_input()

def get_input():
  user_input = input('#: ')
  try:
    user_input = int(user_input)
    is_int = True
  except ValueError:
    is_int = False
    
  if is_int == True:
    if -1 < user_input and user_input < len(country_list):
      print("You chose "+country_list[user_input])
      print("The currency code is "+get_code(user_input))
    else:
      print("Choose a number from the list.")
      get_input()
  else: 
    print("That wasn't a number.")
    get_input()

def get_code(user_input):
  return code_list[user_input]

main()