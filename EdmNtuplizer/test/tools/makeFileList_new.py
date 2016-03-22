import os, re

path = "/data_CMS/cms/cadamuro/test_submit_to_tier3/Stage2_Commissioning_MinBias_Run266667_resub/"

##############################################

listaData = []
listaEmul = []

if not path.endswith("/"):
    path += "/"

print path

for dd in os.listdir(path):
    m = re.search("l1tCalo_2016_simEDM_\d+.root", dd)
    if m:
        nameEmul = "'file:" + path + dd + "',"
        listaEmul.append(nameEmul)
# outData = open ("EDM_list_data.py", 'w')
# outData.write("FILELIST = cms.untracked.vstring()\n")
# outData.write("FILELIST.extend ([\n")
# for dd in listaData:
#     outData.write(dd+"\n")
# outData.write("])\n")

outEmul = open ("EDM_list_emul_MinBias_266667.py", 'w')
outEmul.write("FILELIST = cms.untracked.vstring()\n")
outEmul.write("FILELIST.extend ([\n")
for dd in listaEmul:
    outEmul.write(dd+"\n")
outEmul.write("])\n")

