import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

brands_request = requests.get(alba_url)
brands_soup = BeautifulSoup(brands_request.text, "html.parser")

def export_csv (job_list,company):
  file = open(company+'.csv',mode="w")
  writer = csv.writer(file)
  writer.writerow(["place","title","time","pay","date"])
  
  for job in job_list:
    writer.writerow(list(job.values()))
  return  

def get_total_count_URL(url):
  total_count_request = requests.get(url)
  total_count_soup = BeautifulSoup(total_count_request.text,"html.parser")
  total_count = total_count_soup.find("p",{"class":"jobCount"}).find("strong").string
  print('totalcount:'+total_count)
  request_url = url + 'job/brand/?pagesize=' + total_count.replace(',','')
  return request_url

def get_job(alba_list):
  job_list = []
  for job in alba_list:
    place = job.find('td',{"class":"local first"}).get_text().replace('\xa0',' ')
    company = job.find('span',{"class":"company"}).get_text()
    working_time = job.find('td',{"class":"data"}).get_text()
    pay = job.find('span',{"class":"number"}).get_text()
    reg_date = job.find('td', {"class":"regDate"}).get_text()

    job_list.append({
      'place': place,
      'title': company,
      'time' : working_time,
      'pay'  : pay,
      'date' : reg_date
    })
  return job_list  
  

def main():
  brands = brands_soup.find("div",{"id":"MainSuperBrand"}).find_all("a", {"class":"goodsBox-info"})

  for item in brands:
    url = item['href']
    company = item.find("span",{"class":"company"}).get_text().replace('&','＆').replace('/','＆').replace('.','_')

    if (url.startswith('http://www')):
      combination = []
      sub_page_request = requests.get(url)
      sub_page_soup = BeautifulSoup(sub_page_request.text,"html.parser")
      sub_page = sub_page_soup.find_all("a",{"class":"thum"})
      
      for sub_page_url in sub_page:
        sub_page_url = sub_page_url["href"] + '/'
        request_url = get_total_count_URL(sub_page_url)

        sub_alba_request = requests.get(request_url)
        sub_alba_soup = BeautifulSoup(sub_alba_request.text,"html.parser")
        
        if sub_alba_soup.find("tbody") == None:
          pass
        else:  
          alba_list = sub_alba_soup.find("tbody").find_all("tr",{"class":""})
          result = get_job(alba_list)
          for item in result:
            combination.append(item)
      export_csv(combination,company)      
    else :
      request_url = get_total_count_URL(url)
      alba_request = requests.get(request_url)
      alba_soup = BeautifulSoup(alba_request.text,"html.parser")

      if alba_soup.find("tbody") == None:
        export_csv([],company)
        
      else:
        alba_list = alba_soup.find("tbody").find_all("tr",{"class":["","divide"]})
        job_list = get_job(alba_list)
        
        export_csv(job_list,company)
main()