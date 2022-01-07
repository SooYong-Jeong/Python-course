import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://kr.indeed.com/jobs?q=python&limit=".format(LIMIT)

"""
def extract_indeed_pages()
LIMIT = 50:
  resul = requests.get(URL)

  soup = BeautifulSoup(resul.text, "html.parser")

  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]

  for n in range(max_page):
    print("start={}".format(n*50))
"""
def extract_indeed_pages():
  result = requests.get(URL)

  soup = BeautifulSoup(result.text, "html.parser")

  searchCount = soup.find("div", {"id":"searchCountPages"})

  strcount = str(searchCount).split(' ')[-1]
  cases = strcount.split('건')[0]

  cases = cases.replace(',', '')

  max_page = int(float(cases)/50) - 1

  return max_page

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get("{}&start={}".format(URL, page*LIMIT))
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a", {"class": "fs-unmask"})

    for result in results:
      jobTitle = result.find("h2", {"class":"jobTitle"})
      title = jobTitle.find("span").string
      company = result.find("span", {"class":"companyName"})
      companyName = company.find("span")
      if title == "new":
        title = jobTitle.find_all("span")[1].string
      print(title)
      print(companyName)
  
  return jobs
def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print("Scrapping page {}".format(page))
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
    return jobs
def get_jobs():
  last_pages = get_last_page()
  jobs = get_jobs(last_pages)
  return jobs