import ROOT,sys,os
sys.path.append(os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions')
sys.path.append(os.getenv('CMSSW_BASE')+"/MyCMSSWAnalysisTools/Tools")
import tools
import MyHistFunctions_cfi as MyHistFunctions
import json
def subSlash(st):
  import re
  return re.sub('/','_',st)
def readJson(dS , jsonFileName):
  
  loadedJson = None
  with open(jsonFileName,'r') as jsonFile:
    loadedJson = json.load(jsonFile)
  for i,(key,data) in enumerate(loadedJson.iteritems()):
    dS[key] = {"processedEvents":int(data["totalEvents"])}
    possOutputFiles = loadedJson[key]["outputFiles"]
    for outF in possOutputFiles:
      if 'patRefSel_diLep_cfg_debughistos' in outF:
        dS[key]["file"] = os.path.dirname(jsonFileName)+os.path.sep+outF
    dS[key]["color"]=data["sample"]["color"]
    dS[key]["xSec"]=float(data["sample"]["xSec"])
    dS[key]["label"]=data["sample"]["label"]
plotFolder = "plots" 
plotFolder += "_"+tools.getTimeStamp()
plotFolder = plotFolder if plotFolder.startswith('/') else os.getenv('PWD')+os.path.sep+plotFolder
os.makedirs(plotFolder)
print plotFolder
datasets = {}
# signal
ttbarsignal = "/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepSignal__2013-08-14_20-37-55/bookKeeping_2013-08-14_20-37-55.json"
readJson(datasets , ttbarsignal)
#datasets["signal"] = {'label':"TTbarDiLep","xSec":157.,"processedEvents":14792.,"color":ROOT.kGreen,"file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLep_2013-08-10_19-48-59/patRefSel_diLep_cfg_debughistos_TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM.root" }
# ttbar bck
ttbarbck = "/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-14_20-37-03/bookKeeping_2013-08-14_20-37-03.json"
readJson(datasets , ttbarbck)
#datasets["ttbarBck"] = {'label':"TTbarNonDiLep","xSec":157.,"processedEvents":100000.,"color":ROOT.kRed , "file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-10_19-48-47/patRefSel_diLep_cfg_debughistos_TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM.root"}
# Tbar scaledown_tW-channel-DS
import json
nonTTbarBcks = None
nonTTbarBckFile = "/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/NonTTbarBck_Parallel_2013-08-16_11-00-11/bookKeeping_2013-08-16_11-00-11.json"
readJson(datasets , nonTTbarBckFile)
#####
plots = ["patMuonsPFNM1isTrackerMuonN1Histo/isTrackerMuon",
"patMuonsPFNM1isGlobalMuonN1Histo/isGlobalMuon",
"patMuonsPFNM1globalTrackNormalizedChi2N1Histo/globalTrackNormalizedChi2",
"patMuonsPFNM1innerTrackValHitsN1Histo/innerTrackValHits",
"patMuonsPFNM1globalTrackHitPatValHitsN1Histo/globalTrackHitPatValHits",
"patMuonsPFNM1absEtaN1Histo/absEta",
"patMuonsPFNM1ptN1Histo/pt",
"patMuonsPFNM1dBN1Histo/dB",
"patMuonsPFNM1relIsoN1Histo/relIso"]
Lint = 100.
histMans = []
stacksHists = []
tobePlotted = ['TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM_Background','TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM_Signal','WJetsToLNu_TuneZ2_7TeV-madgraph-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM','T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM','Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM']
datasetsToPlot = dict( [ (l,d) for l,d in datasets.iteritems() if l in tobePlotted ])
ROOT.TH1.AddDirectory(False)
print datasetsToPlot.keys()
for i,plot in enumerate(plots):
  histMan = MyHistFunctions.MyHistManager("hists_"+plot)
  tmpCan = ROOT.TCanvas("c_"+plot,plot,200,10,700,400);tmpCan.cd()
  for key,dataset in datasetsToPlot.iteritems():
    tmpHist = (ROOT.TFile(dataset["file"]).Get(plot)).Clone("hist_"+key+"_"+plot)  
    tmpHist.Sumw2(); MyHistFunctions.addOverFlowToLastBin(tmpHist);tmpHist.SetLineColor(dataset["color"])
    if i == 0:
      print "test scaling ",key," ",dataset["processedEvents"]," " , dataset["xSec"]
    LumSamp = (dataset["processedEvents"]/dataset["xSec"])
    if i == 0:
      print LumSamp
    tmpHist.Scale(Lint/LumSamp)
    histMan.saveHist(tmpHist)
  stackHists = MyHistFunctions.stackHists(histMan.hists)
  histMans.append(histMan)
  stacksHists.append(stackHists)
  stackHists.createStack();stackHists.plotStack(False,"HIST")
  tmpCan.SaveAs(((plotFolder + os.path.sep ) if plotFolder != "" else "") + subSlash(tmpCan.GetName())+".pdf");tmpCan.SaveAs(((plotFolder + os.path.sep ) if plotFolder != "" else "") + subSlash(tmpCan.GetName())+".root")
