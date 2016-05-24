import os, sys

inputList = "fileList_MinimumBias_Commissioning2016_v1_run269160.txt"
outputPath = "/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run269160"

jobfolder = "./MinimumBias_run269160"
os.system("mkdir %s"%jobfolder)
os.system("mkdir %s"%outputPath)

inpt = open(inputList)

pwd = os.environ['CMSSW_BASE']+"/src/EdmNtuplizer/processDatasets/"
srcpwd = os.environ['CMSSW_BASE']+"/src/"

# source tier 3
os.system("source /opt/exp_soft/cms/t3/t3setup")

standardT3 = [
"cd %s" % srcpwd,
"export SCRAM_ARCH=slc6_amd64_gcc493",
"source /opt/exp_soft/cms/cmsset_default.sh",
"eval `scramv1 runtime -sh`",
"export X509_USER_PROXY=~/.t3/proxy.cert",
"cd %s" % pwd
]


for idx, ff in enumerate(inpt):
    name = ff.strip()
    # print name

    # unpack part
    logname = outputPath + "/log_unpack_"+str(idx)+".txt"
    commandUnpck = "cmsRun " + pwd+"unpackData-CaloStage2.py maxEvents=-1 edm=True inputFiles="+name + " outFilePath="+outputPath + " outFileSuffix="+str(idx) + " >& " + logname 
    # print commandUnpck
    
    # reemulateion part
    inptsName = "file:"+outputPath+"/l1tCalo_2016_EDM_"+str(idx)+".root"
    logname2 = outputPath + "/log_emul_"+str(idx)+".txt"
    commandEmul = "cmsRun " + pwd+"runEmulator-CaloStage2.py maxEvents=-1 doLayer1=False inputFiles="+inptsName + " outFilePath="+outputPath + " outFileSuffix="+str(idx) + " >& " + logname2 
    # print commandEmul

    jobfile = open (jobfolder + "/job_"+str(idx)+".sh", 'w')
    for ll in standardT3:
        jobfile.write(ll+"\n")
    jobfile.write(commandUnpck+"\n")
    jobfile.write(commandEmul+"\n")
    jobfile.write('echo "All done for job %s"' % str(idx))
    jobfile.close()
    
    # launch on tier3!
    launchCmd = ('/opt/exp_soft/cms/t3/t3submit -q cms \'' + jobfolder + '/job_' + str (idx) + '.sh\'')
    # print launchCmd
    os.system(launchCmd)
