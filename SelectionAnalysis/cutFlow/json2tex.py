import json,argparse,math,os,sys
import cutFlowTools
sys.path.append(os.getenv('CMSSW_BASE')+'/MyCMSSWAnalysisTools/')
import Tools
import Tools.coreTools as coreTools
##############
def printLatexTableLine(cut, eff, evts):
  return cut+" &  $"+str(eff)+"$  & "+str(evts)+" \\\\"
def formatNumber(num):
  prec=2
  if num*math.pow(10,prec+1) > 1:
   return str( float(int( num*math.pow(10,prec+1)))/math.pow(10,prec+1) )
  return ("%."+str(prec)+"e")%num
def latex_float(f):
    float_str = f
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \cdot 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str
###############################

class json2tex(object):
  def __init__(self,jsF,printIt=False):
    print " processing ",jsF
    self.jsonInput = None if not os.path.isfile(jsF) else json.load(open(jsF))
    self.table = self.jsonInput["cutFlowRes"] if self.jsonInput.has_key("cutFlowRes") else self.jsonInput
    self.jsF = jsF+'_'+coreTools.idGenerator()
    self.printIt = printIt
  def convert(self):
    cutFlowsSorted = cutFlowTools.getSortedKeys(self.table)
    #print "sortedList ",cutFlowsSorted
    sortedPathList = reduce(lambda l1,l2:l1+l2,cutFlowsSorted)
    #print "sorted Path lsit ",sortedPathList
    if len(self.table.keys()) != len(sortedPathList):
      print "not all keys could be sorted"
      print "not sorted keys ",set(self.table.keys())-set(sortedPathList)
      sys.exit(1)
    texedTable=dict2tex(self.table,sortedPathList)
    texFilename = os.path.basename(self.jsF)+"_latex.tex"
    with open(texFilename,'w') as texOutput:
      texOutput.write("\n".join(texedTable))
    if self.printIt:
      print "converted to Latex:"
      for line in texedTable:
        print "  ",line,"\n"
    self.texFilename=texFilename
    return self.texFilename
####################
def dict2tex(theDict,sortedKeyList):
  lines=[]
  for key in (sortedKeyList if sortedKeyList else theDict.keys() ):
      print "key ",key, " item ",theDict[key] 
      item = theDict[key] 
      print "key ",key, " evenbts ",item['totalEvents'], " item ",item
      line=printLatexTableLine(key.replace('_','$\\_$'),latex_float(formatNumber(float(item['events'])/( item['preFilterPath']['preFilterPathEvents']if item['preFilterPath'] else item['totalEvents']))),item['events'])
      lines.append(line)
  return lines
#############

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input',required=True,help='json input')
  args=parser.parse_args()
  texFile = json2tex(args.input,printIt=True)
  print "latex in ",texFile
