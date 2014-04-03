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
########### checkouts
cd $CMSSW_BASE/src
git clone git@github.com:fhoehle/OldCMSSWPackages.git
for d in $(ls OldCMSSWPackages/); do ln -s OldCMSSWPackages/$d $d; done
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
