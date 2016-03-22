import FWCore.ParameterSet.Config as cms
from Configuration.AlCa.autoCond import autoCond
import os


PyFilePath = os.environ['CMSSW_BASE']+"/src/EdmNtuplizer/EdmNtuplizer/"

execfile(PyFilePath+"test/tools/EDM_list_emul_MinBias_266667.py")

process = cms.Process("TEST")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")    

# process.source = cms.Source("PoolSource",
#     fileNames = cms.untracked.vstring(
#     'file:/home/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/l1tCalo_2016_EDM.root',
#     )
# )
process.source = cms.Source("PoolSource",
    fileNames = FILELIST
)

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

## init plugin
process.TreeData = cms.EDAnalyzer("Ntuplizer",
    L1Tau = cms.InputTag("caloStage2Digis", "MP"),
    L1EG  = cms.InputTag("caloStage2Digis", "MP"),
    L1TT  = cms.InputTag("caloStage2Digis", "CaloTower"),
    L1Clusters = cms.InputTag("NOTHING", ""),
    isEmulated = cms.bool(False),
    treeName = cms.string("L1EdmTreeData")
)

process.TreeEmul = process.TreeData.clone(
    L1Tau = cms.InputTag("simCaloStage2Digis", "MP"),
    L1EG  = cms.InputTag("simCaloStage2Digis", "MP"),
    L1TT  = cms.InputTag("simCaloStage2Digis", "MP"),
    L1Clusters = cms.InputTag("simCaloStage2Digis", "MP"),
    isEmulated = cms.bool(True),
    treeName = cms.string("L1EdmTreeEmul")
)

process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_allEvts_MinBias_266667.root'))

# if isEmulated:
#     process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_emul.root'))
# else:
#     process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_data.root'))

process.ntuples = cms.Sequence(
    process.TreeData + 
    process.TreeEmul
)

process.p = cms.Path(process.ntuples)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000