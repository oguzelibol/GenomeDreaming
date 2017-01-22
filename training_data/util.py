import os

class util:
  def __init__(self, working_dir):
    self.initialized = True
    self.WORKING_DIR = working_dir

  def get_single_org_genome(self, file_name):
    with open(self.WORKING_DIR + file_name) as file:
      content = file.readlines()[1:]
      raw = ''.join(content)
      string = ''
      for char in raw:
        if char != '\n' and char != '>':
          string += char
        elif char == '>':
          return string
      return string

  def get_clean_single_org_genome(self, file_name):
    with open(self.WORKING_DIR + file_name) as file:
      content = file.readlines()[0]
      return ''.join(content)

  def get_single_gene_based_genome(self, file_name):
    list_of_json = []
    with open(self.WORKING_DIR + file_name) as file:
      for line in file.readlines():
        if line.find('>lcl') >=0:
          list_of_json.append(self.parse_gene_info(line))
        else:
          for char in line:
            if char != '\n' and char != '>':
              list_of_json[-1]['sequence'] += char
            elif char == '>':
              break
    return list_of_json


  def parse_gene_info(self, line):
    json = {}
    json['sequence'] = ''
    array = line.split(' [')
    for i in range(len(array)):
      while array[i][-1] in [']', '\n']:
        array[i] = array[i][:-1]
    for item in array:
      if item.find('=') >= 0:
        mid = item.find('=')
        json[item[:mid]] = item[mid+1:]
    if 'location' in json:
      if json['location'].find('complement') >= 0:
        json['complement'] = 1
        json['location_start'] = json['location'][json['location'].find('(') + 1: json['location'].find('..')]
        json['location_stop'] = json['location'][json['location'].find('..') + 2: json['location'].find(')')]
      else:
        json['complement'] = 0
        json['location_start'] = json['location'].split('..')[0]
        json['location_stop'] = json['location'].split('..')[1]
    if 'protein' in json:
      json['protein_name'] = json['protein']
      del json['protein']
    return json
