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
cd $CMSSW_BASE/src
git cms-addpkg AnalysisDataFormats/TopObjects         
git cms-addpkg DataFormats/PatCandidates       
git cms-addpkg TopQuarkAnalysis/Configuration         
git cms-addpkg TopQuarkAnalysis/Examples              
git cms-addpkg TopQuarkAnalysis/TopEventProducers     
git cms-addpkg TopQuarkAnalysis/TopEventSelection     
git cms-addpkg TopQuarkAnalysis/TopJetCombination     
git cms-addpkg TopQuarkAnalysis/TopKinFitter          
git cms-addpkg TopQuarkAnalysis/TopObjectResolutions  
git cms-addpkg TopQuarkAnalysis/TopTools              
git cms-addpkg PhysicsTools/KinFitter                 
git cms-addpkg RecoTauTag/Configuration               
git cms-addpkg RecoTauTag/RecoTau                     
git cms-addpkg RecoTauTag/TauTagTools                 
git cms-addpkg PhysicsTools/PatAlgos                       
git cms-addpkg PhysicsTools/PatUtils                       
git cms-addpkg PhysicsTools/SelectorUtils                  
git cms-addpkg PhysicsTools/UtilAlgos                 
git cms-addpkg CommonTools/ParticleFlow       
git cms-addpkg PhysicsTools/Utilities                 
#####
pkgs=(
  "CMSSW_MyAnalyzers src/ V00-01"
  "CMSSW_MyProducers src/"
  "CMSSW_MyDataFormats src/ V00-01"
  "CMSSW_MyFilters src/  V00-01"
)
# install my packages
for idx in ${!pkgs[*]}; do
  cd $CMSSW_BASE/`echo ${pkgs[$idx]} | awk '{print $2}'`
  getGitPackage `echo ${pkgs[$idx]} | awk '{print $1}'`
  if [ "X`echo ${pkgs[$idx]} | awk '{print $3}'`" != "X" ]; then
    git checkout `echo ${pkgs[$idx]} | awk '{print $3}'`
  fi
  if  [ "X`echo ${pkgs[$idx]} | awk '{print $4}'`" != "X" ]; then
    echo "calling additional command "`echo ${pkgs[$idx]} | awk '{print $4}'`
    eval `echo ${pkgs[$idx]} | awk '{print $4}'`
  fi
  cd $CMSSW_BASE
done

scram b -j 5
