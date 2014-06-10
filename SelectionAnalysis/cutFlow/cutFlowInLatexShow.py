import json,argparse,math,os,sys,subprocess
import json2tex 
##############
#############
class cutFlowTexFile(object):
  def __init__(self,texFileName='test.tex'):
    self.texFile = open(texFileName,'w')
    self.header = "\\documentclass[12pt]{article}\n"+"\\usepackage{listings}"+"\\begin{document} \n\n\n"
  def writeHeader(self):
    self.texFile.write(self.header)
  def addTexTableFromFragmentFile(self,fragmentFile,postfix=""):
    self.texFile.write("\\begin{tabular}[h]{c c c} \n" + "  \\input{"+fragmentFile+"}\n" + "\\end{tabular} \n"+postfix)
  def texEnd(self):
    self.texFile.write("\\end{document} \n")
    self.texFile.close()
###############
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--input',nargs="*",required=True,help='jsons input')
  parser.add_argument('--useTTbar',action="store_true",default=False,help='use TTbar events, i.e. looking for dilep tagging')
  args=parser.parse_args()
  if args.useTTbar:
    json2tex.cutFlowTools.channels.extend(['diLep_diMuonMC', u'diLep_ElectronMuonMC', u'diLep_diElectronMC', u'diLepMC'])
  latexTables = []
  print " creating test.tex"
  texFile = cutFlowTexFile()
  texFile.writeHeader()
  for jsF in args.input:
    print "convert to latex ",jsF
    latexJsF=json2tex.json2tex(jsF)
    print "done, created ",latexJsF
    latexTables.append(latexJsF)
    texFile.texFile.write("\\begin{lstlisting}[breaklines]\n  "+jsF+"\n\\end{lstlisting}"+"\n")
    texFile.addTexTableFromFragmentFile(latexJsF,postfix="\n\\newpage\n\n")
  texFile.texEnd()
  pdfLatex=subprocess.Popen(["pdflatex "+texFile.texFile.name],shell=True)
  pdfLatex.wait()
  #print pdfLatex.communicate()[0]
  sys.exit(pdfLatex.returncode)
