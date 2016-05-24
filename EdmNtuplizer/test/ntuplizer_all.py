import FWCore.ParameterSet.Config as cms
from Configuration.AlCa.autoCond import autoCond
import os


PyFilePath = os.environ['CMSSW_BASE']+"/src/EdmNtuplizer/EdmNtuplizer/"

execfile(PyFilePath+"test/tools/EDM_list_pattern17Evts.py")

process = cms.Process("TEST")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")    

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    # 'file:/home/llr/cms/cadamuro/MWGR_802/CMSSW_8_0_2/src/RunOnPattern/dumpedFromData/l1tCalo_2016_simEDM_184Evts.root',
    # 'file:/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run267593_reEmulSecTrimFix/l1tCalo_2016_simEDM_34.root',
    # 'file:/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run267593_reEmulSecTrimFix/l1tCalo_2016_simEDM_35.root',
    # 'file:/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run267593_reEmulSecTrimFix/l1tCalo_2016_simEDM_38.root'  
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_mergedPattern_23Apr2015.root'
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_34.root'
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_TEST.root'
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_run271306Pier.root'
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_SudanCapture_data_calol2_160422_13_demux_15.root'
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_data_calol2_160422_13_demux_15_isoFix.root'
    #'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_34.root',
    #'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_35.root',
    #'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_38.root',
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_Sudan30Apr.root'
    # 'file:/home/llr/cms/cadamuro/TauFixEmulatorFork2/CMSSW_8_0_2/src/RunEmulator/l1tCalo_2016_simEDM_Sudan2Mag.root'
    'file:/home/llr/cms/strebler/L1_eg/fw_tests/P5_capture_files/data_calol2_160429_16_trunkdemux/good/demux/l1tCalo_2016_simEDM.root' # NB: demux only!!
    )
)
# process.source = cms.Source("PoolSource",
#     fileNames = FILELIST
# )

process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(1000)
    input = cms.untracked.int32(-1)
)

## init plugin
process.TreeData = cms.EDAnalyzer("Ntuplizer",
    L1Tau = cms.InputTag("caloStage2Digis", "MP"),
    L1demuxTau = cms.InputTag("caloStage2Digis", "Tau"),
    L1EG  = cms.InputTag("caloStage2Digis", "MP"),
    L1demuxEG  = cms.InputTag("caloStage2Digis", "EGamma"),
    L1TT  = cms.InputTag("caloStage2Digis", "CaloTower"),
    L1Clusters = cms.InputTag("NOTHING", ""),
    isEmulated = cms.bool(False),
    treeName = cms.string("L1EdmTreeData")
)

process.TreeEmul = process.TreeData.clone(
    L1Tau = cms.InputTag("simCaloStage2Digis", "MP"),
    L1demuxTau = cms.InputTag("simCaloStage2Digis", ""),
    L1EG  = cms.InputTag("simCaloStage2Digis", "MP"),
    L1demuxEG  = cms.InputTag("simCaloStage2Digis", ""),
    L1TT  = cms.InputTag("simCaloStage2Digis", "MP"),
    L1Clusters = cms.InputTag("simCaloStage2Digis", "MP"),
    isEmulated = cms.bool(True),
    treeName = cms.string("L1EdmTreeEmul")
)

# process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_allEvts_MinBias_266667_lastEmulTag.root'))
# process.TFileService=cms.Service('TFileService',fileName=cms.string('/home/llr/cms/cadamuro/MWGR_802/CMSSW_8_0_2/src/RunOnPattern/dumpedFromData/L1Ntuple_allEvts_AndyEmul_184Evts.root'))
# process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_reEmulSecTrimFix.root'))
# process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_reEmulWithGoodCalib_hasEMFix_34.root'))
#process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_finalTestAllFixes_1000Taus.root'))
# process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_Sudan30Apr.root'))
process.TFileService=cms.Service('TFileService',fileName=cms.string('L1Ntuple_Sudan2MagDemux.root'))

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
