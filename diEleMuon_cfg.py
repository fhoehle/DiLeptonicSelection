import FWCore.ParameterSet.Config as cms
import os,imp
cfgFileTools = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools/cfgFileTools.py')
debugCollection = cfgFileTools.debugCollection

###################
class myElectronMuonPath():
  def __init__(self,runData,electronMuonTrigger):
    self.runData = runData
    self.electronMuonTrigger = electronMuonTrigger
  def doDiEleMuonPath(self,process,pPF,debugIt = False):
    AddFilters = cfgFileTools.AddFilterAndCreatePath(debugIt) 
    if debugIt:
        candPtHistogram = cms.PSet(min = cms.untracked.double(0), max = cms.untracked.double(400), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Pt'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('pt'))
        candEtaHistogram = cms.PSet(min = cms.untracked.double(-5), max = cms.untracked.double(5), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Eta'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('eta'))
    process.myDiElectronMuonPath = cms.Path(pPF._seq);localPath = process.myDiElectronMuonPath
    process.myMuonElectronTriggerCheck = cms.EDFilter("TriggerResultsFilter",l1tIgnoreMask = cms.bool(False),l1tResults = cms.InputTag(""),l1techIgnorePrescales = cms.bool(False),    hltResults = cms.InputTag("TriggerResults","","HLT"),  triggerConditions = cms.vstring(self.electronMuonTrigger),throw = cms.bool(False), daqPartitions = cms.uint32(1)); localPath += process.myMuonElectronTriggerCheck;#analyzeColl("patElectronsPF",localPath,process,"diEMuTriggerOK");analyzeColl("mySelectedPatMuons2p1",localPath,process,"Muon2p1")
    #if debugIt:debugCollection('mySelectedPatElectrons',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"DiEMu");
    process.mySelectedPatElectronsMuonsMinCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("mySelectedPatElectrons"), minNumber = cms.uint32(1));    localPath += process.mySelectedPatElectronsMuonsMinCount
    process.mySelectedPatMuonsElectronsMinCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("mySelectedPatMuons2p1"), minNumber = cms.uint32(1))
    #if debugIt:debugCollection('mySelectedPatMuons2p1',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"DiEMu");
    localPath += process.mySelectedPatMuonsElectronsMinCount
    process.DiLepCandEMu = cms.EDProducer("DiLepCandProducer",srcColl1 = cms.InputTag("mySelectedPatElectrons"), srcColl2 = cms.InputTag("mySelectedPatMuons2p1"),cut = cms.string("mass > 20 "),pairCut = cms.string("(abs(cand1.pt - cand2.pt) > 0.01 || abs(cand1.px - cand2.px) > 0.01) && abs(cand1.charge - cand2.charge) > 0.01 &&  totalP4.M > 20")); localPath += process.DiLepCandEMu; process.DiLepCandEMuCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("DiLepCandEMu"), minNumber = cms.uint32(1)); AddFilters.AddFilter(process.DiLepCandEMuCount,localPath,process);#analyzeColl("DiLepCandEMu",localPath,process,"DiLepEMuCandOKZVetoAlso");
    #analyzeColl("mySelectedPatElectrons",localPath,process,"diEMuDiLepCandOk")
    process.ElectronsUsedForDiLepCandEMu = cms.EDProducer("PATElectronCleaner",
      src = cms.InputTag("mySelectedPatElectrons"),
      preselection = cms.string(''),# preselection (any string-based cut for pat::Muon)
      checkOverlaps = cms.PSet(# overlap checking configurables
          muons = cms.PSet(
             src       = cms.InputTag("DiLepCandEMu"),
             algorithm = cms.string("byDeltaR"),
             preselection        = cms.string(""),  # don't preselect the muons
             deltaR              = cms.double(9999),
             checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
             pairCut             = cms.string('abs(cand1.pt-cand2.daughter("p1").pt)> 0.1 && abs(cand1.pt-cand2.daughter("p2").pt) > 0.1 '),
             requireNoOverlaps   = cms.bool(True), # overlaps don't cause the electron to be discared
          )
      ),
      finalCut = cms.string(''),# finalCut (any string-based cut for pat::Muon)
    ); localPath += process.ElectronsUsedForDiLepCandEMu;
    process.MuonsUsedForDiLepCandEMu = cms.EDProducer("PATMuonCleaner",
      src = cms.InputTag("mySelectedPatMuons2p1"),
      preselection = cms.string(''),# preselection (any string-based cut for pat::Muon)
      checkOverlaps = cms.PSet(# overlap checking configurables
          muons = cms.PSet(
             src       = cms.InputTag("DiLepCandEMu"),
             algorithm = cms.string("byDeltaR"),
             preselection        = cms.string(""),  # don't preselect the muons
             deltaR              = cms.double(9999),
             checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
             pairCut             = cms.string('abs(cand1.pt-cand2.daughter("p1").pt)> 0.1 && abs(cand1.pt-cand2.daughter("p2").pt) > 0.1 '),
             requireNoOverlaps   = cms.bool(True), # overlaps don't cause the electron to be discared
          )
      ),
      finalCut = cms.string(''),# finalCut (any string-based cut for pat::Muon)
    ); localPath += process.MuonsUsedForDiLepCandEMu; 
    if debugIt:debugCollection('MuonsUsedForDiLepCandEMu',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);debugCollection('ElectronsUsedForDiLepCandEMu',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
    process.MuonsUsedForDiLepCandEMuCount = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("MuonsUsedForDiLepCandEMu"), minNumber = cms.uint32(1) ); localPath += process.MuonsUsedForDiLepCandEMuCount;process.ElectronsUsedForDiLepCandEMuCount = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("ElectronsUsedForDiLepCandEMu"), minNumber = cms.uint32(1) ); localPath += process.ElectronsUsedForDiLepCandEMuCount
    process.cleanJetsDiEMu = process.cleanPatJetsPF.clone();process.cleanJetsDiEMu.checkOverlaps = cms.PSet(    electrons = cms.PSet(src = cms.InputTag("ElectronsUsedForDiLepCandEMu"),deltaR = cms.double(0.4),
        pairCut = cms.string(''), checkRecoComponents = cms.bool(False),
        algorithm = cms.string('byDeltaR'), preselection = cms.string(''), requireNoOverlaps = cms.bool(True)),muons = cms.PSet(src = cms.InputTag("MuonsUsedForDiLepCandEMu"),deltaR = cms.double(0.4),
        pairCut = cms.string(''), checkRecoComponents = cms.bool(False),
        algorithm = cms.string('byDeltaR'), preselection = cms.string(''), requireNoOverlaps = cms.bool(True))    );  localPath += process.cleanJetsDiEMu;
    #if debugIt:debugCollection('cleanJetsDiEMu',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
    process.cleanJetsDiEMuCount = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("cleanJetsDiEMu"), minNumber = cms.uint32(2) ); AddFilters.AddFilter(process.cleanJetsDiEMuCount,localPath,process);
    process.addBTagWeightsEMu = cms.EDProducer("AddMyBTagWeights",jetSrc = cms.InputTag("cleanJetsDiEMu"));localPath+=process.addBTagWeightsEMu 
    if debugIt:debugCollection('cleanJetsDiEMu',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"diEMuJetMOK");#analyzeColl("cleanJetsDiEMu",localPath,process,"cleanJetsDiEMuJetMOK"); 

