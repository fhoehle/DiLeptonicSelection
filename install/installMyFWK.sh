#!/bin/bash

cmsswVer=CMSSW_4_2_8_patch7


echo "Installing My FWK "
#
export SCRAM_ARCH=slc5_amd64_gcc434
cmsrel $cmsswVer

cd $cmsswVer
cmsenv
cd src
addpkg AnalysisDataFormats/TopObjects         V06-07-09
addpkg TopQuarkAnalysis/Configuration         V06-01-14-04
addpkg TopQuarkAnalysis/Examples              V06-07-10
addpkg TopQuarkAnalysis/TopEventProducers     V06-07-14
addpkg TopQuarkAnalysis/TopEventSelection     V06-07-13
addpkg TopQuarkAnalysis/TopJetCombination     V06-07-10
addpkg TopQuarkAnalysis/TopKinFitter          V06-07-17
addpkg TopQuarkAnalysis/TopObjectResolutions  V06-07-08
addpkg TopQuarkAnalysis/TopTools              V06-07-11
addpkg PhysicsTools/KinFitter                 V00-03-06
scram b -j 5
