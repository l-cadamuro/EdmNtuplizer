import os

path = "/data_CMS/cms/strebler/L1_eg/Run266423/MinimumBias_l1t_tsg_v3_firm_match_v16.03.10_266423/"

##############################################

listaData = []
listaEmul = []

if not path.endswith("/"):
    path += "/"

print path

for dd in os.listdir(path):
    if os.path.isdir(path+dd):
        nameData = "'file:" + path + dd + "/" + "l1tCalo_2016_EDM.root',"
        nameEmul = "'file:" + path + dd + "/" + "l1tCalo_2016_simEDM.root',"
        listaData.append(nameData)
        listaEmul.append(nameEmul)

outData = open ("EDM_list_data.py", 'w')
outData.write("FILELIST = cms.untracked.vstring()\n")
outData.write("FILELIST.extend ([\n")
for dd in listaData:
    outData.write(dd+"\n")
outData.write("])\n")

outEmul = open ("EDM_list_emul.py", 'w')
outEmul.write("FILELIST = cms.untracked.vstring()\n")
outEmul.write("FILELIST.extend ([\n")
for dd in listaEmul:
    outEmul.write(dd+"\n")
outEmul.write("])\n")

