from DataFormats.FWLite import Events, Handle
import commands,getopt,sys,os,argparse,re
sys.path.extend([os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions',os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools'])

#commandLine parsing
parser = argparse.ArgumentParser()
parser.add_argument('--input',required=True,help='input edm file, which TriggerReport should be evaluated')
parser.add_argument('--showAvailablePaths',action='store_true',default=False,help='list available paths')
parser.add_argument('--listTriggerResultCollections',action='store_true',default=False,help='show trigegrReport collections of input file')
parser.add_argument('--processName',default='HLT',help='optional process name')
parser.add_argument('--useMCSignal',default=False,action='store_true',help="calculate eff for signal mc events")
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
######
interestingPaths = {
  'isDiLepPath':{'pathName':'isDiLepPath','label':'diLepMC'}
  ,'isDiMuonMcTagPath':{'pathName':'isDiMuonMcTagPath','label':'diLep_diMuonMC'}
  ,'isDiElectronMcTagPath':{'pathName':'isDiElectronMcTagPath','label':'diLep_diElectronMC'}
  ,'isMuonElectronMcTagPath':{'pathName':'isMuonElectronMcTagPath','label':'diLep_ElectronMuonMC'}
  ,'cutFlowPath1myDiMuonPathgoodOfflinePrimaryVertices':{'pathName':'cutFlowPath1myDiMuonPathgoodOfflinePrimaryVertices','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_goodVertex'}
  }
#################
events = Events (args.input)
def getPathNames(evts,trigH,trigL):
  trigNL=[]
  for e in evts:
    e.getByLabel((trigL,"",args.processName),trigH); trigR=trigH.product()
    trigNs=e.object().triggerNames(trigR)
    for j in range(len(trigNs)):
      trigNL.append(trigNs.triggerName(j))
    break
  return trigNL
#triggers
triggerEfficiencies = {}
TrigResultslabel=("TriggerResults");TrigResultshandle=Handle("edm::TriggerResults")
triggerNamesList = getPathNames(events,TrigResultshandle,TrigResultslabel)
####

####
for n in triggerNamesList:
  if args.showAvailablePaths:
    print "path: ",n
  triggerEfficiencies[n] = 0
if args.showAvailablePaths:
  sys.exit(0)
###################
for i,event in enumerate(events):
  event.getByLabel((TrigResultslabel,"",args.processName),TrigResultshandle); TrigResults=TrigResultshandle.product()
  TriggerNames=event.object().triggerNames(TrigResults)
  # print Triggers
  for j in range(len(TriggerNames)):
    triggerName = TriggerNames.triggerName(j)
    mcTriggerName = "" if not interestingPaths.has_key(triggerName) or not args.useMCSignal else ( "" if not interestingPaths[triggerName].has_key('preFilterPath') else interestingPaths[triggerName]['preFilterPath'] )
    mcSignal =  mcTriggerName == "" 
    if not mcTriggerName == "": 
      mcSignal = TrigResults[TriggerNames.triggerIndex(mcTriggerName)].accept()
    if TrigResults[TriggerNames.triggerIndex(triggerName)].accept() and mcSignal:
      triggerEfficiencies[triggerName] += 1 
###############
totalEvts=i+1
import Tools.cfgFileTools as cfgFileTools
print "===================================================="
print "trigger efficiencies calculated using ",totalEvts," events"
sortedTriggers = sorted(triggerEfficiencies.keys(),key=cfgFileTools.natural_sort_key)

for trigN in interestingPaths.keys():
  print interestingPaths[trigN]['label']," "," events: ",triggerEfficiencies[interestingPaths[trigN]['pathName']]," eff. ",float(triggerEfficiencies[interestingPaths[trigN]['pathName']])/(totalEvts if not interestingPaths[trigN].has_key('preFilterPath') or not args.useMCSignal else  triggerEfficiencies[interestingPaths[trigN]['preFilterPath']]), " ",trigN, ("" if not interestingPaths[trigN].has_key('preFilterPath') or not args.useMCSignal else " prePathFilter "+interestingPaths[trigN]['preFilterPath'])

def printLatexTableLine(cut, eff, evts):
  return cut+" & "+eff+" & "+evts+" \\"
