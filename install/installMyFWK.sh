#!/bin/bash

cmsswVer=CMSSW_4_2_8_patch7
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
git cms-addpkg PhysicsTools/Utilities
cd $CMSSW_BASE/src
git clone git@github.com:fhoehle/OldCMSSWPackages.git
for dir in $(ls OldCMSSWPackages/); do 
  if [ -d "$dir" ]; then
    echo "package $d already there copying subpackages"
    for s in $(ls OldCMSSWPackages/$dir); do
      if [ "$dir/$s" -eq "RecoLuminosity/LumiDB" ]; then
        echo "github based version should be used git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git $CMSSW_BASE/src/RecoLuminosity/LumiDB and git checkout V04-02-10"
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
    if [ "$dir" -eq "RecoLuminosity" ]; then
      rsync -av --exclude='OldCMSSWPackages/RecoLuminosity/LumiDB' OldCMSSWPackages/$dir $dir 
    else
      cp -r OldCMSSWPackages/$dir $dir;
    fi
  fi
done  
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
