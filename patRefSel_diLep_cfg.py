#
# This file contains the Top PAG reference selection work-flow for mu + jets analysis.
# as defined in
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopLeptonPlusJetsRefSel_mu#Selection_Version_SelV4_valid_fr
#
import imp,os
executeDiElectronPath = False
diMuon_cfg = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/DiLeptonicSelection/diMuon_cfg.py')
cfgFileTools = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/Tools/cfgFileTools.py')
debugCollection = cfgFileTools.debugCollection
executeDiMuonPath = True
executeDiElectronMuonPath = False
import sys
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.register ('eventsToProcess',
                   '',
                   VarParsing.multiplicity.list,
                   VarParsing.varType.string,
                   "Events to process")
options.register('runOnTTbar',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'runOnTTbar')
#options.register('filterSignal',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'filterSignal')
options.parseArguments()
import FWCore.ParameterSet.Config as cms
#def analyzeCollection(coll):
def analyzeColl(coll,path,process,prefix=''):
 newmod = cms.EDAnalyzer("MyCandPrintAnalyzer", src = cms.InputTag(coll), prefix = cms.string(prefix+"test"+coll),
    quantity = cms.vstring('px', 'py', 'pz', 'energy', 'pt', 'eta', 'phi'))
 setattr(process,prefix+"test"+coll,newmod)
 path += getattr(process,prefix+"test"+coll)

######################
process = cms.Process( 'PAT' )
AddFilters = cfgFileTools.AddFilters
#######
#dump cmsRun parameters
print "this is cmsRun input: ",sys.argv

### Data or MC?
runOnMC = True

# PF2PAT
runPF2PAT = True

### Switch on/off selection steps

# Step 1b
useTightMuon    = True
# Step 2
useMuonVeto     = True
# Step 3
useElectronVeto = True
# Step 4a
use1Jet         = True
# Step 4b
use2Jets        = False
# Step 4c
use3Jets        = False
# Step 5
use4Jets        = False
# Step 6
useBTag         = False

addTriggerMatching = True

### Reference selection

from TopQuarkAnalysis.Configuration.patRefSel_refMuJets import *
postfix = 'PF' # needs to be a non-empty string, if 'runStandardPAT' = True

# subtract charged hadronic pile-up particles (from wrong PVs)
# effects also JECs
usePFnoPU       = True  # before any top projection
usePfIsoLessCHS = False # switch to new PF isolation with L1Fastjet CHS

# other switches for PF top projections (default: all 'True')
useNoMuon     = True # before electron top projection
useNoElectron = True # before jet top projection
useNoJet      = True # before tau top projection
useNoTau      = True # before MET top projection


### JEC levels

# levels to be accessible from the jets
# jets are corrected to L3Absolute (MC), L2L3Residual (data) automatically, if enabled here
# and remain uncorrected, if none of these levels is enabled here
useL1FastJet    = True  # needs useL1Offset being off, error otherwise
useL1Offset     = False # needs useL1FastJet being off, error otherwise
useL2Relative   = True
useL3Absolute   = True
useL2L3Residual = True  # takes effect only on data
useL5Flavor     = False
useL7Parton     = False

### Input
# maximum number of events
maxInputEvents = -1 # reduce for testing

### Conditions

# GlobalTags (w/o suffix '::All')
globalTagData = 'GR_R_42_V23'
globalTagMC   = 'START42_V17'

### Output

# output file
outputFile = 'patRefSel_diLep_cfg_output.root'

# event frequency of Fwk report
fwkReportEvery = 1

# switch for 'TrigReport'/'TimeReport' at job end
wantSummary = True

###
### Basic configuration
###

process.load( "TopQuarkAnalysis.Configuration.patRefSel_basics_cff" )
process.MessageLogger.cerr.FwkReport.reportEvery = fwkReportEvery
process.options.wantSummary = wantSummary
if runOnMC:
  process.GlobalTag.globaltag = globalTagMC   + '::All'
else:
  process.GlobalTag.globaltag = globalTagData + '::All'


###
### Input configuration
###

process.load( "TopQuarkAnalysis.Configuration.patRefSel_inputModule_cfi" )
process.source.fileNames.append("/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FED956DF-7F2A-E111-8124-002618943958.root")
print "default source ",process.source.fileNames
if options.inputFiles != cms.untracked.vstring():
 process.source.fileNames=options.inputFiles
if options.eventsToProcess:
 process.source.eventsToProcess = cms.untracked.VEventRange (options.eventsToProcess)
if options.maxEvents != '':
 print "maxEvents",options.maxEvents
 process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))


###
### Output configuration
###

process.load( "TopQuarkAnalysis.Configuration.patRefSel_outputModule_cff" )
# output file name
process.out.fileName = outputFile
# event content
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out.outputCommands += patEventContent
# clear event selection
process.out.SelectEvents.SelectEvents = []


###
### Cleaning and trigger selection configuration
###

### Trigger selection
if runOnMC:
  # diMuon triggers
  diMuonTriggers = "HLT_DoubleMu6_v*"
  mytriggerSelection = diMuonTriggers 
  # di Electron triggers
  diElectronTriggers = "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v2 OR HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v8"
  mytriggerSelection += " OR " + diElectronTriggers
  # ele muon triggers
  MuonElectronTriggers = "HLT_Mu8_Ele17_CaloIdL_v* OR HLT_Mu10_Ele10_CaloIdL_v3"
  mytriggerSelection += " OR " + MuonElectronTriggers
  triggerSelection = mytriggerSelection
  print "triggerSelection my  ",triggerSelection
else:
  triggerSelection = triggerSelectionData
from TopQuarkAnalysis.Configuration.patRefSel_triggerSelection_cff import triggerResults
process.step0a = triggerResults.clone(
  triggerConditions = [ triggerSelection ]
)

### Good vertex selection
process.load( "TopQuarkAnalysis.Configuration.patRefSel_goodVertex_cfi" )
process.step0b = process.goodOfflinePrimaryVertices.clone( filter = True )

### Event cleaning
process.load( 'TopQuarkAnalysis.Configuration.patRefSel_eventCleaning_cff' )
process.step0c = cms.Sequence(
  process.HBHENoiseFilter
+ process.scrapingFilter
)


###
### PAT/PF2PAT configuration
###

pfSuffix = 'PF'

process.load( "PhysicsTools.PatAlgos.patSequences_cff" )
from PhysicsTools.PatAlgos.tools.coreTools import *

### Check JECs

# JEC set
jecSet      = jecSetBase + 'Calo'
jecSetAddPF = jecSetBase + pfSuffix
jecSetPF    = jecSetAddPF
if usePFnoPU:
  jecSetPF += 'chs'

# JEC levels
if useL1FastJet and useL1Offset:
  sys.exit( 'ERROR: switch off either "L1FastJet" or "L1Offset"' )
jecLevels = []
if useL1FastJet:
  jecLevels.append( 'L1FastJet' )
if useL1Offset:
  jecLevels.append( 'L1Offset' )
if useL2Relative:
  jecLevels.append( 'L2Relative' )
if useL3Absolute:
  jecLevels.append( 'L3Absolute' )
if useL2L3Residual and not runOnMC:
  jecLevels.append( 'L2L3Residual' )
if useL5Flavor:
  jecLevels.append( 'L5Flavor' )
if useL7Parton:
  jecLevels.append( 'L7Parton' )

### Switch configuration

if runPF2PAT:
  from PhysicsTools.PatAlgos.tools.pfTools import *
  usePF2PAT( process
           , runPF2PAT      = runPF2PAT
           , runOnMC        = runOnMC
           , jetAlgo        = jetAlgo
           , postfix        = postfix
           , jetCorrections = ( jecSetPF
                              , jecLevels
                              )
           )
  adaptPFTaus( process, tauType='hpsPFTau', postfix=postfix )
  applyPostfix( process, 'pfNoPileUp'  , postfix ).enable = usePFnoPU
  applyPostfix( process, 'pfNoMuon'    , postfix ).enable = useNoMuon
  applyPostfix( process, 'pfNoElectron', postfix ).enable = useNoElectron
  applyPostfix( process, 'pfNoJet'     , postfix ).enable = useNoJet
  applyPostfix( process, 'pfNoTau'     , postfix ).enable = useNoTau
  applyPostfix( process, 'pfPileUp', postfix ).Vertices = cms.InputTag( pfVertices )
  if useL1FastJet:
    applyPostfix( process, 'pfPileUp'   , postfix ).checkClosestZVertex = False
    applyPostfix( process, 'pfPileUpIso', postfix ).checkClosestZVertex = usePfIsoLessCHS
    applyPostfix( process, 'pfJets', postfix ).doAreaFastjet = True
    applyPostfix( process, 'pfJets', postfix ).doRhoFastjet  = False
  applyPostfix( process, 'pfMuonsFromVertex'    , postfix ).vertices = cms.InputTag( pfVertices )
  applyPostfix( process, 'pfMuonsFromVertex'    , postfix ).d0Cut    = pfD0Cut
  applyPostfix( process, 'pfMuonsFromVertex'    , postfix ).dzCut    = pfDzCut
  applyPostfix( process, 'pfSelectedMuons'      , postfix ).cut = pfMuonSelectionCut
  applyPostfix( process, 'pfIsolatedMuons'      , postfix ).isolationCut = pfMuonCombIsoCut
  if pfMuonIsoConeR03:
    applyPostfix( process, 'pfIsolatedMuons', postfix ).isolationValueMapsCharged  = cms.VInputTag( cms.InputTag( 'muPFIsoValueCharged03' + postfix )
                                                                                                  )
    applyPostfix( process, 'pfIsolatedMuons', postfix ).deltaBetaIsolationValueMap = cms.InputTag( 'muPFIsoValuePU03' + postfix )
    applyPostfix( process, 'pfIsolatedMuons', postfix ).isolationValueMapsNeutral  = cms.VInputTag( cms.InputTag( 'muPFIsoValueNeutral03' + postfix )
                                                                                                  , cms.InputTag( 'muPFIsoValueGamma03' + postfix )
                                                                                                  )
    applyPostfix( process, 'pfMuons', postfix ).isolationValueMapsCharged  = cms.VInputTag( cms.InputTag( 'muPFIsoValueCharged03' + postfix )
                                                                                          )
    applyPostfix( process, 'pfMuons', postfix ).deltaBetaIsolationValueMap = cms.InputTag( 'muPFIsoValuePU03' + postfix )
    applyPostfix( process, 'pfMuons', postfix ).isolationValueMapsNeutral  = cms.VInputTag( cms.InputTag( 'muPFIsoValueNeutral03' + postfix )
                                                                                          , cms.InputTag( 'muPFIsoValueGamma03' + postfix )
                                                                                          )
    applyPostfix( process, 'patMuons', postfix ).isolationValues.pfNeutralHadrons   = cms.InputTag( 'muPFIsoValueNeutral03' + postfix )
    applyPostfix( process, 'patMuons', postfix ).isolationValues.pfChargedAll       = cms.InputTag( 'muPFIsoValueChargedAll03' + postfix )
    applyPostfix( process, 'patMuons', postfix ).isolationValues.pfPUChargedHadrons = cms.InputTag( 'muPFIsoValuePU03' + postfix )
    applyPostfix( process, 'patMuons', postfix ).isolationValues.pfPhotons          = cms.InputTag( 'muPFIsoValueGamma03' + postfix )
    applyPostfix( process, 'patMuons', postfix ).isolationValues.pfChargedHadrons   = cms.InputTag( 'muPFIsoValueCharged03' + postfix )
  applyPostfix( process, 'pfElectronsFromVertex'    , postfix ).vertices = cms.InputTag( pfVertices )
  applyPostfix( process, 'pfElectronsFromVertex'    , postfix ).d0Cut    = pfD0Cut
  applyPostfix( process, 'pfElectronsFromVertex'    , postfix ).dzCut    = pfDzCut
  applyPostfix( process, 'pfSelectedElectrons'      , postfix ).cut = pfElectronSelectionCut
  applyPostfix( process, 'pfIsolatedElectrons'      , postfix ).isolationCut = pfElectronCombIsoCut
  if pfElectronIsoConeR03:
    applyPostfix( process, 'pfIsolatedElectrons', postfix ).isolationValueMapsCharged  = cms.VInputTag( cms.InputTag( 'elPFIsoValueCharged03' + postfix )
                                                                                                      )
    applyPostfix( process, 'pfIsolatedElectrons', postfix ).deltaBetaIsolationValueMap = cms.InputTag( 'elPFIsoValuePU03' + postfix )
    applyPostfix( process, 'pfIsolatedElectrons', postfix ).isolationValueMapsNeutral  = cms.VInputTag( cms.InputTag( 'elPFIsoValueNeutral03' + postfix )
                                                                                                      , cms.InputTag( 'elPFIsoValueGamma03' + postfix )
                                                                                                      )
    applyPostfix( process, 'pfElectrons', postfix ).isolationValueMapsCharged  = cms.VInputTag( cms.InputTag( 'elPFIsoValueCharged03' + postfix )
                                                                                              )
    applyPostfix( process, 'pfElectrons', postfix ).deltaBetaIsolationValueMap = cms.InputTag( 'elPFIsoValuePU03' + postfix )
    applyPostfix( process, 'pfElectrons', postfix ).isolationValueMapsNeutral  = cms.VInputTag( cms.InputTag( 'elPFIsoValueNeutral03' + postfix )
                                                                                              , cms.InputTag( 'elPFIsoValueGamma03' + postfix )
                                                                                              )
    applyPostfix( process, 'patElectrons', postfix ).isolationValues.pfNeutralHadrons   = cms.InputTag( 'elPFIsoValueNeutral03' + postfix )
    applyPostfix( process, 'patElectrons', postfix ).isolationValues.pfChargedAll       = cms.InputTag( 'elPFIsoValueChargedAll03' + postfix )
    applyPostfix( process, 'patElectrons', postfix ).isolationValues.pfPUChargedHadrons = cms.InputTag( 'elPFIsoValuePU03' + postfix )
    applyPostfix( process, 'patElectrons', postfix ).isolationValues.pfPhotons          = cms.InputTag( 'elPFIsoValueGamma03' + postfix )
    applyPostfix( process, 'patElectrons', postfix ).isolationValues.pfChargedHadrons   = cms.InputTag( 'elPFIsoValueCharged03' + postfix )
  applyPostfix( process, 'patElectrons', postfix ).pvSrc = cms.InputTag( pfVertices )
  applyPostfix( process, 'patMuons'    , postfix ).pvSrc = cms.InputTag( pfVertices )

from TopQuarkAnalysis.Configuration.patRefSel_refMuJets_cfi import *

# remove MC matching, object cleaning, objects etc.
jecLevelsCalo = copy.copy( jecLevels )
if runPF2PAT:
  if not runOnMC:
    runOnData( process
             , names = [ 'PFAll' ]
             , postfix = postfix
             )
  removeSpecificPATObjects( process
                          , names = [ 'Photons', 'Taus' ]
                          , postfix = postfix
                          ) # includes 'removeCleaning'
# additional event content has to be (re-)added _after_ the call to 'removeCleaning()':
process.out.outputCommands += [ 'keep edmTriggerResults_*_*_*'
                              , 'keep *_hltTriggerSummaryAOD_*_*'
                              # vertices and beam spot
                              , 'keep *_offlineBeamSpot_*_*'
                              , 'keep *_offlinePrimaryVertices*_*_*'
                              , 'keep *_goodOfflinePrimaryVertices*_*_*'
                              ]
if runOnMC:
  process.out.outputCommands += [ 'keep GenEventInfoProduct_*_*_*'
                                , 'keep recoGenParticles_*_*_*'
                                , 'keep *_addPileupInfo_*_*'
                                ]


###
### Additional configuration
###

goodPatJetsAddPFLabel = 'goodPatJets' + jetAlgo + pfSuffix


if runPF2PAT:

  ### Muons

  intermediatePatMuonsPF = intermediatePatMuons.clone( src = cms.InputTag( 'selectedPatMuons' + postfix ) )
  setattr( process, 'intermediatePatMuons' + postfix, intermediatePatMuonsPF )

  loosePatMuonsPF = loosePatMuons.clone( src = cms.InputTag( 'intermediatePatMuons' + postfix ) )
  setattr( process, 'loosePatMuons' + postfix, loosePatMuonsPF )
  getattr( process, 'loosePatMuons' + postfix ).checkOverlaps.jets.src = cms.InputTag( 'goodPatJets' + postfix )

  step1aPF = step1a.clone( src = cms.InputTag( 'loosePatMuons' + postfix ) )
  setattr( process, 'step1a' + postfix, step1aPF )

  tightPatMuonsPF = tightPatMuons.clone( src = cms.InputTag( 'loosePatMuons' + postfix ) )
  setattr( process, 'tightPatMuons' + postfix, tightPatMuonsPF )

  step1bPF = step1b.clone( src = cms.InputTag( 'tightPatMuons' + postfix ) )
  setattr( process, 'step1b' + postfix, step1bPF )

  step2PF = step2.clone( src = cms.InputTag( 'selectedPatMuons' + postfix ) )
  setattr( process, 'step2' + postfix, step2PF )

  ### Jets

  applyPostfix( process, 'patJetCorrFactors', postfix ).primaryVertices = cms.InputTag( pfVertices )
  setattr( process, 'kt6PFJets' + postfix, kt6PFJets )
  getattr( process, 'patPF2PATSequence' + postfix).replace( getattr( process, 'patJetCorrFactors' + postfix )
                                                          , getattr( process, 'kt6PFJets' + postfix ) * getattr( process, 'patJetCorrFactors' + postfix )
                                                          )
  if useL1FastJet:
    applyPostfix( process, 'patJetCorrFactors', postfix ).rho = cms.InputTag( 'kt6PFJets' + postfix, 'rho' )
  process.out.outputCommands.append( 'keep double_kt6PFJets' + postfix + '_*_' + process.name_() )

  goodPatJetsPF = goodPatJets.clone( src = cms.InputTag( 'selectedPatJets' + postfix ) )
  setattr( process, 'goodPatJets' + postfix, goodPatJetsPF )
  getattr( process, 'goodPatJets' + postfix ).checkOverlaps.muons.src = cms.InputTag( 'intermediatePatMuons' + postfix )

  step4aPF = step4a.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
  setattr( process, 'step4a' + postfix, step4aPF )
  step4bPF = step4b.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
  setattr( process, 'step4b' + postfix, step4bPF )
  step4cPF = step4c.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
  setattr( process, 'step4c' + postfix, step4cPF )
  step5PF = step5.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
  setattr( process, 'step5'  + postfix, step5PF  )

  ### Electrons

  step3PF = step3.clone( src = cms.InputTag( 'selectedPatElectrons' + postfix ) )
  setattr( process, 'step3' + postfix, step3PF )

process.out.outputCommands.append( 'keep *_intermediatePatMuons*_*_*' )
process.out.outputCommands.append( 'keep *_loosePatMuons*_*_*' )
process.out.outputCommands.append( 'keep *_tightPatMuons*_*_*' )
process.out.outputCommands.append( 'keep *_goodPatJets*_*_*' )


###
### Selection configuration
###

if runPF2PAT:

  applyPostfix( process, 'patMuons', postfix ).usePV      = muonsUsePV
  applyPostfix( process, 'patMuons', postfix ).embedTrack = muonEmbedTrack

  applyPostfix( process, 'selectedPatMuons', postfix ).cut = muonCutPF

  getattr( process, 'intermediatePatMuons' + postfix ).preselection = looseMuonCutPF

  getattr( process, 'loosePatMuons' + postfix ).preselection              = looseMuonCutPF
  getattr( process, 'loosePatMuons' + postfix ).checkOverlaps.jets.deltaR = muonJetsDR

  getattr( process, 'tightPatMuons' + postfix ).preselection = tightMuonCutPF

  ### Jets

  getattr( process, 'goodPatJets' + postfix ).preselection               = jetCutPF
  getattr( process, 'goodPatJets' + postfix ).checkOverlaps.muons.deltaR = jetMuonsDRPF

  ### Electrons

  applyPostfix( process, 'patElectrons', postfix ).electronIDSources = electronIDSources

  applyPostfix( process, 'selectedPatElectrons', postfix ).cut = electronCutPF


###
### Trigger matching
###

if addTriggerMatching:

  if runOnMC:
    triggerObjectSelection = triggerObjectSelectionMC
  else:
    triggerObjectSelection = triggerObjectSelectionData
  ### Trigger matching configuration
  from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi import patTrigger
  from TopQuarkAnalysis.Configuration.patRefSel_triggerMatching_cfi import patMuonTriggerMatch
  from PhysicsTools.PatAlgos.tools.trigTools import *
  if runPF2PAT:
    triggerProducerPF = patTrigger.clone()
    setattr( process, 'patTrigger' + postfix, triggerProducerPF )
    triggerMatchPF = patMuonTriggerMatch.clone( matchedCuts = triggerObjectSelection )
    setattr( process, 'triggerMatch' + postfix, triggerMatchPF )
    switchOnTriggerMatchEmbedding( process
                                 , triggerProducer = 'patTrigger' + postfix
                                 , triggerMatchers = [ 'triggerMatch' + postfix ]
                                 , sequence        = 'patPF2PATSequence' + postfix
                                 , postfix         = postfix
                                 )
    removeCleaningFromTriggerMatching( process
                                     , sequence = 'patPF2PATSequence' + postfix
                                     )
    getattr( process, 'intermediatePatMuons' + postfix ).src = cms.InputTag( 'selectedPatMuons' + postfix + 'TriggerMatch' )


###
### Scheduling
###

# CiC electron ID

process.load( "RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentificationV06_cfi" )
process.eidCiCSequence = cms.Sequence(
  process.eidVeryLooseMC
+ process.eidLooseMC
+ process.eidMediumMC
+ process.eidTightMC
+ process.eidSuperTightMC
+ process.eidHyperTight1MC
+ process.eidHyperTight2MC
+ process.eidHyperTight3MC
+ process.eidHyperTight4MC
)

# The additional sequence
if runPF2PAT:
  patAddOnSequence = cms.Sequence(
    getattr( process, 'intermediatePatMuons' + postfix )
  * getattr( process, 'goodPatJets' + postfix )
  * getattr( process, 'loosePatMuons' + postfix )
  * getattr( process, 'tightPatMuons' + postfix )
  )
  setattr( process, 'patAddOnSequence' + postfix, patAddOnSequence )

# The paths
if runPF2PAT:

  pPF = cms.Path()
  pPF += process.goodOfflinePrimaryVertices
  pPF += process.eidCiCSequence
  pPF += getattr( process, 'patPF2PATSequence' + postfix )
  pPF += getattr( process, 'patAddOnSequence' + postfix )
  process.mySelectedPatMET = cms.EDFilter("PATMETSelector", src = cms.InputTag('patMETs'+postfix), cut = cms.string("pt > 30") );  pPF += process.mySelectedPatMET
  process.pfNoMuonPF.enable = False
  process.pfNoElectronPF.enable = False
  process.pfNoTauPF.enable = False
  process.patMuonsPF.isolationValues = cms.PSet(
    pfNeutralHadrons = cms.InputTag("muPFIsoValueNeutral03PF"),
    pfPUChargedHadrons = cms.InputTag("muPFIsoValuePU03PF"),
    pfPhotons = cms.InputTag("muPFIsoValueGamma03PF"),
    pfChargedHadrons = cms.InputTag("muPFIsoValueCharged03PF")
  )
  process.pfIsolatedMuonsPF.isolationCut = 99
  process.kt6PFJetsPF.Rho_EtaMax = cms.double(2.5); process.kt6PFJetsPF.doRhoFastjet = cms.bool(True)
  process.kt6PFJetsPF.src = cms.InputTag("particleFlow")
  process.kt6PFJetsPF.doAreaFastjet = False
  process.patJetCorrFactorsPF.primaryVertices = cms.InputTag("offlinePrimaryVertices")
  process.selectedPatJetsPF.cut = cms.string('pt > 30. && abs(eta) < 2.5 && chargedHadronEnergyFraction > 0.0 && chargedEmEnergyFraction < 0.99 && neutralHadronEnergyFraction < 0.99 && neutralEmEnergyFraction < 0.99')
  process.cleanPatJetsPF.checkOverlaps = cms.PSet(    muons = cms.PSet(src = cms.InputTag("mySelectedPatMuons"),deltaR = cms.double(0.4),
        pairCut = cms.string(''),
        checkRecoComponents = cms.bool(False),
        algorithm = cms.string('byDeltaR'),
        preselection = cms.string(''),
        requireNoOverlaps = cms.bool(True)),
 	electrons = cms.PSet(src = cms.InputTag("mySelectedPatElectrons"),deltaR = cms.double(0.4),
        pairCut = cms.string(''),
        checkRecoComponents = cms.bool(False),
        algorithm = cms.string('byDeltaR'),
        preselection = cms.string(''),
        requireNoOverlaps = cms.bool(True)
    ))
 
  process.mySelectedPatMuons = cms.EDFilter("PATMuonSelector", src = cms.InputTag("patMuonsPF"),
    cut = cms.string('isTrackerMuon && isGlobalMuon && globalTrack.normalizedChi2 < 10. && innerTrack.numberOfValidHits > 10 && globalTrack.hitPattern.numberOfValidMuonHits > 0 && abs(eta) < 2.4 && pt > 20. && abs(dB) < 0.02 && (neutralHadronIso + chargedHadronIso + photonIso)/pt < 0.20') )
  process.mySelectedPatMuons2p1 =cms.EDFilter("PATMuonSelector", src = cms.InputTag("mySelectedPatMuons"), cut = cms.string('abs(eta) < 2.1' )  )
  pPF += process.mySelectedPatMuons; pPF += process.mySelectedPatMuons2p1 
  process.simpleCutBasedElectronID = cms.EDProducer("EleIdCutBasedExtProducer",
    src = cms.InputTag("gsfElectrons"),
    reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
    reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
    verticesCollection = cms.InputTag("offlineBeamSpot"),
    dataMagneticFieldSetUp = cms.bool(False),
    dcsTag = cms.InputTag("scalersRawToDigi"),                                          
    algorithm = cms.string('eIDCB'),
    electronIDType  = cms.string('robust'),
    electronQuality = cms.string('test'),
    electronVersion = cms.string('V04'),
    #### Selections with Relative Isolation                                          
    robust95relIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(5.0e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 1.5e-01, 
                                 2.0e+00, 1.2e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
           endcap =  cms.vdouble(7.0e-02, 3.0e-02, 7.0e-01, 1.0e-02, -1, -1, 9999., 9999., 9999., 9999., 9999., 8.0e-02, 
                                 6.0e-02, 5.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
    ),
    robust90relIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(1.2e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 1.2e-01, 
                                 9.0e-02, 1.0e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(5.0e-02, 3.0e-02, 7.0e-01, 9.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 5.0e-02, 
                                 6.0e-02, 3.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
    ),
    robust85relIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 6.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9.0e-02, 
                                 8.0e-02, 1.0e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 4.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 5.0e-02, 
                                 5.0e-02, 2.5e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
    ),
    robust80relIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9.0e-02, 
                                 7.0e-02, 1.0e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 3.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 4.0e-02, 
                                 5.0e-02, 2.5e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
    ),
    # 70% point modified with restricting cuts to physical values                                                                                    
    robust70relIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(2.5e-02, 1.0e-02, 3.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 5.0e-02, 
                                 6.0e-02, 3.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 2.5e-02, 
                                 2.5e-02, 2.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
    ),
    # 60% point modified with restricting cuts to physical values                                                                                    
    robust60relIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(2.5e-02, 1.0e-02, 2.5e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 4.0e-02, 
                                 4.0e-02, 3.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 2.5e-02, 
                                 2.0e-02, 2.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
    ),
    #### Selections with Combined Isolation

    robust95cIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(5.0e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 1.5e-01, 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
           endcap =  cms.vdouble(7.0e-02, 3.0e-02, 7.0e-01, 1.0e-02, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 1.0e-01, 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
    ),
    robust90cIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(1.2e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 1.0e-01, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(5.0e-02, 3.0e-02, 7.0e-01, 9.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 7.0e-02, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
    ),
    robust85cIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 6.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 9.0e-02, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 4.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 6.0e-02, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
    ),
    robust80cIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 7.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 3.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 6.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
    ),
    # 70% point modified with restricting cuts to physical values                                          
    robust70cIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(2.5e-02, 1.0e-02, 3.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 4.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 3.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
    ),
    # 60% point modified with restricting cuts to physical values
    robust60cIsoEleIDCutsV04 = cms.PSet(
           barrel =  cms.vdouble(2.5e-02, 1.0e-02, 2.5e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 3.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
           endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                                 9999., 9999., 9999., 9999., 9999., 2.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
    ),

  )
  process.simpleEleId90cIso = process.simpleCutBasedElectronID.clone()
  process.simpleEleId90cIso.electronQuality = '90cIso'
  process.pfIsolatedElectronsPF.isolationCut = 99
  process.pfPileUpIsoPF.Vertices = cms.InputTag("goodOfflinePrimaryVertices")
  process.elPFIsoValueGamma03PFIdPF.deposits[0].vetos = cms.vstring('Threshold(0.5)')
  process.elPFIsoValueNeutral03PFIdPF.deposits[0].vetos = cms.vstring('Threshold(0.5)')
  pPF.replace(process.patElectronsPF,process.simpleEleId90cIso * process.patElectronsPF) #pPF += process.simpleEleId90cIso
  process.patElectronsPF.electronIDSources.simpleEleId90cIso = cms.InputTag("simpleEleId90cIso")
  process.patElectronsPF.isolationValues = cms.PSet( pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFIdPF"),pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFIdPF"),pfPhotons = cms.InputTag("elPFIsoValueGamma03PFIdPF"))
  process.AddAdditionalElecConvInfoProducer = cms.EDProducer("AddAdditionalElecConvInfoProducer",eleSrc = cms.InputTag("patElectronsPF"));pPF +=process.AddAdditionalElecConvInfoProducer
  process.myIntermediateElectrons = cms.EDProducer("PATElectronCleaner", src = cms.InputTag("AddAdditionalElecConvInfoProducer"),
      preselection = cms.string(''),# preselection (any string-based cut for pat::Muon)
      checkOverlaps = cms.PSet(# overlap checking configurables
          muonsTrkOrGl = cms.PSet(
             src       = cms.InputTag("patMuonsPF"),
             algorithm = cms.string("byDeltaR"),
             preselection        = cms.string("isTrackerMuon || isGlobalMuon"),  # don't preselect the muons
             deltaR              = cms.double(0.1),
             checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
             pairCut             = cms.string(''),
             requireNoOverlaps   = cms.bool(False), # overlaps don't cause the electron to be discared
          )
      ),
      finalCut = cms.string(''),# finalCut (any string-based cut for pat::Muon)
    );pPF += process.myIntermediateElectrons 
  process.mySelectedPatElectrons = cms.EDFilter("PATElectronSelector", src = cms.InputTag("myIntermediateElectrons"),
		  cut = cms.string('pt > 20. && abs(eta) < 2.5 && gsfTrack.trackerExpectedHitsInner.numberOfLostHits < 2 && !(abs(userFloat("deltaCotTheta")) < 0.02 && abs(userFloat("deltaDistance")) < 0.02 )  && test_bit(electronID("simpleEleId90cIso"), 0) && (neutralHadronIso + chargedHadronIso + photonIso)/pt < 0.17 && abs(dB) < 0.04 && ecalDrivenSeed && !hasOverlaps("muonsTrkOrGl")')#&& gsfTrack->trackerExpectedHitsInner().numberOfLostHits() < 2 &&test_bit(electronID("simpleEleId90cIso"), 0)')
  )
  pPF += process.mySelectedPatElectrons; pPF += process.cleanPatJetsPF
  process.addBTagWeights = cms.EDProducer("AddMyBTagWeights",jetSrc = cms.InputTag("cleanPatJetsPF")); pPF += process.addBTagWeights
  ## pileupWeight
  process.addPileupInfo = cms.EDProducer("AddPileUpWeightsProducer",
                                  vertexSrc = cms.InputTag("offlinePrimaryVertices"),
  pileupFile1 = cms.string("$CMSSW_BASE/src/CMSSW_MyProducers/AddPileUpWeightsProducer/input/JeremyFWK_PU3DMC.root"),
  pileupFile2 = cms.string("$CMSSW_BASE/src/CMSSW_MyProducers/AddPileUpWeightsProducer/input/JeremyFWK_dataPUhisto_2011AB_73.5mb_pixelLumi_diffBinning_bin25.root"),
  PUHistname1 = cms.string("histoMCPU"),
  PUHistname2 = cms.string("pileup")
)
  pPF +=process.addPileupInfo
  from PhysicsTools.PatAlgos.tools.pfTools import *
  #adaptPFTaus( process, tauType='hpsPFTau', postfix=postfix )
  debugIt = True
  if debugIt:
   process.TFileService=cms.Service("TFileService",fileName=cms.string('patRefSel_diLep_cfg_debughistos.root'))
   candPtHistogram = cms.PSet(min = cms.untracked.double(0), max = cms.untracked.double(400), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Pt'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('pt'))
   candEtaHistogram = cms.PSet(min = cms.untracked.double(-5), max = cms.untracked.double(5), nbins =  cms.untracked.int32 (200), name = cms.untracked.string('Eta'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string('eta'))
  # DI Muon Signal 
  if executeDiMuonPath:
    diMuon_cfg.doDiMuonPath(process,pPF,True)
  #DI Electron Signal
  #executeDiElectronPath = True
  if executeDiElectronPath:
    ## my electron selection
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
  # Di EMu Signal
  #executeDiElectronMuonPath = True
  if executeDiElectronMuonPath: 
    ##DiElectronMuon
    process.myDiElectronMuonPath = cms.Path(pPF._seq);localPath = process.myDiElectronMuonPath
    process.myMuonElectronTriggerCheck = cms.EDFilter("TriggerResultsFilter",l1tIgnoreMask = cms.bool(False),l1tResults = cms.InputTag(""),l1techIgnorePrescales = cms.bool(False),    hltResults = cms.InputTag("TriggerResults","","HLT"),  triggerConditions = cms.vstring(MuonElectronTriggers),throw = cms.bool(False), daqPartitions = cms.uint32(1)); localPath += process.myMuonElectronTriggerCheck;#analyzeColl("patElectronsPF",localPath,process,"diEMuTriggerOK");analyzeColl("mySelectedPatMuons2p1",localPath,process,"Muon2p1")
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
  ## pPF configuration continues ...
#
if options.outputFile != str('output.root'):
 print "the outputfile ",options.outputFile
 process.out.fileName = options.outputFile
process.out.outputCommands = cms.untracked.vstring('keep *_*_*_'+process.name_(),'keep  *_addPileupInfo_*_*', 'keep *_generator_*_*','keep *_addBTagWeights_*_*','keep *_addPileupInfo_*_*' )

# simple production
process.simpleProd = cms.Path()
process.addMyPileupInfo = cms.EDProducer("AddPileUpWeightsProducer", vertexSrc = cms.InputTag("offlinePrimaryVertices"),
   pileupFile1 = cms.string("$CMSSW_BASE/src/CMSSW_MyProducers/AddPileUpWeightsProducer/input/JeremyFWK_PU3DMC.root"),
   pileupFile2 = cms.string("$CMSSW_BASE/src/CMSSW_MyProducers/AddPileUpWeightsProducer/input/JeremyFWK_dataPUhisto_2011AB_73.5mb_pixelLumi_diffBinning_bin25.root"),
   PUHistname1 = cms.string("histoMCPU"), PUHistname2 = cms.string("pileup")); process.simpleProd += process.addMyPileupInfo
process.MessageLogger.debugModules.extend(['addMyPileupInfo','addPileupInfo'])
process.MessageLogger.destinations.append('myDebugFile')
process.MessageLogger.myDebugFile = cms.untracked.PSet(threshold = cms.untracked.string('INFO'),filename = cms.untracked.string('patRefSel_diLep_cfg_myDebugFile.log'))
#process.addMyBTagWeights = cms.EDProducer("AddMyBTagWeights"); process.simpleProd += process.addMyBTagWeights
process.out.SelectEvents.SelectEvents.append( 'simpleProd' )
# Compute the mean pt per unit area (rho) from the
if options.runOnTTbar:
  print "attention using genMC ttbar di lep cut"
  process.myttbarGenEvent10Parts = cms.EDProducer('MyTTbarGenEvent10Parts')
  for pName in process.paths.keys():
    getattr(process,pName).insert(0,process.myttbarGenEvent10Parts)
  process.diLepMcFilter = cms.EDFilter('DiLepMcFilter', ttbarEventTag = cms.untracked.InputTag("myTTbarGenEvent10Parts")    )
  #if options.filterSignal:
  print "tagging di lep signal"
  process.isDiLepPath = cms.Path(process.myttbarGenEvent10Parts*process.diLepMcFilter)
