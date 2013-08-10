#!/bin/bash

cmsswVer=CMSSW_4_2_8_patch7
function getGitPackage {
echo "getting "$1
if [ -d "$1" ]; then
  cd $1
  git fetch
else
  git clone git@github.com:fhoehle/$1.git
  cd $1
fi

}
####
echo "Installing My FWK "
#
export SCRAM_ARCH=slc5_amd64_gcc434
if [ -z "$CMSSW_BASE" ]; then
 if [[ "$PWD" =~ "$cmsswVer" ]]; then
   echo "you forgot cmsenv"
 else
  echo "creating "$cmsswVer
  scramv1 project CMSSW $cmsswVer # this is cmsrel 
  cd $cmsswVer
 fi
else 
 cd $CMSSW_BASE
fi
eval `scramv1 runtime -sh` # this is cmsenv
cd src
# check kerberos
klist -s
rc=$?
if [[ $rc != 0 ]] ; then
    echo "kerberos credentials missing"
    klist -c
    exit $rc
fi
########### checkouts
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
#####
pkgs=(
  "CMSSW_MyAnalyzers src/ V00-01"
  "CMSSW_MyProducers src/ V00-03"
  "CMSSW_MyDataFormats src/ V00-01"
  "CMSSW_MyFilters src/  V00-01"
)
# install my packages
for idx in ${!pkgs[*]}; do
  cd $CMSSW_BASE/`echo ${pkgs[$idx]} | awk '{print $2}'`
  getGitPackage `echo ${pkgs[$idx]} | awk '{print $1}'`
  git checkout `echo ${pkgs[$idx]} | awk '{print $3}'`
  if  [ "X`echo ${pkgs[$idx]} | awk '{print $4}'`" != "X" ]; then
    echo "calling additional command "`echo ${pkgs[$idx]} | awk '{print $4}'`
    eval `echo ${pkgs[$idx]} | awk '{print $4}'`
  fi
  cd $CMSSW_BASE
done

scram b -j 5
