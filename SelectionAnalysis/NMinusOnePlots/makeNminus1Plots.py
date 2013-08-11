import ROOT,sys,os
sys.path.append(os.getenv('HOME')+'/PyRoot_Helpers/PyRoot_Functions')
import MyHistFunctions_cfi as MyHistFunctions
def subSlash(st):
  import re
  return re.sub('/','_',st)
datasets = {}
# signal
datasets["signal"] = {'label':"TTbarDiLep","xSec":157.,"processedEvents":14792.,"color":ROOT.kGreen,"file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLep_2013-08-10_19-48-59/patRefSel_diLep_cfg_debughistos_TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM.root" }
# ttbar bck
datasets["ttbarBck"] = {'label':"TTbarNonDiLep","xSec":157.,"processedEvents":100000.,"color":ROOT.kRed , "file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-10_19-48-47/patRefSel_diLep_cfg_debughistos_TT_TuneZ2_7TeV-mcatnlo__Fall11-PU_S6_START42_V14B-v1__AODSIM.root"}
# Tbar scaledown_tW-channel-DS
import json
nonTTbarBcks = None
#with open('/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TMP_Bck_2013-08-11_20-25-26/bookKeeping_2013-08-11_20-25-26.json') as nonTTbarBckFile:
with open('/.automount/net_rw/net__scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TMP_Bck_2013-08-11_22-08-56/bookKeeping_2013-08-11_22-08-56.json') as nonTTbarBckFile:
  nonTTbarBcks = json.load(nonTTbarBckFile)

for i,(key,data) in enumerate(nonTTbarBcks.iteritems()):
  datasets[key] = {"processedEvents":int(data["totalEvents"])}
  possOutputFiles = nonTTbarBcks[key]["outputFiles"]
  for outF in possOutputFiles:
    if 'patRefSel_diLep_cfg_debughistos' in outF:
      datasets[key]["file"] = os.path.dirname(nonTTbarBckFile.name)+os.path.sep+outF
  datasets[key]["color"]=ROOT.kBlue-i
  datasets[key]["xSec"]=data["sample"]["xSec"]
  datasets[key]["label"]=data["sample"]["label"]
##
datasets["tbarScaleDowntWChDS"] = {'label':"Tbar_scaledown_tW-channel-DS","xSec":1,"processedEvents":9512.,"color":ROOT.kYellow , "file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-10_15-48-14/patRefSel_diLep_cfg_debughistos_Tbar_TuneZ2_scaledown_tW-channel-DS_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM.root"}
#
datasets["tbartWChDS"] = {'label':"Tbar_TuneZ2_tW-channel-DS","xSec":1,"processedEvents":1,"color":ROOT.kYellow+3 , "file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-10_15-48-14/patRefSel_diLep_cfg_debughistos_Tbar_TuneZ2_tW-channel-DS_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM.root"}
#
datasets["ttWChDR"] = {'label':"T_TuneZ2_tW-channel-DR","xSec":1,"processedEvents":1,"color":ROOT.kYellow+5 , "file":"/net/scratch_cms/institut_3b/hoehle/Nminus1_DiLepSelection/TTbarDiLepBck_2013-08-10_15-48-14/patRefSel_diLep_cfg_debughistos_T_TuneZ2_tW-channel-DR_7TeV-powheg-tauola__Fall11-PU_S6_START42_V14B-v1__AODSIM.root"}
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
ROOT.TH1.AddDirectory(False)
for plot in plots:
  histMan = MyHistFunctions.MyHistManager("hists_"+plot)
  tmpCan = ROOT.TCanvas("c_"+plot,plot,200,10,700,400);tmpCan.cd()
  for key,dataset in datasets.iteritems():
    tmpHist = (ROOT.TFile(dataset["file"]).Get(plot)).Clone("hist_"+key+"_"+plot)  
    tmpHist.Sumw2(); MyHistFunctions.addOverFlowToLastBin(tmpHist);tmpHist.SetLineColor(dataset["color"])
    tmpHist.Scale(Lint/(dataset["processedEvents"]/dataset["xSec"]));
    histMan.saveHist(tmpHist)
  stackHists = MyHistFunctions.stackHists(histMan.hists)
  histMans.append(histMan)
  stacksHists.append(stackHists)
  stackHists.createStack();stackHists.plotStack(False,"HIST")
  tmpCan.SaveAs(subSlash(tmpCan.GetName())+".pdf");tmpCan.SaveAs(subSlash(tmpCan.GetName())+".root")
