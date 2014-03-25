from DataFormats.FWLite import Events, Handle
import commands,getopt,sys,os,argparse
sys.path.extend([os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions',os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools'])

#commandLine parsing
parser = argparse.ArgumentParser()
parser.add_argument('--input',required=True,help='input edm file, which TriggerReport should be evaluated')
parser.add_argument('--showAvailablePaths',action='store_true',default=False,help='list available paths')
parser.add_argument('--listTriggerResultCollections',action='store_true',default=False,help='show trigegrReport collections of input file')
parser.add_argument('--processName',default='HLT',help='optional process name')
args=parser.parse_args()
print "called with ",sys.argv
#
#edmTriggerResults_TriggerResults__

if args.listTriggerResultCollections:
  import re,ROOT
  triggerResults=re.compile('^edmTriggerResults_TriggerResults_([^_]*)_([^_]*)$')
  rootFile = ROOT.TFile(args.input)
  evtTree= rootFile.Get('Events')
  listOfBranches = evtTree.GetListOfBranches()
  for b in listOfBranches:
    m = triggerResults.match(b.GetName())
    if m : 
      print "TriggerResults found in paths ",m.group(2),(" have sublabel "+m.group(1) if m.group(1) != "" else "")
  sys.exit(0)

events = Events (args.input)
#triggers
TrigResultslabel=("TriggerResults");TrigResultshandle=Handle("edm::TriggerResults")
###################
triggerEfficiencies = {}
for i,event in enumerate(events):
  event.getByLabel((TrigResultslabel,"",args.processName),TrigResultshandle); TrigResults=TrigResultshandle.product()
  TriggerNames=event.object().triggerNames(TrigResults)
  # print Triggers
  if args.showAvailablePaths or i == 0:
    if args.showAvailablePaths: print "trigger in ",args.processName
    for j in range(len(TriggerNames)):
      triggerName = TriggerNames.triggerName(j)
      if args.showAvailablePaths:  print "path: ",triggerName
      triggerEfficiencies[triggerName] = 0
    ###########
    if args.showAvailablePaths: sys.exit(0) 
  
  for j in range(len(TriggerNames)):
    triggerName = TriggerNames.triggerName(j)
    if TrigResults[TriggerNames.triggerIndex(triggerName)].accept():
      triggerEfficiencies[triggerName] += 1 
###############
totalEvts=i+1
import Tools.cfgFileTools as cfgFileTools
print "===================================================="
print "trigger efficiencies calculated using ",totalEvts," events"
interestingPaths = {
  'diLepMC':{'pathName':'isDiLepPath'}
  ,'diLep_diMuonMC':{'pathName':'isDiMuonMcTagPath'}
  ,'diLep_diElectronMC':{'pathName':'isDiElectronMcTagPath'}
  ,'diLep_ElectronMuonMC':{'pathName':'isMuonElectronMcTagPath'}
  }
for trigN in sorted(triggerEfficiencies.keys(),key=cfgFileTools.natural_sort_key) :
  print trigN," "," events: ",triggerEfficiencies[trigN]," eff. ",float(triggerEfficiencies[trigN])/totalEvts

def printLatexTableLine(cut, eff, evts):
  return cut+" & "+eff+" & "+evts+" \\"
