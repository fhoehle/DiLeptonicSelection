import ROOT
ROOT.gROOT.SetBatch()
from DataFormats.FWLite import Events, Handle
import commands,getopt,sys,os
sys.path.append(os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions')
import MyHistFunctions_cfi as MyHistFunctions
#commandLine parsing
opts, args = getopt.getopt(sys.argv[1:], '',['input='])
input=None
for opt,arg in opts:
 #print opt , " :   " , arg
 if opt in  ("--input"):
  input=arg
if input == None or input == "":
 sys.exit('no input given')
print "called with ",sys.argv
#
events = Events (input)
#triggers
printPaths = True 
myTrigResultslabel=("TriggerResults");myTrigResultshandle=Handle("edm::TriggerResults");trigResultsHLThandle=Handle("edm::TriggerResults")
# collections
myMuonHandle=Handle("vector<pat::Muon>");myMuonLabel=("selectedPatMuonsPF")
# hists
histMan = MyHistFunctions.MyHistManager("controlPlots")
muonPt = ROOT.TH1F("muonPt","",100,0,400)
numMuons = ROOT.TH1F("muonNum","",5,-0.5,4.5)
######### looping events 
for i,event in enumerate(events):
 event.getByLabel(myTrigResultslabel,myTrigResultshandle); myTrigResults=myTrigResultshandle.product()
 event.getByLabel((myTrigResultslabel,"","PAT"),trigResultsHLThandle); trigResultsHLT = trigResultsHLThandle.product()
 TriggerNames=event.object().triggerNames(myTrigResults)
 TriggerNamesHLT=event.object().triggerNames(trigResultsHLT)
 # print Triggers
 if i == 0 and printPaths:
  TriggerNames=event.object().triggerNames(myTrigResults)
  for j in range(len(TriggerNames)):
   print "path: ",TriggerNames.triggerName(j)
  TriggerNames=event.object().triggerNames(trigResultsHLT)
  for j in range(len(TriggerNames)):
   print "path: ",TriggerNames.triggerName(j)
 #do analysis
 event.getByLabel(myMuonLabel,myMuonHandle); selectedMuons=myMuonHandle.product()
 #event.getByLabel(myDiLepCandLabel,myDiLepCandHandle); diLepCands = myDiLepCandHandle.product()
 if myTrigResults[TriggerNames.triggerIndex("myDiMuonPath")].accept() and trigResultsHLT[TriggerNamesHLT.triggerIndex("HLT_DoubleMu7_v8")].accept():
  numMuons.Fill(len(selectedMuons))
  for muon in selectedMuons:
   muonPt.Fill(muon.pt())
 #for diLepCand in diLepCands:
 # diLepCandMass.Fill(diLepCand.mass())
histMan.saveHist(numMuons)
histMan.saveHist(muonPt)
histMan.done()

