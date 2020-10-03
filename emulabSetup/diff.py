import glob
import os
import sys
import xml.etree.ElementTree as ET

runsFolder = ""

def getStat(xmlFile, logFolder):
  def normalizedName(name):
      head, tail = os.path.split(name)
      return os.path.join(os.path.split(head)[1], tail)
  ''' output is a map from benchmark name to stat '''
  data = dict()
  tree = ET.parse(xmlFile)
  root = tree.getroot()
  for child in root:
    if child.tag == 'run':
      runData = dict()
      name = normalizedName(child.attrib['name'])
      for col in child:
        runData[col.attrib['title']] = col.attrib['value']
      runData['logFolder'] = logFolder
      data[name] = runData
  return data

def mergeDDSubsets(stats):
  #DD = "Systems_DeviceDriversLinux64_ReachSafety"
  #if DD in stats.keys():
  #  return stats
  #else:
  #  ret = dict(stats)
  #  ret[DD] = dict()
  #for setName in stats.keys():
  #  if DD in setName:
  #    ret[DD].update(stats[setName])
  #    del ret[setName]
  #return ret
  return stats

def run(set1, set2):
  stats1 = dict()
  stats2 = dict()
  for xmlPath in glob.glob('/proj/SMACK/SMACKBenchResults/data/runs/*/*/*.xml'):
    # skip witness checked files and ECA and Termination*
    if 'witchecked' in xmlPath or 'ECA' in xmlPath or 'Termination' in xmlPath:
      continue
    else:
      xmlFile = os.path.basename(xmlPath)
      logFolder = os.path.join(os.path.dirname(xmlPath), '.'.join(xmlFile.split('.')[0:2]+['logfiles']))
      setName, _ = xmlFile.split('.')[-2:]
      if set1 in xmlFile:
        stats1[setName] = getStat(xmlPath, logFolder)
      #elif set2 in xmlFile and not 'baseline' in xmlFile and not 'no-bv' in xmlFile and not 'release' in xmlFile and not 'unroll' in xmlFile and not 'fix-z3-options' in xmlFile:
      elif set2 in xmlFile:
        stats2[setName] = getStat(xmlPath, logFolder)
  #compare(stats1, stats2)
  compare(mergeDDSubsets(stats1), mergeDDSubsets(stats2))

def isErrorStatus(status):
  return (status == 'TIMEOUT') \
          or (status == 'OUT OF MEMORY') \
            or ('ERROR' in status)

def compare(stats1, stats2):
  def statusEqual(s1, s2):
    if 'false' in s1 and 'false' in s2:
      return True
    else:
      return s1 == s2
  #assert len(stats1.keys()) == len(stats2.keys()), "#set differs\n"
  for setName in stats1.keys():
    setStat1 = stats1[setName]
    setStat2 = stats2[setName]
    setStatCP1 = dict(setStat1)
    setStatCP2 = dict(setStat2)
    score1 = 0
    score2 = 0
    print '=================={}================'.format(setName)
    for bm in setStat1.keys():
      if bm in setStat2.keys():
        del setStatCP1[bm]
        del setStatCP2[bm]
        status1 = setStat1[bm]['status']
        status2 = setStat2[bm]['status']
        if status1 == '' or status2 == '':
          #raise RuntimeError("Losing info")
          continue
        if not statusEqual(status1, status2):
          if status1 == 'ERROR (1)' and status2 == 'OUT OF MEMORY':
            with open(glob.glob(setStat1[bm]['logFolder']+'/*'+os.path.basename(bm)+'.log')[0], 'r') as f:
              c = f.read()
              if 'Stopping: Out of memory' in c or 'OutOfMemoryException' in c:
                continue
          try:
            wrong = setStat1[bm]['category'] == 'wrong' or setStat2[bm]['category'] == 'wrong'
          except KeyError:
            print bm
            continue
          formatStr = '{0}: {1}, {2}'
          formatStr = '\033[93m'+formatStr+'\033[0m' if wrong else formatStr
          def myPrint(s):
            print(s)
          printFunc = lambda info1 : lambda info2 : myPrint(formatStr.format(bm, info1, info2))

          #if status1 == 'TIMEOUT' or status2 == 'TIMEOUT':
          if isErrorStatus(status1) or isErrorStatus(status2):
            scored = lambda stat: ('true' in stat or 'false' in stat) and (not isErrorStatus(stat))
            score1 += (1 if scored(status1) else 0)
            score2 += (1 if scored(status2) else 0)
            formatCputime = lambda cputime: '(' + cputime.split('.')[0]+')'
            printFunc(status1+formatCputime(setStat1[bm]['cputime']))(status2+formatCputime(setStat2[bm]['cputime']))
          else:
            printFunc(status1)(status2)
    print '{0} {1}'.format(score1, score2)
    #print len(setStat1.keys())
    if len(setStatCP1) != 0 or len(setStatCP2) != 0:
      print '# differs'

if __name__ == '__main__':
  set1 = sys.argv[1]
  set2 = sys.argv[2]
  run(set1, set2)
