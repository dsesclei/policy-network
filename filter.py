import re
import os

#regex = re.compile('.*RE\[(W|B)\+\d.*')
completed_regex = re.compile('RE\[(W|B)\+\d')
handicap_regex = re.compile('HA\[[1-9]\]')

filtered = 1
total = 1

renames = []
for filename in os.listdir('data/sgf'):
  sgf = open('data/sgf/%s' % filename).read()
  if not completed_regex.search(sgf) or handicap_regex.search(sgf):
    filtered += 1
    os.rename('data/sgf/%s' % filename, 'data/filtered/%s' % filename)
  total += 1
  if total % 10000 == 0:
    print(filtered, total, filtered / total * 100)
    print()
    filtered = 1
    total = 1

