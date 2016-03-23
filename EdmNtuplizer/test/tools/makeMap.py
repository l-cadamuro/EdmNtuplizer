from ROOT import *

fIn = TFile.Open ("../L1Ntuple_allEvts_MinBias_266667_lastEmulTag.root")
tree = fIn.Get("TreeData/L1EdmTreeData")

evtNum = 1968083

# retrieve evt entry

evtIdx = -1

br = tree.GetBranch("EventNumber")
for i in range(0, evtNum):
    br.GetEntry(i)
    num = tree.EventNumber
    if num == evtNum:
        evtIdx = i
        break

print "IDX: " , evtIdx
tree.GetEntry(evtIdx)

#### I have the index, make map
existing = {}
for TT in range (0, tree.L1TT_hwpt.size()):
    eta = tree.L1TT_hweta.at(TT)
    phi = tree.L1TT_hwphi.at(TT)
    pt = tree.L1TT_hwpt.at(TT)
    
    key = "%s,%s" % (str(eta), str(phi))
    existing [key] = pt

# mapFile = open ("map_"+str(evtNum)+".txt", 'w')
## make map!

# three = "   "
# two   = "  "
# one   = " "
# for iphi in range (0, 72):
#     print 
#     for ieta in range (-30, 30):
        
