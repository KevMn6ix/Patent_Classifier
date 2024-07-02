from bs4 import BeautifulSoup
import requests
import re

url ='https://www.uspto.gov/web/patents/classification/cpc/html/cpc-G.html'

parser = 'lxml'

def find_section_description(section):
    url = f'https://www.uspto.gov/web/patents/classification/cpc/html/cpc-{section}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, parser)
    desc = soup.find('span', class_ ='ipc-text').text.rstrip().title()
    letters_only = re.findall(r'[a-zA-Z]+', desc)
    desc = ' '.join(letters_only)
    return desc

def find_class_description(section, class_):
    url = f'https://www.uspto.gov/web/patents/classification/cpc/html/cpc-{section}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, parser)
    desc = soup.find('table', id=f'{section}{class_}').find('span', class_='ipc-text').text.rstrip().title()
    letters_only = re.findall(r'[a-zA-Z]+', desc)
    desc = ' '.join(letters_only)
    return desc

def find_subclass_description(section, class_, subclass):
    url = f'https://www.uspto.gov/web/patents/classification/cpc/html/cpc-{section}{class_}{subclass}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, parser)
    desc = soup.find('table', id =f'{section}{class_}{subclass}').find('span', class_='ipc-text').text.rstrip().title()
    letters_only = re.findall(r'[a-zA-Z]+', desc)
    desc = ' '.join(letters_only)
    return desc

def find_group_description(section, class_, subclass, group):
    url = f'https://www.uspto.gov/web/patents/classification/cpc/html/cpc-{section}{class_}{subclass}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, parser)
    desc = soup.find('table', id = f'{section}{class_}{subclass}{group}/00').find('span', class_ = 'ipc-text').text.rstrip().title()
    letters_only = re.findall(r'[a-zA-Z]+', desc)
    desc = ' '.join(letters_only)
    return desc

def find_subgroup_description(section, class_, subclass, group, subgroup):
    url = f'https://www.uspto.gov/web/patents/classification/cpc/html/cpc-{section}{class_}{subclass}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, parser)
    desc = soup.find('table', id = f'{section}{class_}{subclass}{group}/{subgroup}').find('span', class_ = 'cpc-text').text.rstrip().title()
    letters_only = re.findall(r'[a-zA-Z]+', desc)
    desc = ' '.join(letters_only)
    return desc

def find_description(section, class_, subclass, group, subgroup):
    code_description = {}
    code_description['Section'] = find_section_description(section)
    code_description['Class'] = find_class_description(section, class_)
    code_description['Subclass'] = find_subclass_description(section, class_, subclass)
    code_description['Group'] = find_group_description(section, class_, subclass, group)
    code_description['Subgroup'] = find_subgroup_description(section, class_, subclass, group, subgroup)
    return code_description