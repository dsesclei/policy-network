import re
import os

#regex = re.compile('.*RE\[(W|B)\+\d.*')
completed_regex = re.compile('RE\[(W|B)\+\d')
handicap_regex = re.compile('HA\[[1-9]\]')

filtered = 1
total = 1

renames = []
for filename in os.listdir('data/sgf'):
  try:
    sgf = open('data/sgf/%s' % filename).read()
  except:
    print(filename)
    print( 1 / 0)
  if handicap_regex.search(sgf):
    filtered += 1
    os.rename('data/sgf/%s' % filename, 'data/filtered/%s' % filename)
  total += 1
  if total % 10000 == 0:
    print(filtered, total, filtered / total)


