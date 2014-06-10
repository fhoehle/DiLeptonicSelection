import json,argparse,math,os,sys
import cutFlowTools
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
def json2tex(jsF,printIt=False):
  table = json.load(open(jsF))
  cutFlowsSorted = cutFlowTools.getSortedKeys(table)
  sortedPathList = reduce(lambda l1,l2:l1+l2,cutFlowsSorted)
  if len(table.keys()) != len(sortedPathList):
    print "not all keys could be sorted"
    print "not sorted keys ",set(table.keys())-set(sortedPathList)
    sys.exit(1)
  texedTable=dict2tex(table,sortedPathList)
  texFilename = os.path.basename(jsF)+"_latex.tex"
  with open(texFilename,'w') as texOutput:
    texOutput.write("\n".join(texedTable))
  if printIt:
    print "converted to Latex:"
    for line in texedTable:
      print "  ",line,"\n"
  return texFilename
def dict2tex(theDict,sortedKeyList):
  lines=[]
  for key in (sortedKeyList if sortedKeyList else theDict.keys() ):
      item = theDict[key] 
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
