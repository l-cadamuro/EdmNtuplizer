cd /home/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/
export SCRAM_ARCH=slc6_amd64_gcc493
source /opt/exp_soft/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
export X509_USER_PROXY=~/.t3/proxy.cert
cd /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/
cmsRun /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/unpackData-CaloStage2.py maxEvents=-1 edm=True inputFiles=/store/data/Commissioning2016/MinimumBias/RAW/v1/000/266/667/00000/60FA322D-89E8-E511-A7A1-02163E011FCE.root outFilePath=/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667 outFileSuffix=22 >& /data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667/log_unpack_22.txt
cmsRun /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/runEmulator-CaloStage2.py maxEvents=-1 doLayer1=False inputFiles=file:/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667l1tCalo_2016_EDM_22.root outFilePath=/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667 outFileSuffix=22 >& /data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667/log_emul_22.txt
echo "All done for job 22"