import requests

while True:
  url_input = input('Please write a URL or URLs you want to check. (separated by comma)\n')

  small_input = url_input.lower()
  no_space_input = small_input.replace(' ','')
  split_input = no_space_input.split(',')

  for url in split_input:
    num = url.find('http')
    if(num == -1):
      url = 'https://' + url
    try:
      result = requests.get(url)
      if(result.status_code == 200):
        print(url + ' is up!')
      elif (result.status_code == 404):
        print(url + ' is down!')
    except:
      print('invalid url')

  while True:
    terminate_input = input('Do you want to start over? ')
    if terminate_input == 'y':
      break
    else:
      if terminate_input == 'n':
        print('OK, bye!')
        quit()
      else:
        print('Thats not a invaild answer')
        continue