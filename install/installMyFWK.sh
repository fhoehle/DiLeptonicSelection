#!/bin/bash

cmsswVer=CMSSW_4_2_8_patch7


echo "Installing My FWK "
#
export SCRAM_ARCH=slc5_amd64_gcc434
if [ -z "$CMSSW_BASE" ]; then
 echo "creating "$cmsswVer
 cmsrel $cmsswVer
 cd $cmsswVer
else 
 cd $CMSSW_BASE
fi
cmsenv
cd src
addpkg AnalysisDataFormats/TopObjects         V06-07-09
addpkg DataFormats/PatCandidates                        V06-04-19-05
addpkg TopQuarkAnalysis/Configuration         V06-01-14-04
addpkg TopQuarkAnalysis/Examples              V06-07-10
addpkg TopQuarkAnalysis/TopEventProducers     V06-07-14
addpkg TopQuarkAnalysis/TopEventSelection     V06-07-13
addpkg TopQuarkAnalysis/TopJetCombination     V06-07-10
addpkg TopQuarkAnalysis/TopKinFitter          V06-07-17
addpkg TopQuarkAnalysis/TopObjectResolutions  V06-07-08
addpkg TopQuarkAnalysis/TopTools              V06-07-11
addpkg PhysicsTools/KinFitter                 V00-03-06
addpkg RecoTauTag/Configuration               V01-02-09
addpkg RecoTauTag/RecoTau                     V01-02-07-02  
addpkg RecoTauTag/TauTagTools                 V01-02-00
addpkg PhysicsTools/PatAlgos                            V08-06-58      
addpkg PhysicsTools/PatUtils                            V03-09-18      
addpkg PhysicsTools/SelectorUtils                       V00-03-24      
addpkg PhysicsTools/UtilAlgos                           V08-02-14
addpkg CommonTools/ParticleFlow                         B4_2_X_V00-03-05
addpkg PhysicsTools/Utilities                           V08-03-17
git clone git@github.com:fhoehle/CMSSW_MyAnalyzers.git
git clone git@github.com:fhoehle/CMSSW_MyProducers.git

scram b -j 5
