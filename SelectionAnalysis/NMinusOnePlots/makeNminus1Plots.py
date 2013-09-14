import ROOT,sys,os,argparse
sys.path.append(os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions')
sys.path.append(os.getenv('CMSSW_BASE')+"/MyCMSSWAnalysisTools/Tools")
import tools
import MyHistFunctions_cfi as MyHistFunctions
import json
parser = argparse.ArgumentParser()
parser.add_argument('--debug',action='store_true',default=False,help="debug mode")
args = parser.parse_args()
def subSlash(st):
  import re
  return re.sub('/','_',st)
def readJson(dS , jsonFileName,debug=False):
  
  loadedJson = None
  with open(jsonFileName,'r') as jsonFile:
    loadedJson = json.load(jsonFile)
  if debug:
    print "json ",jsonFileName," contains ",loadedJson.keys()
  for i,(key,data) in enumerate(loadedJson.iteritems()):
    dS[key] = {"processedEvents":int(data['sample']["totalEvents"])}
    possOutputFiles = None
    if debug:
      print "samp ",key," contain ",data.keys()
    if data.has_key("outputFilesCrab"):
      possOutputFiles = data["outputFilesCrab"]
    else:
      possOutputFiles = loadedJson[key]["outputFiles"]
    for outF in possOutputFiles:
      if 'patRefSel_diLep_cfg_debughistos' in outF:
        dS[key]["file"] = os.path.dirname(jsonFileName)+os.path.sep+outF
    dS[key]["color"]=data["sample"]["color"]
    dS[key]["xSec"]=float(data["sample"]["xSec"])
    dS[key]["label"]=data["sample"]["label"]
########################################
ROOT.gROOT.SetStyle("Plain")
####################
plotFolder = "plots" 
plotFolder += "_"+tools.getTimeStamp()
plotFolder = plotFolder if plotFolder.startswith('/') else os.getenv('PWD')+os.path.sep+plotFolder
os.makedirs(plotFolder)
print plotFolder
datasets = {}
# signal
ttbarsignal = "/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarSignal_Grid_2013-09-03_11-13-04/bookKeeping_2013-09-03_11-13-04__bookKeepingUpdated_2013-09-10_18-27-40.json"
readJson(datasets , ttbarsignal)
#datasets["signal"] = {'label':"TTbarDiLep","xSec":157.,"processedEvents":14792.,"color":ROOT.kGreen,"file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLep_2013-08-10_19-48-59/patRefSel_diLep_cfg_debughistos_TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM.root" }
# ttbar bck
ttbarbck = "/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarBkg_Grid_2013-09-03_13-13-35/bookKeeping_2013-09-03_13-13-35__bookKeepingUpdated_2013-09-10_18-44-18.json"
readJson(datasets , ttbarbck,args.debug)
#datasets["ttbarBck"] = {'label':"TTbarNonDiLep","xSec":157.,"processedEvents":100000.,"color":ROOT.kRed , "file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-10_19-48-47/patRefSel_diLep_cfg_debughistos_TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM.root"}
# Tbar scaledown_tW-channel-DS
import json
nonTTbarBcks = None
# wjets
wJetsToLNuBckFile = "/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/NonTTbarBck_Parallel_2013-08-17_11-21-09/bookKeeping_2013-08-17_11-21-09__bookKeepingUpdated_2013-09-10_18-13-10.json"
readJson(datasets ,wJetsToLNuBckFile,args.debug)
# singleTopTwChDS
singleTopTwChDSFile ='/.automount/net_rw/net__scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/BackGrounds_Nminus1/T_TuneZ2_tW-channel-DS_2013-09-12_11-30-31/bookKeeping_2013-09-12_11-30-31__bookKeepingUpdated_2013-09-14_15-28-22.json'
readJson(datasets ,singleTopTwChDSFile,args.debug)
# singleTopTwChDR
singleTopTwChDRFile='/.automount/net_rw/net__scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/BackGrounds_Nminus1/T_TuneZ2_tW-channel-DR_2013-09-12_12-18-28/bookKeeping_2013-09-12_12-18-28__bookKeepingUpdated_2013-09-14_15-27-17.json'
readJson(datasets ,singleTopTwChDRFile,args.debug)
###
#datasets
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
#tobePlotted = ['TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM_Background','TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM_Signal','WJetsToLNu_TuneZ2_7TeV-madgraph-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM','T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM','Tbar_TuneZ2_tW-channel-DR_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM']
tobePlotted = [u'TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM_Signal', u'TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM_Bck', u'T_TuneZ2_tW-channel-DS_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM', u'WJetsToLNu_TuneZ2_7TeV-madgraph-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM']
#print "available datasets ",datasets.keys()
datasetsToPlot = dict( [ (l,d) for l,d in datasets.iteritems() if l in tobePlotted ])
ROOT.TH1.AddDirectory(False)
#print " plotted datasets ",datasetsToPlot.keys()
debug = True
for i,plot in enumerate(plots):
  histMan = MyHistFunctions.MyHistManager("hists_"+plot)
  tmpCan = ROOT.TCanvas("c_"+plot,plot,200,10,700,400);tmpCan.cd()
  for key,dataset in datasetsToPlot.iteritems():
    tmpHist = (ROOT.TFile(dataset["file"]).Get(plot)).Clone("hist_"+key+"_"+plot) 
    setattr(tmpHist,'label',dataset["label"] )
    setattr(tmpHist,'copyIt',['label'])
    tmpHist.Sumw2(); MyHistFunctions.addOverFlowToLastBin(tmpHist);tmpHist.SetLineColor(dataset["color"])
    if debug:
      print "test scaling ",key," ",dataset["processedEvents"]," " , dataset["xSec"] , " i ",i
    LumSamp = (dataset["processedEvents"]/dataset["xSec"])
    if debug:
      print "sample factor ",Lint/LumSamp
    tmpHist.Scale(Lint/LumSamp)
    if debug:
      print (plot," ",dataset["label"]," ", tmpHist.Integral())
    histMan.saveHist(tmpHist)
  stackHists = MyHistFunctions.stackHists(histMan.hists,debug=True)
  histMans.append(histMan)
  stacksHists.append(stackHists)
  stackHists.createStack();stackHists.plotStack(False,"HIST");stackHists.drawLegend()
  tmpCan.SaveAs(((plotFolder + os.path.sep ) if plotFolder != "" else "") + subSlash(tmpCan.GetName())+".pdf");tmpCan.SaveAs(((plotFolder + os.path.sep ) if plotFolder != "" else "") + subSlash(tmpCan.GetName())+".root")
