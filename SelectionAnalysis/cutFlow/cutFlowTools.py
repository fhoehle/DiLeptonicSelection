#########
channels=['diMuon_','diElectronMuon_','diElectron_']
def getSortedKeys(toBeSorted):
  paths=toBeSorted.keys()
  print channels,paths
  return [sorted( filter(lambda s : s.startswith(ch),paths), key=lambda n : -1*toBeSorted[n]['events']) for ch in channels ]
#######
