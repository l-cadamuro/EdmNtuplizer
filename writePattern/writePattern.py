# dump rx patterns from EDM files

import FWCore.ParameterSet.Config as cms
from Configuration.AlCa.autoCond import autoCond
import os

# PyFilePath = os.environ['CMSSW_BASE']+"/src/EdmNtuplizer/writePattern/"

## file list of EDM files
PyFilePath = os.environ['CMSSW_BASE']+"/src/EdmNtuplizer/EdmNtuplizer/"
execfile(PyFilePath+"test/tools/EDM_list_emul_MinBias_267593_lastEmulTag_fixUnpack.py")

process = cms.Process("TEST")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")    

process.source = cms.Source("PoolSource",
    fileNames = FILELIST
)

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)

# process.l1tStage2InputPatternWriter = cms.EDAnalyzer('Stage2InputPatternWriter',
#     towerToken = cms.InputTag("l1tCaloStage2Layer1Digis", "CaloTower"),
#     filename   = cms.untracked.string("pattern1000.txt")
# )

process.load('L1Trigger.L1TCalorimeter.l1tStage2InputPatternWriter_cfi')
process.l1tStage2InputPatternWriter.filename = cms.untracked.string("pattern1000.txt")
process.l1tStage2InputPatternWriter.towerToken = cms.InputTag("caloStage2Digis", "CaloTower")

process.pattern = cms.Sequence(
    process.l1tStage2InputPatternWriter
)
process.p = cms.Path(process.pattern)