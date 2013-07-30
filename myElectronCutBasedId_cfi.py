import FWCore.ParameterSet.Config as cms

simpleCutBasedElectronID = cms.EDProducer("EleIdCutBasedExtProducer",
  src = cms.InputTag("gsfElectrons"),
  reducedBarrelRecHitCollection = cms.InputTag("reducedEcalRecHitsEB"),
  reducedEndcapRecHitCollection = cms.InputTag("reducedEcalRecHitsEE"),
  verticesCollection = cms.InputTag("offlineBeamSpot"),
  dataMagneticFieldSetUp = cms.bool(False),
  dcsTag = cms.InputTag("scalersRawToDigi"),                                          
  algorithm = cms.string('eIDCB'),
  electronIDType  = cms.string('robust'),
  electronQuality = cms.string('test'),
  electronVersion = cms.string('V04'),
  #### Selections with Relative Isolation                                          
  robust95relIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(5.0e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 1.5e-01, 
                               2.0e+00, 1.2e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
         endcap =  cms.vdouble(7.0e-02, 3.0e-02, 7.0e-01, 1.0e-02, -1, -1, 9999., 9999., 9999., 9999., 9999., 8.0e-02, 
                               6.0e-02, 5.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
  ),
  robust90relIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(1.2e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 1.2e-01, 
                               9.0e-02, 1.0e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(5.0e-02, 3.0e-02, 7.0e-01, 9.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 5.0e-02, 
                               6.0e-02, 3.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
  ),
  robust85relIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 6.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9.0e-02, 
                               8.0e-02, 1.0e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 4.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 5.0e-02, 
                               5.0e-02, 2.5e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
  ),
  robust80relIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9.0e-02, 
                               7.0e-02, 1.0e-01, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 3.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 4.0e-02, 
                               5.0e-02, 2.5e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
  ),
  # 70% point modified with restricting cuts to physical values                                                                                    
  robust70relIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(2.5e-02, 1.0e-02, 3.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 5.0e-02, 
                               6.0e-02, 3.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 2.5e-02, 
                               2.5e-02, 2.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
  ),
  # 60% point modified with restricting cuts to physical values                                                                                    
  robust60relIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(2.5e-02, 1.0e-02, 2.5e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 4.0e-02, 
                               4.0e-02, 3.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 2.5e-02, 
                               2.0e-02, 2.0e-02, 9999., 9999., 9999., 9999., 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
  ),
  #### Selections with Combined Isolation

  robust95cIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(5.0e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 1.5e-01, 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
         endcap =  cms.vdouble(7.0e-02, 3.0e-02, 7.0e-01, 1.0e-02, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 1.0e-01, 0.0, -9999., 9999., 9999., 1, -1, 0.0, 0.0, ),
  ),
  robust90cIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(1.2e-01, 1.0e-02, 8.0e-01, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 1.0e-01, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(5.0e-02, 3.0e-02, 7.0e-01, 9.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 7.0e-02, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
  ),
  robust85cIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 6.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 9.0e-02, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 4.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 6.0e-02, 0.0, -9999., 9999., 9999., 1, -1, 0.02, 0.02, ),
  ),
  robust80cIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(4.0e-02, 1.0e-02, 6.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 7.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 3.0e-02, 7.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 6.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
  ),
  # 70% point modified with restricting cuts to physical values                                          
  robust70cIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(2.5e-02, 1.0e-02, 3.0e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 4.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 3.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
  ),
  # 60% point modified with restricting cuts to physical values
  robust60cIsoEleIDCutsV04 = cms.PSet(
         barrel =  cms.vdouble(2.5e-02, 1.0e-02, 2.5e-02, 4.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 3.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
         endcap =  cms.vdouble(2.5e-02, 3.0e-02, 2.0e-02, 5.0e-03, -1, -1, 9999., 9999., 9999., 9999., 9999., 9999., 
                               9999., 9999., 9999., 9999., 9999., 2.0e-02, 0.0, -9999., 9999., 9999., 0, -1, 0.02, 0.02, ),
  ),

)
simpleEleId90cIso = simpleCutBasedElectronID.clone()
simpleEleId90cIso.electronQuality = '90cIso'

