cd /home/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/
export SCRAM_ARCH=slc6_amd64_gcc493
source /opt/exp_soft/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
export X509_USER_PROXY=~/.t3/proxy.cert
cd /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/
cmsRun /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/unpackData-CaloStage2.py maxEvents=-1 edm=True inputFiles=/store/data/Commissioning2016/MinimumBias/RAW/v1/000/266/667/00000/54E5A42C-66E8-E511-9C28-02163E0144F4.root outFilePath=/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub outFileSuffix=17 >& /data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub/log_unpack_17.txt
cmsRun /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/runEmulator-CaloStage2.py maxEvents=-1 doLayer1=False inputFiles=file:/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resubl1tCalo_2016_EDM_17.root outFilePath=/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub outFileSuffix=17 >& /data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub/log_emul_17.txt
echo "All done for job 17"