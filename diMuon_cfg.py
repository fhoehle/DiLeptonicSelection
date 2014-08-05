import FWCore.ParameterSet.Config as cms
import os,imp
cfgFileTools = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools/cfgFileTools.py')
debugCollection = cfgFileTools.debugCollection
###########################
class myMuonPath:
  def __init__(self,runData,muonTrigger):
    self.runData = runData
    self.muonTrigger = muonTrigger
    self.muonPathName = "myDiMuonPath"
  def doDiMuonPath(self,process,pPF,debugIt = False):
      AddFilters = cfgFileTools.AddFilterAndCreatePath(debugIt)
      if debugIt:
        candPtHistogram = cms.PSet(min = cms.untracked.double(0), max = cms.untracked.double(400), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Pt'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('pt'))
        candEtaHistogram = cms.PSet(min = cms.untracked.double(-5), max = cms.untracked.double(5), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Eta'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('eta'))
      #################
      Zmax=106;Zmin=76
      setattr(process,self.muonPathName, cms.Path(pPF._seq)); localPath = getattr(process,self.muonPathName)
      process.myDiMuonTriggerCheck = cms.EDFilter("TriggerResultsFilter",l1tIgnoreMask = cms.bool(False),l1tResults = cms.InputTag(""),l1techIgnorePrescales = cms.bool(False),    hltResults = cms.InputTag("TriggerResults","","HLT"),  triggerConditions = cms.vstring(self.muonTrigger),throw = cms.bool(False), daqPartitions = cms.uint32(1));  localPath += process.myDiMuonTriggerCheck;#analyzeColl("patMuonsPF",localPath,process,"diMuTriggerOK")
      #my di muon selection
      if debugIt:debugCollection('mySelectedPatMuons',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);debugCollection('mySelectedPatMuons2p1',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
      process.mySelectedPatMuonsMinCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("mySelectedPatMuons"), minNumber = cms.uint32(2))
      process.mySelectedPatMuonsMaxCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(2), src = cms.InputTag("mySelectedPatMuons"), minNumber = cms.uint32(0))
      process.mySelectedPatMuons2p1Count = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(2), src = cms.InputTag("mySelectedPatMuons2p1"), minNumber = cms.uint32(1))
      localPath += process.mySelectedPatMuonsMinCount;localPath += process.mySelectedPatMuonsMaxCount;localPath += process.mySelectedPatMuons2p1Count
      process.DiLepCandMuons = cms.EDProducer("DiLepCandProducer",srcColl1 = cms.InputTag("mySelectedPatMuons"), srcColl2 = cms.InputTag("mySelectedPatMuons"),cut = cms.string("mass > 20 "),pairCut = cms.string("(abs(mu1.pt - mu2.pt) > 0.1 || abs(mu1.px - mu2.px) > 0.1) && abs(mu1.charge - mu2.charge) > 0.1 &&  totalP4.M > 20")); localPath += process.DiLepCandMuons;
      if debugIt:debugCollection('DiLepCandMuons',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);#analyzeColl("DiLepCandMuons",localPath,process,"DiLepCandOK");analyzeColl("mySelectedPatMuons",localPath,process,"MuonTest");
      process.DiLepCandMuonsCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("DiLepCandMuons"), minNumber = cms.uint32(1));AddFilters.AddFilter(process.DiLepCandMuonsCount,localPath,process);#analyzeColl("DiLepCandMuons",localPath,process,"DiLepCandOK");analyzeColl("mySelectedPatMuons",localPath,process,"MuonTest");
      #analyzeColl("DiLepCandMuons",localPath,process,"BOOMDiLepCandZVetoOK")
      process.MuonsUsedForDiLepCand = cms.EDProducer("PATMuonCleaner",
        src = cms.InputTag("mySelectedPatMuons"),
        preselection = cms.string(''),# preselection (any string-based cut for pat::Muon)
        checkOverlaps = cms.PSet(# overlap checking configurables
            muons = cms.PSet(
               src       = cms.InputTag("DiLepCandMuons"),
               algorithm = cms.string("byDeltaR"),
               preselection        = cms.string(""),  # don't preselect the muons
               deltaR              = cms.double(9999),
               checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
               pairCut             = cms.string('abs(cand1.pt-cand2.daughter("p1").pt)> 0.1 && abs(cand1.pt-cand2.daughter("p2").pt) > 0.1 '),
               requireNoOverlaps   = cms.bool(True), # overlaps don't cause the electron to be discared
            )
        ),
        finalCut = cms.string(''),# finalCut (any string-based cut for pat::Muon)
      ); localPath += process.MuonsUsedForDiLepCand
      if debugIt:debugCollection('MuonsUsedForDiLepCand',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);#analyzeColl("MuonsUsedForDiLepCand",localPath,process,"MuonUsedTest");
      #analyzeColl("selectedPatJetsPF",localPath,process,"diMuontestSelPatJet")
      #analyzeColl("MuonsUsedForDiLepCand",localPath,process,"diMuontestMuonsUsedForDiLepCand")
      process.cleanJetsDiMuon = process.cleanPatJetsPF.clone();process.cleanJetsDiMuon.checkOverlaps = cms.PSet(    muons = cms.PSet(src = cms.InputTag("MuonsUsedForDiLepCand"),deltaR = cms.double(0.4),
          pairCut = cms.string(''), checkRecoComponents = cms.bool(False),
          algorithm = cms.string('byDeltaR'), preselection = cms.string(''), requireNoOverlaps = cms.bool(True))    );  localPath += process.cleanJetsDiMuon
      #if debugIt:debugCollection('cleanJetsDiMuon',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
      process.DiLepCandMuonsZVeto = cms.EDFilter("PATCompositeCandidateRefSelector", src = cms.InputTag("DiLepCandMuons"), cut = cms.string("mass < "+str(Zmin) + " || mass > "+str(Zmax)) ); localPath += process.DiLepCandMuonsZVeto; 
      #if debugIt:debugCollection('DiLepCandMuonsZVeto',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
      process.DiLepCandMuonsZVetoCount = cms.EDFilter("PATCandViewCountFilter", maxNumber = cms.uint32(99), src = cms.InputTag("DiLepCandMuonsZVeto"), minNumber = cms.uint32(1));AddFilters.AddFilter(process.DiLepCandMuonsZVetoCount,localPath,process);#analyzeColl("DiLepCandMuonsZVeto",localPath,process,"BOOMDiLepCandZVetoOK")
      process.cleanJetsDiMuonCount =  cms.EDFilter("CandViewCountFilter", src = cms.InputTag("cleanJetsDiMuon"), minNumber = cms.uint32(2) ); AddFilters.AddFilter(process.cleanJetsDiMuonCount,localPath,process);
      process.addBTagWeightsDiMu = cms.EDProducer("AddMyBTagWeights",jetSrc = cms.InputTag("cleanJetsDiMuon"));localPath += process.addBTagWeightsDiMu
      if debugIt:debugCollection('cleanJetsDiMuon',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"DiMuJetMOk");#analyzeColl("cleanJetsDiMuon",localPath,process,"cleanJetsDiMuonJetMOK");analyzeColl("cleanJetsDiMuon",localPath,process,"JetMOK")
      process.DiMuonmyselectedPatMETs = cms.EDFilter("PATMETSelector",  src = cms.InputTag("patMETsPF"),     cut = cms.string("energy > 40") ); localPath += process.DiMuonmyselectedPatMETs
      #if debugIt:debugCollection('DiMuonmyselectedPatMETs',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process);
      process.DiMuonmyselectedPatMETsCount = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("DiMuonmyselectedPatMETs"), minNumber = cms.uint32(1) ); AddFilters.AddFilter(process.DiMuonmyselectedPatMETsCount,localPath,process);#localPath += process.DiMuonmyselectedPatMETsCount
      if debugIt:debugCollection('DiMuonmyselectedPatMETs',localPath,cms.VPSet(candPtHistogram,candEtaHistogram),process,"diMuonMETOK") 
  
