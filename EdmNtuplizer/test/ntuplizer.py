import FWCore.ParameterSet.Config as cms
from Configuration.AlCa.autoCond import autoCond
import os
import FWCore.ParameterSet.VarParsing as VarParsing

##########################
isEmulated = True
##########################

## override isEmulated flag if in input, otherwise use standard one
options = VarParsing.VarParsing ('analysis')
options.register ('isEmulated',
                  None,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,
                  "is emulated?")
options.parseArguments()

if not options.isEmulated == None:
    if options.isEmulated == 0:
        isEmulated = False
    else:
        isEmulated = True
print "isEmulated?: " , isEmulated
#####

PyFilePath = os.environ['CMSSW_BASE']+"/src/EdmNtuplizer/EdmNtuplizer/"
if isEmulated:
    execfile(PyFilePath+"test/tools/EDM_list_emul.py")
else:
    execfile(PyFilePath+"test/tools/EDM_list_data.py")


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
    input = cms.untracked.int32(1000)
)

## init plugin
process.Tree = cms.EDAnalyzer("Ntuplizer",
    L1Tau = cms.InputTag("caloStage2Digis", "MP"),
    L1EG  = cms.InputTag("caloStage2Digis", "MP"),
    L1TT  = cms.InputTag("caloStage2Digis", ""),
    L1Clusters = cms.InputTag("NOTHING", ""),
    isEmulated = cms.bool(isEmulated)
)

if isEmulated:
    process.Tree.L1Tau = cms.InputTag("simCaloStage2Digis", "MP")
    process.Tree.L1EG  = cms.InputTag("simCaloStage2Digis", "MP")
    process.Tree.L1TT  = cms.InputTag("simCaloStage2Digis", "MP")
    process.Tree.L1Clusters = cms.InputTag("simCaloStage2Digis", "MP")

if isEmulated:
    process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_emul.root'))
else:
    process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_data.root'))

process.ntuples = cms.Sequence(
    process.Tree
)

process.p = cms.Path(process.ntuples)

# Silence output
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000