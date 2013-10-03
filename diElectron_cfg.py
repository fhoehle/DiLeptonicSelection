import FWCore.ParameterSet.Config as cms
import os,imp
cfgFileTools = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools/cfgFileTools.py')
debugCollection = cfgFileTools.debugCollection
AddFilters = cfgFileTools.AddFilters
###################
class myElectronPath:
  def __init__(self,runData,dataElectronTrigger):
    self.runData = runData
    self.dataElectronTrigger = dataElectronTrigger
  def doDiElectronPath(self,process,pPF,debugIt = False):
    if debugIt:
        candPtHistogram = cms.PSet(min = cms.untracked.double(0), max = cms.untracked.double(400), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Pt'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('pt'))
        candEtaHistogram = cms.PSet(min = cms.untracked.double(-5), max = cms.untracked.double(5), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Eta'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('eta'))
    ## my electron selection
    Zmax=106;Zmin=76
    diElectronTriggers = ""
    if self.runData:
      diElectronTriggers = self.dataElectronTrigger
    else:
      diElectronTriggers = "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v2"
    process.myDiElectronPath = cms.Path(pPF._seq); localPath = process.myDiElectronPath
    process.myDiElectronTriggerCheck = cms.EDFilter("TriggerResultsFilter",l1tIgnoreMask = cms.bool(False),l1tResults = cms.InputTag(""),l1techIgnorePrescales = cms.bool(False),    hltResults = cms.InputTag("TriggerResults","","HLT"),  triggerConditions = cms.vstring(diElectronTriggers),throw = cms.bool(False), daqPartitions = cms.uint32(1));  localPath += process.myDiElectronTriggerCheck;#analyzeColl("patElectronsPF",localPath,process,"diETriggerOK")
    coll='patElectronsPF'
    process.myTestAnalyzer = cms.EDAnalyzer("MyCandPrintAnalyzer", src = cms.InputTag(coll), prefix = cms.string("test"+coll),
    quantity = cms.vstring('px', 'py', 'pz', 'energy', 'pt', 'eta', 'phi','gsfTrack.trackerExpectedHitsInner.numberOfLostHits' ,'abs(userFloat("deltaCotTheta"))',' abs(userFloat("deltaDistance"))', 'electronID("simpleEleId90cIso")','(neutralHadronIso + chargedHadronIso + photonIso)/pt','neutralHadronIso ',' chargedHadronIso ',' photonIso','abs(dB)'));localPath += process.myTestAnalyzer
    if debugIt:debugCollection('mySelectedPatElectrons',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);#analyzeColl("mySelectedPatElectrons",localPath,process,"diETriggerOK")
    process.mySelectedPatElectronsMinCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("mySelectedPatElectrons"), minNumber = cms.uint32(2)); process.mySelectedPatElectronsMaxCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(2), src = cms.InputTag("mySelectedPatElectrons"), minNumber = cms.uint32(0)); localPath += process.mySelectedPatElectronsMinCount; localPath += process.mySelectedPatElectronsMaxCount
    process.DiLepCandElectrons = cms.EDProducer("DiLepCandProducer",srcColl1 = cms.InputTag("mySelectedPatElectrons"), srcColl2 = cms.InputTag("mySelectedPatElectrons"),cut = cms.string("mass >= 20 "),pairCut = cms.string("(abs(ele1.pt - ele2.pt) > 0.1 || abs(ele1.px - ele2.px) > 0.1) && abs(ele1.charge - ele2.charge) > 0.1 &&  totalP4.M >= 20")); localPath += process.DiLepCandElectrons;#analyzeColl("mySelectedPatElectrons",localPath,process,"diElTestEls");analyzeColl("DiLepCandElectrons",localPath,process,"diElTestEls") 
    if debugIt:debugCollection('DiLepCandElectrons',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
    process.DiLepCandElectronsCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("DiLepCandElectrons"), minNumber = cms.uint32(1));AddFilters.AddFilter(process.DiLepCandElectronsCount,localPath,process);#analyzeColl("DiLepCandElectrons",localPath,process,"DiLepEleCandOK");
    process.ElectronsUsedForDiLepCand = cms.EDProducer("PATElectronCleaner",
      src = cms.InputTag("mySelectedPatElectrons"),
      preselection = cms.string(''),# preselection (any string-based cut for pat::Muon)
      checkOverlaps = cms.PSet(# overlap checking configurables
          muons = cms.PSet(
             src       = cms.InputTag("DiLepCandElectrons"),
             algorithm = cms.string("byDeltaR"),
             preselection        = cms.string(""),  # don't preselect the muons
             deltaR              = cms.double(9999),
             checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
             pairCut             = cms.string('abs(cand1.pt-cand2.daughter("p1").pt)> 0.1 && abs(cand1.pt-cand2.daughter("p2").pt) > 0.1 '),
             requireNoOverlaps   = cms.bool(True), # overlaps don't cause the electron to be discared
          )
      ),
      finalCut = cms.string(''),# finalCut (any string-based cut for pat::Muon)
    ); localPath += process.ElectronsUsedForDiLepCand
    if debugIt:debugCollection('ElectronsUsedForDiLepCand',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"DiLepCandOkDiEl");
    process.cleanJetsDiElectron = process.cleanPatJetsPF.clone();process.cleanJetsDiElectron.checkOverlaps = cms.PSet(    electrons = cms.PSet(src = cms.InputTag("ElectronsUsedForDiLepCand"),deltaR = cms.double(0.4),
        pairCut = cms.string(''), checkRecoComponents = cms.bool(False),
        algorithm = cms.string('byDeltaR'), preselection = cms.string(''), requireNoOverlaps = cms.bool(True))    );  localPath += process.cleanJetsDiElectron; 
    if debugIt:debugCollection('cleanJetsDiElectron',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
    process.DiLepCandElectronsZVeto = cms.EDFilter("PATCompositeCandidateRefSelector", src = cms.InputTag("DiLepCandElectrons"), cut = cms.string("mass < "+str(Zmin) + " || mass > "+str(Zmax)) ); localPath += process.DiLepCandElectronsZVeto; process.DiLepCandElectronsZVetoCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("DiLepCandElectronsZVeto"), minNumber = cms.uint32(1));AddFilters.AddFilter(process.DiLepCandElectronsZVetoCount,localPath,process);#analyzeColl("DiLepCandElectronsZVeto",localPath,process,"diEleZVetoOK")
    process.cleanJetsDiElectronCount = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("cleanJetsDiElectron"), minNumber = cms.uint32(2) ); AddFilters.AddFilter(process.cleanJetsDiElectronCount,localPath,process);
    process.addBTagWeightsDiE = cms.EDProducer("AddMyBTagWeights",jetSrc = cms.InputTag("cleanJetsDiElectron")); localPath += process.addBTagWeightsDiE 
    if debugIt:debugCollection('cleanJetsDiElectron',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"DiEJetMOK");#analyzeColl("cleanJetsDiElectron",localPath,process,"cleanJetsDiElectronJetMOK");
    process.DiElectronmyselectedPatMETs = cms.EDFilter("PATMETSelector",  src = cms.InputTag("patMETsPF"),     cut = cms.string("energy > 40") ); localPath += process.DiElectronmyselectedPatMETs
    #if debugIt:debugCollection('DiMuonmyselectedPatMETs',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
    process.DiElectronmyselectedPatMETsCount = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("DiElectronmyselectedPatMETs"), minNumber = cms.uint32(1) ); AddFilters.AddFilter(process.DiElectronmyselectedPatMETsCount,localPath,process);

