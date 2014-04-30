import json,argparse,math,os,sys,subprocess
import json2tex 
##############
#############
def texHeader():
  return  "\\documentclass[12pt]{article}\n"+"\\usepackage{listings}"+"\\begin{document} \n"
def createTexTableFromFragmentFile(fragmentFile):
  return  "\\begin{tabular}[h]{c c c} \n" + "  \\input{"+fragmentFile+"}\n" + "\\end{tabular} \n"
def texEnd():
  return "\\end{document} \n"
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
  texFile = open("test.tex","w")
  texFile.write(texHeader()+"\n\n")
  for jsF in args.input:
    print "convert to latex ",jsF
    latexJsF=json2tex.json2tex(jsF)
    print "done, created ",latexJsF
    latexTables.append(latexJsF)
    texFile.write("\\begin{lstlisting}[breaklines]\n  "+jsF+"\n\\end{lstlisting}"+"\n")
    texFile.write(createTexTableFromFragmentFile(latexJsF)+"\n\\newpage\n\n")
  texFile.write(texEnd()+"\n")
  texFile.close()
  pdfLatex=subprocess.Popen(["pdflatex "+texFile.name],shell=True)
  pdfLatex.wait()
  #print pdfLatex.communicate()[0]
  sys.exit(pdfLatex.returncode)
