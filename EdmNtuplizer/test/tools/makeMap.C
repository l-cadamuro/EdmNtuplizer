// #include "treeReader.h"

// // EType: 0:E+H, 1:E, 2:H
// TH2D* FillTTMap (TTree* mtree, int ev, int EType = 0)
// {
//     mtree->GetEntry(ev);
//     //TH2D* TTmap = new TH2D ("TTmap", "TTmap", 66, -33, 33, 74, 0, 74);
//     TH2D* TTmap = new TH2D ("TTmap", "TTmap", 6, -33, 33, 7, 0, 74);
//     for (int i = 0; i < mtree->tower_hwPt->size(); i++)
//     {
//         int ieta = mtree->tower_hwEta->at(i);
//         int iphi = mtree->tower_hwPhi->at(i);
//         int EtEm = mtree->tower_hwEtEm->at(i);
//         int EtHad = mtree->tower_hwEtHad->at(i);
//         int hwPt  = mtree->tower_hwPt->at(i);

//         int energy = hwPt;
//         if (EType == 1) energy = EtEm;
//         if (EType == 2) energy = EtHad;

//         cout << energy << " " << ieta << " " << iphi << endl;
//         TTmap->SetBinContent (TTmap->FindBin(ieta), TTmap->FindBin(iphi), energy);
//     }

//     return TTmap;
// }

void printMapOnTerminal (std::ostream& out, TTree* mtree, int ev, int EType = 0)
{
    int etaRange = 2*33; // should be limited to 28 but ok
    int phiRange = 72; // [1:72] in these ntuples
    const int spacing = 5; // width of each cell: 3 for energies + 1 space
    const char separator  = ' ';
    /*
    for (int i = 0; i < etaRange; i++)
    {
        out << "+---+";
    }
    out << "END" << endl;
    */

    // set tree branch addresses
    std::vector<int>     *L1TT_hwpt = 0;
    std::vector<int>     *L1TT_hweta = 0;
    std::vector<int>     *L1TT_hwphi = 0;
    std::vector<int>     *L1TT_hwem = 0;
    std::vector<int>     *L1TT_hwhad = 0;
    mtree->SetBranchAddress("L1TT_hwpt", &L1TT_hwpt);
    mtree->SetBranchAddress("L1TT_hweta", &L1TT_hweta);
    mtree->SetBranchAddress("L1TT_hwphi", &L1TT_hwphi);
    mtree->SetBranchAddress("L1TT_hwem", &L1TT_hwem);
    mtree->SetBranchAddress("L1TT_hwhad", &L1TT_hwhad);

    mtree->GetEntry(ev);
    // filled TT
    std:vector<std::pair<int,int>> TTpos;
    std::vector<int> TTen;
    
    
    for (int i = 0; i < L1TT_hwpt->size(); i++)
    {
        int ieta = L1TT_hweta->at(i);
        int iphi = L1TT_hwphi->at(i);
        int EtEm = L1TT_hwem->at(i);
        int EtHad = L1TT_hwhad->at(i);
        int hwPt  = L1TT_hwpt->at(i);

        int energy = hwPt;
        if (EType == 1) energy = EtEm;
        if (EType == 2) energy = EtHad;

        //cout << energy << " " << ieta << " " << iphi << endl;

        TTpos.push_back (make_pair(ieta, iphi));
        TTen.push_back (energy);
    }

    // now print title
    out << "EVENT: " << ev << endl;
    out << left << setw(spacing) << setfill(separator) << "";
    out << "||";
    //for (int i = 0; i < spacing-1; i++) cout << " ";
    //cout << "|";
    for (int i = 0; i < etaRange; i++)
    {
        int thisEta = i - (etaRange/2);
        out << left << setw(spacing) << setfill(separator) << thisEta;
        out << "|";
    }
    out << endl;

    for (int i = 0; i < (spacing+1)*(etaRange+1)+1; i++) out << "-";
    out << endl;

    // print table body
    for (int row = 1; row <= phiRange; row++)
    {
        int thisPhi = row;
        out << left << setw(spacing) << setfill(separator) << thisPhi;
        out << "||";
        for (int col = 0; col < etaRange; col++)
        {
            int thisEta = col - (etaRange/2);
            std::vector<pair<int,int>>::iterator it = find (TTpos.begin(), TTpos.end(), make_pair(thisEta, thisPhi));
            int thisEnergy = (it !=  TTpos.end() ? TTen.at(it - TTpos.begin()) : 0);

            if (thisEnergy != 0) out << left << setw(spacing) << setfill(separator) << thisEnergy;
            else out << left << setw(spacing) << setfill(separator) << "";
            out << "|";
        }
        out << endl;
    }



}

void makeMap(int ev = 0)
{
    //TFile* f = new TFile ("/home/llr/cms/cadamuro/Stage2TauEGamma/comparisons/pattern-SingleElec-1000evt_screen_ComparisonTree.root");
    TFile* f = new TFile ("../L1Ntuple_allEvts_MinBias_266667_lastEmulTag.root");
    //TFile* f = new TFile ("/home/llr/cms/cadamuro/Stage2TauEGamma/comparisons/pattern-H2Tau-1000evt_screen_fixTrimLut_29Ott2015_ComparisonTree.root");    
    TTree* t = (TTree*) f->Get("TreeEmul/L1EdmTreeEmul");

    // mergedTree* mtree = new mergedTree(t);

    cout << t->GetEntries() << endl;
    
    t->GetEntry(ev);
    
    // cout << "L1 candidates (emul): (Et -- hwEt, ieta, iphi)" << endl;
    // for (int i = 0; i < mtree->tau_ieta_emul->size(); i++)
    // {
    //    if (abs(mtree->tau_ieta_emul->at(i)) >= 29) continue; 
    //    cout << i << " - " << mtree->tau_ET_emul->at(i) << " -- " << mtree->tau_hwPt_emul->at(i) <<  " , " << mtree->tau_ieta_emul->at(i) << " , " << mtree->tau_iphi_emul->at(i) << endl;
    // }

    // cout << endl << " --------------------------------------- " << endl;

    // cout << "L1 candidates (firm): (Et , ieta, iphi)" << endl;
    // for (int i = 0; i < mtree->tau_ieta_fw->size(); i++)
    // {
    //     cout << i << " - " << mtree->tau_ET_fw->at(i) << " , " << mtree->tau_ieta_fw->at(i) << " , " << mtree->tau_iphi_fw->at(i) << endl;
    // }

    // cout << endl << " --------------------------------------- " << endl;

    // cout << endl << endl;
    
    ofstream outFileMap (Form("map_%i_Emul.txt", ev));
    printMapOnTerminal(outFileMap, t, ev);

    //TH2D* TTMap = FillTTMap (mtree, ev);
    //TTMap->Draw("COLZ");

}
