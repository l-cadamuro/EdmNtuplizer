#include <vector>
#include <map>
#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "treeReader.h"

using namespace std;

// c++ -lm -o linearize linearize.cpp treeReader.cc `root-config --glibs --cflags`

/*
** DESCRIPTION: create a linear tree where for each entry one has the emulated and corresponding firmware tau
** NOTE!!! this relies on the 100% correspondence between firmware and emulator in the position of eta, phi
*/

int main(int argc, char** argv)
{
    TFile* fIn = new TFile ("/home/llr/cms/cadamuro/MWGR2016_Analysis_Stage2_LastTag/CMSSW_8_0_2/src/EdmNtuplizer/EdmNtuplizer/test/L1Ntuple_allEvts_MinBias_266667_lastEmulTag.root");
    TTree* tData = (TTree*) fIn->Get("TreeData/L1EdmTreeData");
    TTree* tEmul = (TTree*) fIn->Get("TreeEmul/L1EdmTreeEmul");

    treeReader* rData = new treeReader (tData);
    treeReader* rEmul = new treeReader (tEmul);

    // int nEvents = rData->GetEntries();
    int nEvents = 1000;

    ////////////////////////////////////////
    TFile* fOut = new TFile ("linearized_L1Tree.root", "recreate");
    TTree* outTree = new TTree("linearTree", "linearTree");
    
    ULong64_t EventNumber;
    int emul_hwpt;
    int emul_hweta;
    int emul_hwphi;
    int emul_hwiso;
    int emul_hwqual;
    int emul_hwrawpt;
    int emul_hwisoet;    
    int data_hwpt;
    int data_hweta;
    int data_hwphi;
    int data_hwiso;
    int data_hwqual;
    int data_hwrawpt;
    int data_hwisoet;
    int nTT;
    bool hasEM;
    bool isMerged;

    outTree->Branch("EventNumber", &EventNumber, "EventNumber/l");
    outTree->Branch("emul_hwpt", &emul_hwpt, "emul_hwpt/I");
    outTree->Branch("emul_hweta", &emul_hweta, "emul_hweta/I");
    outTree->Branch("emul_hwphi", &emul_hwphi, "emul_hwphi/I");
    outTree->Branch("emul_hwiso", &emul_hwiso, "emul_hwiso/I");
    outTree->Branch("emul_hwqual", &emul_hwqual, "emul_hwqual/I");
    outTree->Branch("emul_hwrawpt", &emul_hwrawpt, "emul_hwrawpt/I");
    outTree->Branch("emul_hwisoet", &emul_hwisoet, "emul_hwisoet/I");    
    outTree->Branch("data_hwpt", &data_hwpt, "data_hwpt/I");
    outTree->Branch("data_hweta", &data_hweta, "data_hweta/I");
    outTree->Branch("data_hwphi", &data_hwphi, "data_hwphi/I");
    outTree->Branch("data_hwiso", &data_hwiso, "data_hwiso/I");
    outTree->Branch("data_hwqual", &data_hwqual, "data_hwqual/I");
    outTree->Branch("data_hwrawpt", &data_hwrawpt, "data_hwrawpt/I");
    outTree->Branch("data_hwisoet", &data_hwisoet, "data_hwisoet/I");
    outTree->Branch("nTT", &nTT, "nTT/I");
    outTree->Branch("hasEM", &hasEM, "hasEM/O");
    outTree->Branch("isMerged", &isMerged, "isMerged/O");

    ////////////////////////////////////////


    for (int iEv = 0; iEv < nEvents; iEv++)
    {
        rData->GetEntry(iEv);
        rEmul->GetEntry(iEv);

        if (iEv % 10000 == 0) cout << iEv << endl;
        // cout << endl << " ========================================== " << iEv << endl << endl;

        // loop on emulated candidates, fill a map with: (emul ieta, emul iphi) -- (idx emul)
        map <pair<int, int>, int> mapEmulIdx;

        // if (rEmul->L1Tau_hwpt->size() != rData->L1Tau_hwpt->size())
        // {
        //     cout << "*** WARNING!! Size of emul and data is different for event/run/lumi " << rData->EventNumber << "/" << rData->RunNumber << "/" << rData->lumi << "  -- evt idx " << iEv << endl;
        // }

        int nTauEmul = rEmul->L1Tau_hwpt->size();
        int nTauData = 0; // remove 0 E cands

        for (int i = 0; i < rEmul->L1Tau_hwpt->size(); i++)
        {
            int ieta = rEmul->L1Tau_hweta->at(i);
            int iphi = rEmul->L1Tau_hwphi->at(i);
            mapEmulIdx[make_pair(ieta, iphi)] = i;
            // cout << "Emul: " << i << " " << ieta << " " << iphi << endl;
        }

        // loop on firmware candidates
        for (int i = 0; i < rData->L1Tau_hwpt->size(); i++)
        {
            int pt = rData->L1Tau_hwpt->at(i);
            if (pt == 0) continue;

            nTauData++;
            int ieta = rData->L1Tau_hweta->at(i);
            int iphi = rData->L1Tau_hwphi->at(i);
            // cout << "Data: " << i << " " << ieta << " " << iphi << " [ pt: " << pt << endl;
            auto it = mapEmulIdx.find(make_pair(ieta, iphi));
            if (it != mapEmulIdx.end())
            {
                int idxEmul = it->second;

                // set tree and fill
                if (rEmul->EventNumber != rData->EventNumber) 
                {
                    cout << "*** ERROR: different event number!!!!" << endl;
                    continue;
                }

                EventNumber  = rEmul->EventNumber;
                emul_hwpt    = rEmul->L1Tau_hwpt->at(idxEmul);
                emul_hweta   = rEmul->L1Tau_hweta->at(idxEmul);
                emul_hwphi   = rEmul->L1Tau_hwphi->at(idxEmul);
                emul_hwiso   = rEmul->L1Tau_hwiso->at(idxEmul);
                emul_hwqual  = rEmul->L1Tau_hwqual->at(idxEmul);
                emul_hwrawpt = (rEmul->L1Tau_hwrawpt->at(idxEmul) < 256 ? rEmul->L1Tau_hwrawpt->at(idxEmul) : 255);
                emul_hwisoet = rEmul->L1Tau_hwisoet->at(idxEmul);  
                data_hwpt    = rData->L1Tau_hwpt->at(i);
                data_hweta   = rData->L1Tau_hweta->at(i);
                data_hwphi   = rData->L1Tau_hwphi->at(i);
                data_hwiso   = rData->L1Tau_hwiso->at(i);
                data_hwqual  = rData->L1Tau_hwqual->at(i);
                data_hwrawpt = rData->L1Tau_hwrawpt->at(i);
                data_hwisoet = rData->L1Tau_hwisoet->at(i);  
                nTT          = rEmul->L1Tau_nTT->at(idxEmul);  
                hasEM        = rEmul->L1Tau_hasEM->at(idxEmul);    
                isMerged     = rEmul->L1Tau_isMerged->at(idxEmul);       

                outTree->Fill();
            }
            else
            {
                cout << "  ---> MISMATCH: did not find eta-phi " << ieta << "-" << iphi << " in emulated tree, skipping" << endl;
                continue;
            }
        }

        if (nTauData != nTauEmul) cout << "*** WARNING!! Size of emul and data is different for event/run/lumi " << rData->EventNumber << "/" << rData->RunNumber << "/" << rData->lumi << "  -- evt idx " << iEv << endl;
    }

    cout << "Finished loop" << endl;
    outTree->Write();

    cout << "Written tree" << endl;
    fOut->Close();
    cout << "closed out file" << endl;
}