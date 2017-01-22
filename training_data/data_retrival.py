import os, requests, urllib, gzip, time, datetime, shutil, pprint, gzip
import json as JSON
from util import util
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("low", help="display a square of a given number", type=int)
args = parser.parse_args()

def download_zip_files():
  for i in range(len(names)):
    genomic_name = names[i] + '.fna.gz'
    try:
      if genomic_name not in os.listdir('prokaryotes/'):
        print str(i) + ': START ' + names[i] + ' ' + str(datetime.datetime.now())
        urllib.urlretrieve(genomic_urls[i], 'prokaryotes/' + genomic_name)
        print str(i) + ': DOWNLOADED ' + genomic_name
      else:
        print str(i) + ': ALREADY EXISTS ' + genomic_name
    except:
      print str(i) + ': UNABLE TO DOWNLOAD ' + genomic_name + " - " + genomic_urls[i]

    cds_name = 'cds_' + names[i] + '.fna.gz'
    try:
      if cds_name not in os.listdir('prokaryotes/'):
        print str(i) + ': START cds ' + cds_name + ' ' + str(datetime.datetime.now())
        urllib.urlretrieve(cds_urls[i], 'prokaryotes/' + cds_name)
        print str(i) + ': DOWNLOADED ' + cds_name
      else:
        print str(i) + ': ALREADY EXISTS ' + cds_name
    except:
      print str(i) + ': UNABLE TO DOWNLOAD ' + cds_name + " - " + cds_urls[i]

  print "ALL DONWLOADS COMPLETED"  

def parse_genomic_url(string):
  left = string.find('ftp://ftp')
  right = string.find('">', left)
  original_url = string[left:right]
  file_name = original_url[original_url.find('/all/') + 5:]
  return original_url + '/' + file_name + '_genomic.fna.gz'

def parse_cds_url(string):
  left = string.find('ftp://ftp')
  right = string.find('">', left)
  original_url = string[left:right]
  file_name = original_url[original_url.find('/all/') + 5:]
  return original_url + '/' + file_name + '_cds_from_genomic.fna.gz'

def parse_name(string):
  index = string.find('?org=')
  left = string.find('">', index)
  right = string.find('</a>', left)
  return string[left+2:right]

def parse_formal_name(string):
  index = string.find('www_bfind?')
  left = string.find('">', index)
  right = string.find('</a>', left)
  return string[left+2:right]

def parse_Class(string):
  index = string.find('show_organism?category=')
  left = string.find('">', index)
  right = string.find('</a>', left)
  return string[left+2:right]

def parse_phylum(Class):
  if Class.find('proteobacteria') >= 0:
    return 'Proteobacteria'
  elif Class.find('Tenericutes') >= 0:
    return 'Tenericutes'
  elif Class.find('Firmicutes') >= 0:
    return 'Firmicutes'
  else:
    return 'Other'

def create_labels():
  for i in range(len(names)):
    json[names[i]] = {}
    json[names[i]]['url'] = genomic_urls[i]
    json[names[i]]['raw_file_name'] = names[i] + '.fna'
    # json[names[i]]['full_genome_file_dir'] = 'prokaryotes/' + names[i] + '.fna'
    # json[names[i]]['gene_based_genome_file_dir'] = 'prokaryotes/' + 'cds_' + names[i] + '.fna'
    json[names[i]]['organism'] = scientific_names[i]
    json[names[i]]['genus'] = scientific_names[i].split()[0]
    json[names[i]]['domain'] = domain_names[i]
    json[names[i]]['class'] = class_names[i]
    json[names[i]]['name'] = names[i]
    json[names[i]]['phylum'] = parse_phylum(class_names[i])
  with open('y.json', 'w') as outfile:
    JSON.dump(json, outfile)
  print 'Written JSON to file'

def unzip_files():
  for i in range(len(names)):
    if names[i] + '.fna' not in os.listdir('prokaryotes/') and names[i] + '.fna.gz' in os.listdir('prokaryotes/'):
      try:
        inF = gzip.GzipFile('prokaryotes/' + names[i] + '.fna.gz', 'rb') 
        outF = file('prokaryotes/' + names[i] + '.fna', 'wb')
        outF.write(inF.read())
        inF.close()
        outF.close()
        print str(i) + ': ' + names[i] + '.fna'
      except:
        print 'unable to extract ' + names[i] + '.fna'

    if 'cds_' + names[i] + '.fna' not in os.listdir('prokaryotes/') and 'cds_' + names[i] + '.fna.gz' in os.listdir('prokaryotes/'):
      try:
        inF = gzip.GzipFile('prokaryotes/' + 'cds_' + names[i] + '.fna.gz', 'rb') 
        outF = file('prokaryotes/' + 'cds_' + names[i] + '.fna', 'wb')
        outF.write(inF.read())
        inF.close()
        outF.close()
        print str(i) + ': ' + 'cds_' + names[i] + '.fna'
      except:
        print 'unable to extract ' + names[i] + '.fna'

pp = pprint.PrettyPrinter(indent=4)
with open('genome_urls.htm') as html:
  content = html.readlines()

genomic_urls, cds_urls, names, scientific_names, domain_names, class_names = [], [], [], [], [], []
json = {}
Class, domain = None, None

for i in range(len(content)):
  if content[i].find('ftp://ftp') >= 0:
    genomic_urls.append(parse_genomic_url(content[i]))
    cds_urls.append(parse_cds_url(content[i]))
  elif content[i].find('?org=') >= 0:
    names.append(parse_name(content[i]))
    domain_names.append(domain)
    class_names.append(Class)
  elif content[i].find('www_bfind?') >= 0:
    scientific_names.append(parse_formal_name(content[i]))
  elif content[i].find('>Bacteria<') >= 0:
    domain = 'Bacteria'
  elif content[i].find('>Archaea<') >= 0:
    domain = 'Archaea'
  elif content[i].find('show_organism?category=') >=0 and content[i+1].find('show_organism?category=') >= 0:
    Class = parse_Class(content[i])

print len(genomic_urls)
print len(names)
assert len(genomic_urls) == len(names) == len(scientific_names) == len(domain_names) == len(class_names)

download_zip_files()

create_labels()

# pp.pprint(json)

unzip_files()
