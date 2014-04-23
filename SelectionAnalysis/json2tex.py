import json,argparse,math
##############
def printLatexTableLine(cut, eff, evts):
  return cut+" & "+str(eff)+" & "+str(evts)+" \\\\"
def formatNumber(num):
  prec=2
  if num*math.pow(10,prec+1) > 1:
   return str( float(int( num*math.pow(10,prec+1)))/math.pow(10,prec+1) )
  return ("%."+str(prec)+"e")%num
def latex_float(f):
    float_str = f
    if "e" in float_str:
        base, exponent = float_str.split("e")
        return r"{0} \times 10^{{{1}}}".format(base, int(exponent))
    else:
        return float_str
#############
parser = argparse.ArgumentParser()
parser.add_argument('--input',required=True,help='json input')
args=parser.parse_args()
table = json.load(open(args.input))
diMuon = filter(lambda s : s.startswith('diMuon_'),table.keys())
diMuon.sort(key=lambda n : -1*table[n]['events'])
diElectronMuon = filter(lambda s : s.startswith('diElectronMuon_'),table.keys())
diElectronMuon.sort(key=lambda n : -1*table[n]['events'])
diElectron = filter(lambda s : s.startswith('diElectron_'),table.keys())
diElectron.sort(key=lambda n : -1*table[n]['events'])
for key in diMuon+diElectronMuon+diElectron:
  item = table[key] 
  print printLatexTableLine(key,latex_float(formatNumber(float(item['events'])/( item['preFilterPath']['preFilterPathEvents']if item['preFilterPath'] else item['totalEvents']))),item['events'])
