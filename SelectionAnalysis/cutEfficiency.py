from DataFormats.FWLite import Events, Handle
import commands,getopt,sys,os,argparse,re,signal
stopIteration = False
def signal_handler(signal, frame):
   print('You pressed Ctrl+C!')
   global stopIteration 
   stopIteration = True
   pass
signal.signal(signal.SIGINT, signal_handler)

sys.path.extend([os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions',os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools'])

#commandLine parsing
parser = argparse.ArgumentParser()
parser.add_argument('--input',required=True,help='input edm file, which TriggerReport should be evaluated',nargs = '*')
parser.add_argument('--showAvailablePaths',action='store_true',default=False,help='list available paths')
parser.add_argument('--listTriggerResultCollections',action='store_true',default=False,help='show trigegrReport collections of input file')
parser.add_argument('--processName',default='HLT',help='optional process name')
parser.add_argument('--useMCSignal',default=False,action='store_true',help="calculate eff for signal mc events")
parser.add_argument('--showAllPathCutFlow',default='',help="show all paths for regex i.e. myDiMuonPath")
parser.add_argument('--usage',action='store_true',default=False,help='help message')
parser.add_argument('--usingBkg',action='store_true',default=False,help='use this switch to run on background')
args=parser.parse_args()
if args.usage:
  parser.print_help()
  sys.exit(0)
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
import Tools.coreTools as coreTools
coreTools.OrderedDict
interestedPaths = coreTools.OrderedDict([
  ('isDiLepPath',{'pathName':'isDiLepPath','label':'diLepMC','isMCpath':True})
  ,('isDiMuonMcTagPath',{'pathName':'isDiMuonMcTagPath','label':'diLep_diMuonMC','isMCpath':True})
  ,('isDiElectronMcTagPath',{'pathName':'isDiElectronMcTagPath','label':'diLep_diElectronMC','isMCpath':True})
  ,('isMuonElectronMcTagPath',{'pathName':'isMuonElectronMcTagPath','label':'diLep_ElectronMuonMC','isMCpath':True})
  #(##########################################
  ,('cutFlowPath1myDiMuonPathgoodOfflinePrimaryVertices',{'pathName':'cutFlowPath1myDiMuonPathgoodOfflinePrimaryVertices','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_goodVertex'})
  ,('cutFlowPath35myDiMuonPathmyDiMuonTriggerCheck',{'pathName':'cutFlowPath35myDiMuonPathmyDiMuonTriggerCheck','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_trigger'})
  ,('cutFlowPath37myDiMuonPathmySelectedPatMuonsMaxCount',{'pathName':'cutFlowPath37myDiMuonPathmySelectedPatMuonsMaxCount','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_oneMinAndMaxMuons'})
  ,('cutFlowPath39myDiMuonPathDiLepCandMuonsCount',{'pathName':'cutFlowPath39myDiMuonPathDiLepCandMuonsCount','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_DiLepCandMuons'})
  ,('cutFlowPath41myDiMuonPathDiLepCandMuonsZVetoCount',{'pathName':'cutFlowPath41myDiMuonPathDiLepCandMuonsZVetoCount','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_ZVeto'})
  ,('cutFlowPath42myDiMuonPathcleanJetsDiMuonCount',{'pathName':'cutFlowPath42myDiMuonPathcleanJetsDiMuonCount','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_jetCount'})
  ,('cutFlowPath44myDiMuonPathDiMuonmyselectedPatMETsCount',{'pathName':'cutFlowPath44myDiMuonPathDiMuonmyselectedPatMETsCount','preFilterPath':'isDiMuonMcTagPath','label':'diMuon_MET'})
  #(####################################
  ,('cutFlowPath1myDiElectronMuonPathgoodOfflinePrimaryVertices',{'pathName':'cutFlowPath1myDiElectronMuonPathgoodOfflinePrimaryVertices','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_goodVertex'})
  ,('cutFlowPath35myDiElectronMuonPathmyMuonElectronTriggerCheck',{'pathName':'cutFlowPath35myDiElectronMuonPathmyMuonElectronTriggerCheck','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_trigger'})
  ,('cutFlowPath36myDiElectronMuonPathmySelectedPatElectronsMuonsMinCount',{'pathName':'cutFlowPath36myDiElectronMuonPathmySelectedPatElectronsMuonsMinCount','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_eleMuonMin'})
  ,('cutFlowPath37myDiElectronMuonPathmySelectedPatMuonsElectronsMinCount',{'pathName':'cutFlowPath37myDiElectronMuonPathmySelectedPatMuonsElectronsMinCount','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_muonEleMin'})
  ,('cutFlowPath38myDiElectronMuonPathDiLepCandEMuCount',{'pathName':'cutFlowPath38myDiElectronMuonPathDiLepCandEMuCount','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_DiLepCand'})
  ,('cutFlowPath39myDiElectronMuonPathMuonsUsedForDiLepCandEMuCount',{'pathName':'cutFlowPath39myDiElectronMuonPathMuonsUsedForDiLepCandEMuCount','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_muonUsedForDiLepCandEMu'})
  ,('cutFlowPath40myDiElectronMuonPathElectronsUsedForDiLepCandEMuCount',{'pathName':'cutFlowPath40myDiElectronMuonPathElectronsUsedForDiLepCandEMuCount','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_eleUsedForDiLepCandEMu'})
  ,('cutFlowPath41myDiElectronMuonPathcleanJetsDiEMuCount',{'pathName':'cutFlowPath41myDiElectronMuonPathcleanJetsDiEMuCount','preFilterPath':'isMuonElectronMcTagPath','label':'diElectronMuon_jetCount'})
  ##############################################
  ,('cutFlowPath1myDiElectronPathgoodOfflinePrimaryVertices',{'pathName':'cutFlowPath1myDiElectronPathgoodOfflinePrimaryVertices','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_goodVertex'})
  ,('cutFlowPath35myDiElectronPathmyDiElectronTriggerCheck',{'pathName':'cutFlowPath35myDiElectronPathmyDiElectronTriggerCheck','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_trigger'})
  ,('cutFlowPath37myDiElectronPathmySelectedPatElectronsMaxCount',{'pathName':'cutFlowPath37myDiElectronPathmySelectedPatElectronsMaxCount','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_oneMinAndMaxElectron'})
  ,('cutFlowPath38myDiElectronPathDiLepCandElectronsCount',{'pathName':'cutFlowPath38myDiElectronPathDiLepCandElectronsCount','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_DiLepCandElectrons'})
  ,('cutFlowPath40myDiElectronPathDiLepCandElectronsZVetoCount',{'pathName':'cutFlowPath40myDiElectronPathDiLepCandElectronsZVetoCount','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_ZVeto'})
  ,('cutFlowPath41myDiElectronPathcleanJetsDiElectronCount',{'pathName':'cutFlowPath41myDiElectronPathcleanJetsDiElectronCount','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_jetCount'})
  ,('cutFlowPath43myDiElectronPathDiElectronmyselectedPatMETsCount',{'pathName':'cutFlowPath43myDiElectronPathDiElectronmyselectedPatMETsCount','preFilterPath':'isDiElectronMcTagPath','label':'diElectron_MET'})
  ])
####################
if args.usingBkg:
  for k in interestedPaths.keys():
    if interestedPaths[k].has_key('isMCpath'):
      print "neglecting ",k
      del interestedPaths[k]
  print "done mc cleaning"
###############
def fixKeysMinus1(d):
  import re
  keyRe = re.compile('(cutFlowPath)([0-9][0-9]*)(.*)')
  for k in d.keys():
    kg= keyRe.match(k)
    if kg:
      d[k]['pathName'] = kg.group(1)+str(int(kg.group(2))-1)+kg.group(3)
      d[kg.group(1)+str(int(kg.group(2))-1)+kg.group(3)]=d.pop(k)
  return d
#########################
interestingPaths=None
if args.usingBkg:
  interestingPaths = fixKeysMinus1(interestedPaths)
else:
  interestingPaths=interestedPaths
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
if args.showAllPathCutFlow:
  for n in triggerNamesList:
    if interestingPaths.has_key(n):
      continue
    interestingPaths[n]= {'pathName':n,'label':'TEST'}
####
for n in triggerNamesList:
  if args.showAvailablePaths:
    print "path: ",n
  triggerEfficiencies[n]=0
if args.showAvailablePaths:
  sys.exit(0)
######################
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
  if i % 1000 == 0:
    print "processed ",i," events"
  if stopIteration:
    break
###############
###############
totalEvts=i+1
import Tools.cfgFileTools as cfgFileTools
print "===================================================="
print "trigger efficiencies calculated using ",totalEvts," events"
sortedTriggers = interestingPaths.keys() if not args.showAllPathCutFlow else sorted([k for k in interestingPaths.keys() if args.showAllPathCutFlow in k],key=cfgFileTools.natural_sort_key)
if args.showAllPathCutFlow:
  print " only using paths containing ",args.showAllPathCutFlow
for trigN in sortedTriggers:#interestingPaths.keys():
  print "trigN ",trigN
  print interestingPaths[trigN]['label']," ",
  print " events: ",triggerEfficiencies[interestingPaths[trigN]['pathName']],
  print " eff. ",float(triggerEfficiencies[interestingPaths[trigN]['pathName']])/(totalEvts if (not interestingPaths[trigN].has_key('preFilterPath') or not args.useMCSignal) else  triggerEfficiencies[interestingPaths[trigN]['preFilterPath']]), " ",
  print trigN, ("" if not interestingPaths[trigN].has_key('preFilterPath') or not args.useMCSignal else " prePathFilter "+interestingPaths[trigN]['preFilterPath'])

def printLatexTableLine(cut, eff, evts):
  return cut+" & "+eff+" & "+evts+" \\"
