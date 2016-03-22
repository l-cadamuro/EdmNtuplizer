cd /home/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/
export SCRAM_ARCH=slc6_amd64_gcc493
source /opt/exp_soft/cms/cmsset_default.sh
eval `scramv1 runtime -sh`
export X509_USER_PROXY=~/.t3/proxy.cert
cd /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/
cmsRun /grid_mnt/vol__vol_U__u/llr/cms/cadamuro/MWGR2016_Analysis_Stage2/CMSSW_8_0_2/src/EdmNtuplizer/processDatasets/runEmulator-CaloStage2.py maxEvents=-1 doLayer1=False inputFiles=file:/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub/l1tCalo_2016_EDM_7.root outFilePath=/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub outFileSuffix=7 >& /data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub/log_emul_7.txt
echo "All done for job 7"