#!/bin/bash

cmsswVer=CMSSW_5_3_
function testExistance {
   repoName=`echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/'`
   echo "repoName "$repoName
   if [ -d "$repoName" ]; then
     echo "there "$1
   else 
    echo "not"
   fi
}
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
#export SCRAM_ARCH=slc5_amd64_gcc434
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
########### checkouts
cd $CMSSW_BASE/src
git cms-addpkg PhysicsTools/Utilities
git cms-addpkg PhysicsTools/PatUtils
git cms-addpkg DataFormats/PatCandidates
git cms-addpkg RecoTauTag/RecoTau
git cms-addpkg PhysicsTools/PatAlgos
git cms-addpkg AnalysisDataFormats/TopObjects
git cms-addpkg CommonTools/ParticleFlow
git cms-addpkg RecoTauTag/TauTagTools
git cms-addpkg TopQuarkAnalysis/TopJetCombination

replaced="PhysicsTools/PatUtils DataFormats/PatCandidates RecoTauTag/RecoTau PhysicsTools/PatAlgos AnalysisDataFormats/TopObjects TopQuarkAnalysis/TopJetCombination RecoTauTag/TauTagTools CommonTools/ParticleFlow"
cd $CMSSW_BASE/src
git clone git@github.com:fhoehle/OldCMSSWPackages.git
for dir in $(ls OldCMSSWPackages/); do 
  if [ -d "$dir" ]; then
    for s in $(ls OldCMSSWPackages/$dir); do
      if [ "$dir/$s" == "RecoLuminosity/LumiDB" ]; then
        echo "github based version should be used git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git $CMSSW_BASE/src/RecoLuminosity/LumiDB and git checkout V04-02-10"
        continue
      fi
      if [[ $replaced =~ "$dir/$s" ]]; then 
	echo "  $dir/$s was replaced"
        continue
      fi
      if [ -d "$dir/$s" ]; then
        echo "fatal $s already there"
        echo "diff $PWD/OldCMSSWPackages/$dir/$s $PWD/$dir/$s"
        exit 1
      fi
      cp -r OldCMSSWPackages/$dir/$s $dir/
    done
  else
    if [ "$dir" == "RecoLuminosity" ]; then
      rsync -a --exclude="RecoLuminosity/LumiDB" OldCMSSWPackages/$dir . 
    else
      cp -r OldCMSSWPackages/$dir $dir;
    fi
  fi
done  
#####
pkgs=(
  "CMSSW_MyAnalyzers src/" #V00-01"
  "CMSSW_MyProducers src/"
  "CMSSW_MyDataFormats src/"
  "CMSSW_MyFilters src/"
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
