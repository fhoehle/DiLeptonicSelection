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
#############

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input',required=True,help='json input')
  args=parser.parse_args()
  table = json.load(open(args.input))
  cutFlowsSorted = cutFlowTools.getSortedKeys(table)
  sortedPathList = reduce(lambda l1,l2:l1+l2,cutFlowsSorted)
  if len(table.keys()) != len(sortedPathList):
    print "not all keys could be sorted"
    print "not sorted keys ",set(table.keys())-set(sortedPathList)
    sys.exit(1)
  with open(os.path.basename(args.input)+"_latex.tex",'w') as texOutput:
    for key in sortedPathList:
      item = table[key] 
      line=printLatexTableLine(key.replace('_','$\\_$'),latex_float(formatNumber(float(item['events'])/( item['preFilterPath']['preFilterPathEvents']if item['preFilterPath'] else item['totalEvents']))),item['events'])
      print line
      texOutput.write(line+"\n")
    print "latex in ",texOutput.name
