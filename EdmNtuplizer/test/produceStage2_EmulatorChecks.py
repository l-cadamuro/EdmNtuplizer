
# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: l1 -s L1 --pileup=NoPileUp --geometry DB --conditions=auto:startup -n 1 --no_exec --filein=/store/mc/Fall13dr/TT_Tune4C_13TeV-pythia8-tauola/GEN-SIM-RAW/tsg_PU40bx25_POSTLS162_V2-v1/00000/007939EF-8075-E311-B675-0025905938AA.root
import FWCore.ParameterSet.Config as cms

process = cms.Process('L1')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
    #fileNames = cms.untracked.vstring('/store/relval/CMSSW_7_1_0_pre2/RelValTTbar_13/GEN-SIM-DIGI-RAW-HLTDEBUG/POSTLS170_V3-v1/00000/20379CB0-E28E-E311-97BE-0026189438A7.root')
    fileNames = cms.untracked.vstring('file:/data_CMS/cms/vlonde/000EC1B0-27CD-E311-8169-00304867920C.root')
    #fileNames = cms.untracked.vstring('/store/mc/Fall13dr/DYJetsToLL_M-50_13TeV-pythia6/GEN-SIM-RAW/tsg_PU40bx25_POSTLS162_V2-v1/00000/044C97C0-B675-E311-B49C-0025901D4D76.root')
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('l1 nevts:1'),
    name = cms.untracked.string('Applications')
)



# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup', '')

# truth filter
process.mcFilter = cms.EDFilter("MCTruthFilter",
                                genParticlesTag = cms.InputTag("genParticles"),
                                pid = cms.int32(11)
                                )

# Raw to digi
process.load('Configuration.StandardSequences.RawToDigi_cff')

# upgrade calo stage 2
process.load('L1Trigger.L1TCalorimeter.L1TCaloStage2_PPFromRaw_cff')

# Ntuplizer
process.load('Ntuplizer.L1TriggerNtuplizer.l1TriggerNtuplizer_cfi')
process.l1TriggerNtuplizer.fillStage2 = cms.bool(True)

# TTree output file
process.load("CommonTools.UtilAlgos.TFileService_cfi")
process.TFileService.fileName = cms.string('tree_stage2_EmulatorChecks.root')

# Path and EndPath definitions
process.L1simulation_step = cms.Path(
    #process.mcFilter
    process.ecalDigis
    +process.hcalDigis
    +process.L1TCaloStage2_PPFromRaw
    +process.l1TriggerNtuplizer)


# Schedule definition
process.schedule = cms.Schedule(process.L1simulation_step)



