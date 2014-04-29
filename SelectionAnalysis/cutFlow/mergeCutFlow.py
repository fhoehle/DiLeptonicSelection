import json,argparse,sys
import cutFlowTools
###########
def mergePath(pathName,cutFLows,subKey="events"):
  return sum( [ d[pathName][subKey] for d in cutFLows] )
def mergedDict(cutFLows):
  keys=cutFLows[0].keys()
  return dict( [ (k,{'events':mergePath(k,cutFLows),'totalEvents':mergePath(k,cutFLows,subKey='totalEvents')}) for k in keys] )
######################### 
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--input',nargs='*',required = True,help='input of cutFlow JSONs')
  args = parser.parse_args()
  cutFlowsAndFiles=[(json.load(open(f)),f) for f in args.input]
  testSet = set(cutFlowsAndFiles[0][0])
  for d in cutFlowsAndFiles[1:]:
    if not testSet ==  set(d[0]):
      print d[1]," has not same keys as ",cutFlowsAndFiles[0][1]
      sys.exit(1)
  ##############
  cutFlows = [d[0] for d in cutFlowsAndFiles]
  mergedCutFlows = mergedDict(cutFlows)
  cutFlowsSorted = cutFlowTools.getSortedKeys(mergedCutFlows)
  paths=cutFlows[0].keys()
  sortedPathList = reduce(lambda l1,l2:l1+l2,cutFlowsSorted) 
  if len(paths) != len(sortedPathList):
    print "not all keys could be sorted"
    print "not sorted keys ",set(paths)-set(sortedPathList)
  ####################
  for c in cutFlowsSorted:
    for p in c:
      print p," ", mergePath(p,cutFlows) 
    print "################################"
