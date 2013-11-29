#
# This file contains the Top PAG reference selection work-flow for mu + jets analysis.
# as defined in
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopLeptonPlusJetsRefSel_mu#Selection_Version_SelV4_valid_fr
#
def createCut(cuts):
  return ''.join([c['cut'] if i == 0 else " && "+c['cut'] for i,c in enumerate(cuts) ])
def getTriggerForRunRange(minRun,maxRun,triggerRunRanges):
  minRunTrig = None; maxRunTrig = None
  for trig,trigRange in triggerRunRanges.iteritems():
    print trig," ",trigRange," ",minRun," ",maxRun
    if minRun >= trigRange[0] and minRun <= trigRange[1]:
      minRunTrig = trig if not minRunTrig else minRunTrig+" OR "+trig
    if maxRun >= trigRange[0] and maxRun <= trigRange[1]:
      maxRunTrig = trig if not maxRunTrig else maxRunTrig+" OR "+trig
    print 'minRunTrig' ,minRunTrig,' maxRunTrig ',maxRunTrig
  return minRunTrig if minRunTrig == maxRunTrig else None
triggersUsedForAnalysis = {
  'diMuon':{}
  ,'diElectron':{}
  ,'electronMuon':{}
}
electronMuonDataUseTriggers = {'HLT_Mu8_Ele17_CaloIdL_v*':[0,167913],'HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v*':[167914,999999],'HLT_Mu17_Ele8_CaloIdL_v*':[0,175972] ,'HLT_Mu17_Ele8_CaloIdT_CaloIsoVL-v*':[175973,999999]}
triggersUsedForAnalysis['electronMuon']['data'] = electronMuonDataUseTriggers; triggersUsedForAnalysis['electronMuon']['mc']='HLT_Mu10_Ele10_CaloIdL_v3 OR HLT_Mu8_Ele17_CaloIdL_v2'
diElectronDataUseTriggers = {'HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v*':[0,170901],'HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v*':[170902,999999]}
triggersUsedForAnalysis['diElectron']['data']=diElectronDataUseTriggers; triggersUsedForAnalysis['diElectron']['mc']="HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v2"
diMuonDataUseTriggers = {'HLT_DoubleMu7_v*':[0,165208],'HLT_Mu13_Mu8_v*':[165209,178419],'HLT_Mu17_Mu8_v* OR HLT_Mu17_TkMu8_v*':[178420,999999]}
triggersUsedForAnalysis['diMuon']['data'] =diMuonDataUseTriggers; triggersUsedForAnalysis['diMuon']['mc']= "HLT_DoubleMu6_v1"

import imp,os,sys,re
executeDiElectronPath = False
diMuon_cfg = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/DiLeptonicSelection/diMuon_cfg.py')
diElectron_cfg = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/DiLeptonicSelection/diElectron_cfg.py')
diEleMuon_cfg = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/DiLeptonicSelection/diEleMuon_cfg.py')
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
options.register('skipEvents',0,VarParsing.multiplicity.singleton,VarParsing.varType.int,'skipEvents')
options.register('runOnTTbar',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'runOnTTbar')
options.register('N1TTbarDiLepBck',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'N1TTbarDiLepBck')
options.register('runOnData',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'runOnData')
options.register('runRange','',VarParsing.multiplicity.singleton,VarParsing.varType.string,'runRange used for running on data to estimate trigger')
options.register('runOnlyDiMuon',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'run only di muon path')
options.register('runOnlyDiElectron',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'run only di electron path')
options.register('runOnlyElectronMuon',False,VarParsing.multiplicity.singleton,VarParsing.varType.bool,'run only electron muon path')
print "args ",sys.argv
options.parseArguments()
print "these options where given",options.__dict__['_setDuringParsing']
if options.runOnlyDiMuon:
  executeDiElectronMuonPath = False
  executeDiElectronPath = False
  executeDiMuonPath = True
if options.runOnlyDiElectron:
  executeDiElectronPath = True
  executeDiMuonPath = False
  executeDiElectronMuonPath = False
if options.runOnlyElectronMuon:
  executeDiElectronMuonPath = True
  executeDiMuonPath = False  
  executeDiElectronPath = False
if sum([options.runOnlyDiMuon,options.runOnlyDiElectron,options.runOnlyElectronMuon]) > 1:
  sys.exit('only one path can be the only')

reRunRange = re.match('^([0-9]+)-([0-9]+)$',options.runRange)
print "options.runRange",options.runRange
minRun = None ; maxRun = None
if options.runOnData: 
  if not reRunRange or len(reRunRange.groups()) != 2 :
    sys.exit('runRange wrong should be 123-234')
  minRun=int(reRunRange.group(1));maxRun=int(reRunRange.group(2))
import FWCore.ParameterSet.Config as cms
def analyzeColl(coll,path,process,prefix=''):
 newmod = cms.EDAnalyzer("MyCandPrintAnalyzer", src = cms.InputTag(coll), prefix = cms.string(prefix+"test"+coll),
    quantity = cms.vstring('px', 'py', 'pz', 'energy', 'pt', 'eta', 'phi'))
 setattr(process,prefix+"test"+coll,newmod)
 path += getattr(process,prefix+"test"+coll)

######################
process = cms.Process( 'PAT' )
#######
#dump cmsRun parameters
print "this is cmsRun input: ",sys.argv

### Data or MC?
runOnMC = True

### Reference selection

import TopQuarkAnalysis.Configuration.patRefSel_refMuJets as patRefSel_refMuJets 
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
fwkReportEvery = 100

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
#process.source.fileNames.append("/store/mc/Fall11/TT_TuneZ2_7TeV-mcatnlo/AODSIM/PU_S6_START42_V14B-v1/0001/FED956DF-7F2A-E111-8124-002618943958.root")
process.source.skipEvents = cms.untracked.uint32(options.skipEvents)
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
import PhysicsTools.PatAlgos.tools.coreTools as PhysPatAlgCoreTools

### Check JECs

# JEC set
jecSetPF    = patRefSel_refMuJets.jecSetBase + pfSuffix + 'chs' 

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
if options.runOnData:
  from PhysicsTools.PatAlgos.tools.coreTools import runOnData
  runOnData(process, names = [ 'All' ])


import PhysicsTools.PatAlgos.tools.pfTools as pfTools
pfTools.usePF2PAT( process
         , runPF2PAT      = True #runPF2PAT
         , runOnMC        = runOnMC
         , jetAlgo        = patRefSel_refMuJets.jetAlgo
         , postfix        = postfix
         , jetCorrections = ( jecSetPF
                            , jecLevels
                            )
         )
pfTools.adaptPFTaus( process, tauType='hpsPFTau', postfix=postfix )
pfTools.applyPostfix( process, 'pfNoPileUp'  , postfix ).enable = usePFnoPU
pfTools.applyPostfix( process, 'pfNoMuon'    , postfix ).enable = useNoMuon
pfTools.applyPostfix( process, 'pfNoElectron', postfix ).enable = useNoElectron
pfTools.applyPostfix( process, 'pfNoJet'     , postfix ).enable = useNoJet
pfTools.applyPostfix( process, 'pfNoTau'     , postfix ).enable = useNoTau
pfTools.applyPostfix( process, 'pfPileUp', postfix ).Vertices = cms.InputTag( patRefSel_refMuJets.pfVertices )
if useL1FastJet:
  pfTools.applyPostfix( process, 'pfPileUp'   , postfix ).checkClosestZVertex = False
  pfTools.applyPostfix( process, 'pfPileUpIso', postfix ).checkClosestZVertex = usePfIsoLessCHS
  pfTools.applyPostfix( process, 'pfJets', postfix ).doAreaFastjet = True
  pfTools.applyPostfix( process, 'pfJets', postfix ).doRhoFastjet  = False
pfTools.applyPostfix( process, 'pfMuonsFromVertex'    , postfix ).vertices = cms.InputTag( patRefSel_refMuJets.pfVertices )
pfTools.applyPostfix( process, 'pfMuonsFromVertex'    , postfix ).d0Cut    = patRefSel_refMuJets.pfD0Cut
pfTools.applyPostfix( process, 'pfMuonsFromVertex'    , postfix ).dzCut    = patRefSel_refMuJets.pfDzCut
pfTools.applyPostfix( process, 'pfSelectedMuons'      , postfix ).cut = patRefSel_refMuJets.pfMuonSelectionCut
pfTools.applyPostfix( process, 'pfIsolatedMuons'      , postfix ).isolationCut = patRefSel_refMuJets.pfMuonCombIsoCut
pfTools.applyPostfix( process, 'pfElectronsFromVertex'    , postfix ).vertices = cms.InputTag( patRefSel_refMuJets.pfVertices )
pfTools.applyPostfix( process, 'pfElectronsFromVertex'    , postfix ).d0Cut    = patRefSel_refMuJets.pfD0Cut
pfTools.applyPostfix( process, 'pfElectronsFromVertex'    , postfix ).dzCut    = patRefSel_refMuJets.pfDzCut
pfTools.applyPostfix( process, 'pfSelectedElectrons'      , postfix ).cut = patRefSel_refMuJets.pfElectronSelectionCut
pfTools.applyPostfix( process, 'pfIsolatedElectrons'      , postfix ).isolationCut = patRefSel_refMuJets.pfElectronCombIsoCut
pfTools.applyPostfix( process, 'patElectrons', postfix ).pvSrc = cms.InputTag( patRefSel_refMuJets.pfVertices )
pfTools.applyPostfix( process, 'patMuons'    , postfix ).pvSrc = cms.InputTag( patRefSel_refMuJets.pfVertices )

import TopQuarkAnalysis.Configuration.patRefSel_refMuJets_cfi as patRefSel_refMuJets_cfi

# remove MC matching, object cleaning, objects etc.
## remove MCMatching if run on Data
if options.runOnData:
  from PhysicsTools.PatAlgos.tools.coreTools import runOnData
  runOnData(process, names = [ 'PFAll' ],postfix =postfix)
  print "removeMatching"
if not runOnMC:
  runOnData( process
           , names = [ 'PFAll' ]
           , postfix = postfix
           )
PhysPatAlgCoreTools.removeSpecificPATObjects( process
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

goodPatJetsAddPFLabel = 'goodPatJets' + patRefSel_refMuJets.jetAlgo + pfSuffix


### Muons

intermediatePatMuonsPF = patRefSel_refMuJets_cfi.intermediatePatMuons.clone( src = cms.InputTag( 'selectedPatMuons' + postfix ) )
setattr( process, 'intermediatePatMuons' + postfix, intermediatePatMuonsPF )

loosePatMuonsPF = patRefSel_refMuJets_cfi.loosePatMuons.clone( src = cms.InputTag( 'intermediatePatMuons' + postfix ) )
setattr( process, 'loosePatMuons' + postfix, loosePatMuonsPF )
getattr( process, 'loosePatMuons' + postfix ).checkOverlaps.jets.src = cms.InputTag( 'goodPatJets' + postfix )

step1aPF = patRefSel_refMuJets_cfi.step1a.clone( src = cms.InputTag( 'loosePatMuons' + postfix ) )
setattr( process, 'step1a' + postfix, step1aPF )

tightPatMuonsPF = patRefSel_refMuJets_cfi.tightPatMuons.clone( src = cms.InputTag( 'loosePatMuons' + postfix ) )
setattr( process, 'tightPatMuons' + postfix, tightPatMuonsPF )

step1bPF = patRefSel_refMuJets_cfi.step1b.clone( src = cms.InputTag( 'tightPatMuons' + postfix ) )
setattr( process, 'step1b' + postfix, step1bPF )

step2PF = patRefSel_refMuJets_cfi.step2.clone( src = cms.InputTag( 'selectedPatMuons' + postfix ) )
setattr( process, 'step2' + postfix, step2PF )

### Jets

pfTools.applyPostfix( process, 'patJetCorrFactors', postfix ).primaryVertices = cms.InputTag( patRefSel_refMuJets.pfVertices )
setattr( process, 'kt6PFJets' + postfix, patRefSel_refMuJets_cfi.kt6PFJets )
getattr( process, 'patPF2PATSequence' + postfix).replace( getattr( process, 'patJetCorrFactors' + postfix )
                                                        , getattr( process, 'kt6PFJets' + postfix ) * getattr( process, 'patJetCorrFactors' + postfix )
                                                        )
if useL1FastJet:
  pfTools.applyPostfix( process, 'patJetCorrFactors', postfix ).rho = cms.InputTag( 'kt6PFJets' + postfix, 'rho' )
process.out.outputCommands.append( 'keep double_kt6PFJets' + postfix + '_*_' + process.name_() )

goodPatJetsPF = patRefSel_refMuJets_cfi.goodPatJets.clone( src = cms.InputTag( 'selectedPatJets' + postfix ) )
setattr( process, 'goodPatJets' + postfix, goodPatJetsPF )
getattr( process, 'goodPatJets' + postfix ).checkOverlaps.muons.src = cms.InputTag( 'intermediatePatMuons' + postfix )

step4aPF = patRefSel_refMuJets_cfi.step4a.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
setattr( process, 'step4a' + postfix, step4aPF )
step4bPF = patRefSel_refMuJets_cfi.step4b.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
setattr( process, 'step4b' + postfix, step4bPF )
step4cPF = patRefSel_refMuJets_cfi.step4c.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
setattr( process, 'step4c' + postfix, step4cPF )
step5PF = patRefSel_refMuJets_cfi.step5.clone( src = cms.InputTag( 'goodPatJets' + postfix ) )
setattr( process, 'step5'  + postfix, step5PF  )

### Electrons

step3PF = patRefSel_refMuJets_cfi.step3.clone( src = cms.InputTag( 'selectedPatElectrons' + postfix ) )
setattr( process, 'step3' + postfix, step3PF )

process.out.outputCommands.append( 'keep *_intermediatePatMuons*_*_*' )
process.out.outputCommands.append( 'keep *_loosePatMuons*_*_*' )
process.out.outputCommands.append( 'keep *_tightPatMuons*_*_*' )
process.out.outputCommands.append( 'keep *_goodPatJets*_*_*' )


###
### Selection configuration
###


pfTools.applyPostfix( process, 'patMuons', postfix ).usePV      = patRefSel_refMuJets.muonsUsePV
pfTools.applyPostfix( process, 'patMuons', postfix ).embedTrack = patRefSel_refMuJets.muonEmbedTrack

pfTools.applyPostfix( process, 'selectedPatMuons', postfix ).cut = patRefSel_refMuJets.muonCutPF

getattr( process, 'intermediatePatMuons' + postfix ).preselection = patRefSel_refMuJets.looseMuonCutPF

getattr( process, 'loosePatMuons' + postfix ).preselection              = patRefSel_refMuJets.looseMuonCutPF
getattr( process, 'loosePatMuons' + postfix ).checkOverlaps.jets.deltaR = patRefSel_refMuJets.muonJetsDR

getattr( process, 'tightPatMuons' + postfix ).preselection = patRefSel_refMuJets.tightMuonCutPF

### Jets

getattr( process, 'goodPatJets' + postfix ).preselection               = patRefSel_refMuJets.jetCutPF
getattr( process, 'goodPatJets' + postfix ).checkOverlaps.muons.deltaR = patRefSel_refMuJets.jetMuonsDRPF

### Electrons

pfTools.applyPostfix( process, 'patElectrons', postfix ).electronIDSources = patRefSel_refMuJets_cfi.electronIDSources

pfTools.applyPostfix( process, 'selectedPatElectrons', postfix ).cut = patRefSel_refMuJets.electronCutPF


###
### Trigger matching
###


if runOnMC:
  triggerObjectSelection = patRefSel_refMuJets.triggerObjectSelectionMC
else:
  triggerObjectSelection = patRefSel_refMuJets.triggerObjectSelectionData
### Trigger matching configuration
from PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cfi import patTrigger
from TopQuarkAnalysis.Configuration.patRefSel_triggerMatching_cfi import patMuonTriggerMatch
if not options.runOnData:
  import PhysicsTools.PatAlgos.tools.trigTools as trigTools
  triggerProducerPF = patTrigger.clone()
  setattr( process, 'patTrigger' + postfix, triggerProducerPF )
  triggerMatchPF = patMuonTriggerMatch.clone( matchedCuts = triggerObjectSelection )
  setattr( process, 'triggerMatch' + postfix, triggerMatchPF )
  trigTools.switchOnTriggerMatchEmbedding( process
                               , triggerProducer = 'patTrigger' + postfix
                               , triggerMatchers = [ 'triggerMatch' + postfix ]
                               , sequence        = 'patPF2PATSequence' + postfix
                               , postfix         = postfix
                               )
  trigTools.removeCleaningFromTriggerMatching( process
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
#patAddOnSequence = cms.Sequence(
#  getattr( process, 'intermediatePatMuons' + postfix )
#* getattr( process, 'goodPatJets' + postfix )
#* getattr( process, 'loosePatMuons' + postfix )
#* getattr( process, 'tightPatMuons' + postfix )
#)
#setattr( process, 'patAddOnSequence' + postfix, patAddOnSequence )

# The paths
pPF = cms.Path()
pPF += process.goodOfflinePrimaryVertices
pPF += process.eidCiCSequence
pPF += getattr( process, 'patPF2PATSequence' + postfix )
#pPF += getattr( process, 'patAddOnSequence' + postfix )
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
## adding collections
myElectronCutBasedId_cfi = imp.load_source('module.name', os.getenv('CMSSW_BASE')+'/DiLeptonicSelection/myElectronCutBasedId_cfi.py')
process.simpleEleId90cIso = myElectronCutBasedId_cfi.simpleEleId90cIso
process.pfIsolatedElectronsPF.isolationCut = 99
process.pfPileUpIsoPF.Vertices = cms.InputTag("goodOfflinePrimaryVertices")
process.elPFIsoValueGamma03PFIdPF.deposits[0].vetos = cms.vstring('Threshold(0.5)')
process.elPFIsoValueNeutral03PFIdPF.deposits[0].vetos = cms.vstring('Threshold(0.5)')
pPF.replace(process.patElectronsPF,process.simpleEleId90cIso * process.patElectronsPF) #pPF += process.simpleEleId90cIso
process.patElectronsPF.electronIDSources.simpleEleId90cIso = cms.InputTag("simpleEleId90cIso")
process.patElectronsPF.isolationValues = cms.PSet( pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFIdPF"),pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFIdPF"),pfPhotons = cms.InputTag("elPFIsoValueGamma03PFIdPF"))
process.AddAdditionalElecConvInfoProducer = cms.EDProducer("AddAdditionalElecConvInfoProducer",eleSrc = cms.InputTag("patElectronsPF"));pPF +=process.AddAdditionalElecConvInfoProducer
## object definition
boolHist = cms.PSet( min = cms.untracked.double(-0.5), max = cms.untracked.double(2.5), nbins = cms.untracked.int32(3))
chi2Hist = cms.PSet( min = cms.untracked.double(-0.5), max = cms.untracked.double(100.5), nbins = cms.untracked.int32(202))
etaHist = cms.PSet( min = cms.untracked.double(-5), max = cms.untracked.double(5), nbins = cms.untracked.int32(200))
ptHist = cms.PSet( min = cms.untracked.double(0), max = cms.untracked.double(200), nbins = cms.untracked.int32(200))
relIsoHist = cms.PSet( min = cms.untracked.double(0), max = cms.untracked.double(2), nbins = cms.untracked.int32(1000))
dbHist = cms.PSet( min = cms.untracked.double(0), max = cms.untracked.double(1), nbins = cms.untracked.int32(200))
#, name = cms.untracked.string('JetPt'), description  = cms.untracked.string(''), plotquantity = cms.untracked.string(   'pt'))
#muons
myMuonCuts = {"cuts":[{'label':'isTrackerMuon','cut':'isTrackerMuon',"hist":boolHist},{'label':'isGlobalMuon','cut':'isGlobalMuon',"hist":boolHist,"not":['globalTrackHitPatValHits','globalTrackNormalizedChi2','globalTrackHitPatValHits']},{'label':'globalTrackNormalizedChi2','cut':'globalTrack.normalizedChi2 < 10.','hist':chi2Hist},{'label':'innerTrackValHits','cut':'innerTrack.numberOfValidHits > 10','hist':chi2Hist},{'label':'globalTrackHitPatValHits','cut':'globalTrack.hitPattern.numberOfValidMuonHits > 0','hist':chi2Hist},{'label':'absEta','cut':'abs(eta) < 2.4','hist':etaHist},{'label':'pt','cut':'pt > 20.','hist':ptHist},{'label':'dB','cut':'abs(dB) < 0.02','hist':dbHist},{'label':'relIso','cut':'(neutralHadronIso + chargedHadronIso + photonIso)/pt < 0.20','hist':relIsoHist}],"coll":"patMuonsPF"}
finalCut=createCut(myMuonCuts["cuts"])
doMuonN1 = True #False
import copy,re
if doMuonN1:
  process.pPFN1 = cms.Path(pPF._seq)
  cutsList =  myMuonCuts["cuts"]
  for i,cut in enumerate(cutsList):
    pPFN1Tmp = cms.Path(pPF._seq)
    print "contructiong for ",cut,"  ",i
    tmpCutList = cutsList[:i]+cutsList[i+1:]
    if cut.has_key("not"):
      tmpCutList = [c for c in cutsList[:i]+cutsList[i+1:] if not c["label"] in cut["not"]] 
    tmpCutList=createCut(tmpCutList)
    print tmpCutList
    tmpMuonN1Coll = cms.EDFilter("PATMuonSelector", src = cms.InputTag(myMuonCuts["coll"]),cut = cms.string(tmpCutList)  )
    tmpMuonN1CollName = tmpMuonN1Coll.src.value() +'NM1'+cut["label"]
    setattr(process,tmpMuonN1CollName,tmpMuonN1Coll); pPFN1Tmp += getattr(process,tmpMuonN1CollName)
    tmpMuonN1CollFilter = countPatMuons = cms.EDFilter("PATCandViewCountFilter", minNumber = cms.uint32(2),maxNumber = cms.uint32(999999), src = cms.InputTag(tmpMuonN1CollName)); setattr(process,tmpMuonN1CollName+"CountFilter",tmpMuonN1CollFilter);  pPFN1Tmp += getattr(process,tmpMuonN1CollName+"CountFilter")
    reCut = re.match('^\ *([^<>=]*)\ *[<>=]*[=]*\ *[^<>=]*$',cut["cut"]).group(1)
    print reCut
    tmpHist = copy.deepcopy(cut["hist"]);setattr(tmpHist,'name',cms.untracked.string(cut["label"]));setattr(tmpHist,'description',cms.untracked.string(cut["label"]));setattr(tmpHist,'plotquantity',cms.untracked.string(reCut));tmpHist.lazyParsing = cms.untracked.bool(True)
    tmpMuonN1Histo = cms.EDAnalyzer('CandViewHistoAnalyzer', src = cms.InputTag(tmpMuonN1CollName),histograms = cms.VPSet(tmpHist))
    setattr(process, tmpMuonN1CollName+"N1Histo" ,tmpMuonN1Histo); pPFN1Tmp += getattr(process,tmpMuonN1CollName+"N1Histo")
    setattr(process, 'pPFNM1'+cut["label"],pPFN1Tmp)
    
process.mySelectedPatMuons = cms.EDFilter("PATMuonSelector", src = cms.InputTag("patMuonsPF"),
  #cut = cms.string('isTrackerMuon && isGlobalMuon && globalTrack.normalizedChi2 < 10. && innerTrack.numberOfValidHits > 10 && globalTrack.hitPattern.numberOfValidMuonHits > 0 && abs(eta) < 2.4 && pt > 20. && abs(dB) < 0.02 && (neutralHadronIso + chargedHadronIso + photonIso)/pt < 0.20') 
   cut = cms.string(finalCut)
  )
process.mySelectedPatMuons2p1 =cms.EDFilter("PATMuonSelector", src = cms.InputTag("mySelectedPatMuons"), cut = cms.string('abs(eta) < 2.1' )  )
pPF += process.mySelectedPatMuons; pPF += process.mySelectedPatMuons2p1 

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
#
debugIt = True
if debugIt:
 process.TFileService=cms.Service("TFileService",fileName=cms.string('patRefSel_diLep_cfg_debughistos.root'))
# DI Muon Signal 
if executeDiMuonPath:
  diMuontrigger = ""
  triggers=triggersUsedForAnalysis['diMuon']
  if options.runOnData:
    dataTriggers = triggers['data']
    diMuonDataUseTrigger = getTriggerForRunRange(minRun,maxRun,dataTriggers)
    if not diMuonDataUseTrigger:
      sys.exit('not suitable run range given '+';'.join([k+":"+str(r[0])+"-"+str(r[1]) for k,r in dataTriggers.iteritems()])) 
    diMuontrigger=diMuonDataUseTrigger
  else:
    diMuontrigger=triggers['mc']
  myMuonPath = diMuon_cfg.myMuonPath(options.runOnData,diMuontrigger)
  myMuonPath.doDiMuonPath(process,pPF,True)
#DI Electron Signal
#executeDiElectronPath = True
if executeDiElectronPath:
  diElectrontrigger = ""
  triggers=triggersUsedForAnalysis['diElectron']
  if options.runOnData:
    dataTriggers=triggers['data']
    diElectronDataUseTrigger = getTriggerForRunRange(minRun,maxRun,dataTriggers)
    if not diElectronDataUseTrigger:
       sys.exit('not suitable run range given '+';'.join([k+":"+str(r[0])+"-"+str(r[1]) for k,r in idataTriggers.iteritems()]))
    diElectrontrigger = diElectronDataUseTrigger
  else:
    diElectrontrigger = triggers['mc']
  myElectronPath = diElectron_cfg.myElectronPath(options.runOnData,diElectrontrigger)
  myElectronPath.doDiElectronPath(process,pPF,True)
  ## my electron selection
# Di EMu Signal
if executeDiElectronMuonPath: 
  electronMuontrigger = ""
  triggers=triggersUsedForAnalysis['electronMuon']
  if options.runOnData:
    dataTriggers=triggers['data']
    electronMuonDataUseTrigger = getTriggerForRunRange(minRun,maxRun,dataTriggers)
    if not electronMuonDataUseTrigger:
      sys.exit('not suitable run range given '+';'.join([k+":"+str(r[0])+"-"+str(r[1]) for k,r in dataTriggers.iteritems()]))
    electronMuontrigger = electronMuonDataUseTrigger
  else:
    electronMuontrigger = triggers['mc']
  myElectronMuonPath = diEleMuon_cfg.myElectronMuonPath(options.runOnData,electronMuontrigger)
  myElectronMuonPath.doDiEleMuonPath(process,pPF,True)
  ##DiElectronMuon

## pPF configuration continues ...
#
if options.outputFile != str('output.root'):
 print "the outputfile ",options.outputFile
 process.out.fileName = options.outputFile
process.out.outputCommands = cms.untracked.vstring('keep *_*_*_'+process.name_(),'keep  *_addPileupInfo_*_*', 'keep *_generator_*_*','keep *_addBTagWeights_*_*','keep *_addPileupInfo_*_*' )

# simple production
process.simpleProd = cms.Path()
if not options.runOnData:
  process.addMyPileupInfo = cms.EDProducer("AddPileUpWeightsProducer", vertexSrc = cms.InputTag("offlinePrimaryVertices"),
   pileupFile1 = cms.string("$CMSSW_BASE/src/CMSSW_MyProducers/AddPileUpWeightsProducer/data/JeremyFWK_PU3DMC.root"),
   pileupFile2 = cms.string("$CMSSW_BASE/src/CMSSW_MyProducers/AddPileUpWeightsProducer/data/JeremyFWK_dataPUhisto_2011AB_73.5mb_pixelLumi_diffBinning_bin25.root"),
   PUHistname1 = cms.string("histoMCPU"), PUHistname2 = cms.string("pileup")); process.simpleProd += process.addMyPileupInfo
  process.MessageLogger.debugModules.extend(['addMyPileupInfo'])
process.MessageLogger.destinations.append('myDebugFile')
process.MessageLogger.myDebugFile = cms.untracked.PSet(threshold = cms.untracked.string('INFO'),filename = cms.untracked.string('patRefSel_diLep_cfg_myDebugFile.log'))
#process.addMyBTagWeights = cms.EDProducer("AddMyBTagWeights"); process.simpleProd += process.addMyBTagWeights
process.out.SelectEvents.SelectEvents.append( 'simpleProd' )
# Compute the mean pt per unit area (rho) from the
if options.N1TTbarDiLepBck:
  options.runOnTTbar = True
if options.runOnTTbar:
  print "attention using genMC ttbar di lep cut"
  process.myttbarGenEvent10Parts = cms.EDProducer('MyTTbarGenEvent10Parts')
  for pName in process.paths.keys():
    getattr(process,pName).insert(0,process.myttbarGenEvent10Parts)
  process.diLepMcFilter = cms.EDFilter('DiLepMcFilter', ttbarEventTag = cms.untracked.InputTag("myttbarGenEvent10Parts")    )
  #if options.filterSignal:
  print "tagging di lep signal"
  process.isDiLepPath = cms.Path(process.myttbarGenEvent10Parts*process.diLepMcFilter)
  if doMuonN1:
   if options.N1TTbarDiLepBck:
     process.pPFN1.replace(process.myttbarGenEvent10Parts,process.myttbarGenEvent10Parts*~process.diLepMcFilter)
   else:
     process.pPFN1.replace(process.myttbarGenEvent10Parts,process.myttbarGenEvent10Parts*process.diLepMcFilter)
