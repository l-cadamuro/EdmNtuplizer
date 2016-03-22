from ROOT import *
import sys
from array import array

def makeDataOverMCRatioPlot (hData, hMC, newName, horErrs=False):
    nPoints = hData.GetNbinsX()
    fX       = []
    fY       = []
    feYUp    = []
    feYDown  = []
    feXRight = []
    feXLeft  = []

    for ibin in range (1, nPoints+1):
        num = hData.GetBinContent(ibin)
        den = hMC.GetBinContent(ibin)
        if den > 0:
            # Y
            fY.append(num/den)
            feYUp.append(hData.GetBinErrorUp(ibin) / den)
            feYDown.append(hData.GetBinErrorLow(ibin) / den)

            # X
            fX.append (hData.GetBinCenter(ibin))
            if horErrs:
                feXRight.append(hData.GetBinLowEdge(ibin+1) - hData.GetBinCenter(ibin))
                feXLeft.append(hData.GetBinCenter(ibin) - hData.GetBinLowEdge(ibin))
            else:
                feXLeft.append(0.0)
                feXRight.append(0.0)

    afX       = array ("d", fX      )
    afY       = array ("d", fY      )
    afeYUp    = array ("d", feYUp   )
    afeYDown  = array ("d", feYDown )
    afeXRight = array ("d", feXRight)
    afeXLeft  = array ("d", feXLeft )

    # gRatio = TGraphAsymmErrors (len(afX), afX, afY, afeXLeft, afeXRight, afeYDown, afeYUp);
    gRatio = TGraph (len(afX), afX, afY);

    gRatio.SetMarkerStyle(8);
    gRatio.SetMarkerSize(1.);
    gRatio.SetMarkerColor(kBlack);
    gRatio.SetLineColor(kBlack);
    gRatio.SetName(newName)

    return gRatio;

def doComparison (hData, hEmul, c1, pad1, pad2, grRatio, hRatio, tag, xtitle, leg):
    c1.cd()
    pad1.cd()

    hEmul.SetLineColor(kRed)
    hEmul.SetLineWidth(2)
    hData.SetMarkerColor(kBlack)
    hData.SetMarkerSize(1)
    hData.SetMarkerStyle(8)

    hEmul.SetTitle(";;events")
    hEmul.GetXaxis().SetTitleSize(0)
    hEmul.GetXaxis().SetLabelSize(0)
    hEmul.GetYaxis().SetTitleSize(28)
    hEmul.GetYaxis().SetLabelSize(20)
    hEmul.GetXaxis().SetTitleFont(43) # so that size is in pixels
    hEmul.GetYaxis().SetTitleFont(43) # so that size is in pixels
    hEmul.GetXaxis().SetLabelFont(43) # so that size is in pixels
    hEmul.GetYaxis().SetLabelFont(43) # so that size is in pixels

    hEmul.Draw("hist")
    hData.Draw("P same")
    leg.Draw()

    c1.cd()
    pad2.cd()

    grRatio.SetMarkerSize(1)
    grRatio.SetMarkerStyle(8)
    
    # for axis only
    hRatio.SetMinimum(0)
    hRatio.SetMaximum(2)
    hRatio.SetTitle(";%s;Data/Emul" % xtitle)
    hRatio.GetXaxis().SetTitleSize(28)
    hRatio.GetYaxis().SetTitleSize(28)
    hRatio.GetXaxis().SetLabelSize(20)
    hRatio.GetYaxis().SetLabelSize(20)
    hRatio.GetYaxis().SetNdivisions(505)
    hRatio.GetXaxis().SetTitleFont(43) # so that size is in pixels
    hRatio.GetYaxis().SetTitleFont(43) # so that size is in pixels
    hRatio.GetXaxis().SetLabelFont(43) # so that size is in pixels
    hRatio.GetYaxis().SetLabelFont(43) # so that size is in pixels
    hRatio.GetXaxis().SetTitleOffset(3.0)

    hRatio.Draw()
    grRatio.Draw("P same")

    c1.Print ("comp_" + tag +".pdf", "pdf")

###########################################################

if __name__ == "__main__":

    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)

    # fData = TFile.Open ("../L1Ntuple_data.root")
    # fEmul = TFile.Open ("../L1Ntuple_emul.root")
    # tData = fData.Get("Tree/L1EdmTree")
    # tEmul = fEmul.Get("Tree/L1EdmTree")
    fIn = TFile.Open ("../L1Ntuple_allEvts_MinBias_266667.root")
    tData = fIn.Get("TreeData/L1EdmTreeData")
    tEmul = fIn.Get("TreeEmul/L1EdmTreeEmul")

    # -----------------------------------------------------
    ############ HISTOS DEFINITION

    hData_pt = TH1F ("hData_pt", "hData_pt", 256, 0, 256)
    hEmul_pt = TH1F ("hEmul_pt", "hEmul_pt", 256, 0, 256)

    hHotStripe_pt = TH1F ("hHotStripe_pt", "hHotStripe_pt", 256, 0, 256)

    hData_eta = TH1F ("hData_eta", "hData_eta", 70, -35, 35)
    hEmul_eta = TH1F ("hEmul_eta", "hEmul_eta", 70, -35, 35)

    hData_phi = TH1F ("hData_phi", "hData_phi", 75, 0, 75)
    hEmul_phi = TH1F ("hEmul_phi", "hEmul_phi", 75, 0, 75)

    hmapEtaPhiEmul = TH2F ("hmapEtaPhiEmul", "hmapEtaPhiEmul", 70, -35, 35, 75, 0, 75)
    hmapEtaPhiData = TH2F ("hmapEtaPhiData", "hmapEtaPhiData", 70, -35, 35, 75, 0, 75)

    hmapEtaPhiEmulSaturated = TH2F ("hmapEtaPhiEmulSaturated", "hmapEtaPhiEmulSaturated", 70, -35, 35, 75, 0, 75)

    ## TT 2d maps
    hmapTTEtaPhiEmul = TH2F ("hmapEtaTTPhiEmul", "hmapTTEtaPhiEmul", 70, -35, 35, 75, 0, 75)
    hmapTTEtaPhiEmulECALOnly = TH2F ("hmapTTEtaPhiEmulECALOnly", "hmapTTEtaPhiEmulECALOnly", 70, -35, 35, 75, 0, 75)
    hmapTTEtaPhiEmulHCALOnly = TH2F ("hmapTTEtaPhiEmulHCALOnly", "hmapTTEtaPhiEmulHCALOnly", 70, -35, 35, 75, 0, 75)
    hmapTTEtaPhiData = TH2F ("hmapEtaTTPhiData", "hmapTTEtaPhiData", 70, -35, 35, 75, 0, 75)

    # nData = tData.GetEntries()
    # nEmul = tEmul.GetEntries() 
    nData = 1000
    nEmul = 1000

    if nData != nEmul:
        print "** ERROR: Data / Emul trees have different entries: " , nData , "/" , nEmul
        sys.exit()

    print "Start loop on tree ..."
    for ev in range (0, nData):
        
        if ev % 1000 == 0:
            print ev , " / " , nData

        ### FIRMWARE
        tData.GetEntry(ev)
        # print " ====== EV:", ev, tData.EventNumber, tData.RunNumber, tData.lumi
        for i in range(0,tData.L1Tau_hwpt.size()):
            pt = tData.L1Tau_hwpt.at(i)
            if pt == 0: continue # skip dummy candidates
            hData_pt.Fill(pt)
            eta = tData.L1Tau_hweta.at(i)
            hData_eta.Fill(eta)
            phi = tData.L1Tau_hwphi.at(i)
            hData_phi.Fill(phi)
            hmapEtaPhiData.Fill (eta, phi)
            # print "TAU: " , i , pt, eta, phi

        # for i in range (0, tData.L1TT_hwpt.size()):
        #     pt  = tData.L1TT_hwpt.at(i)
        #     eta = tData.L1TT_hweta.at(i)
        #     phi = tData.L1TT_hwphi.at(i)
        #     hmapTTEtaPhiData.Fill(eta, phi)

        ### EMULATOR
        tEmul.GetEntry(ev)
        for i in range(0,tEmul.L1Tau_hwpt.size()):
            pt = tEmul.L1Tau_hwpt.at(i)
            hEmul_pt.Fill(pt)
            eta = tEmul.L1Tau_hweta.at(i)
            hEmul_eta.Fill(eta)
            phi = tEmul.L1Tau_hwphi.at(i)
            hEmul_phi.Fill(phi)
            hmapEtaPhiEmul.Fill (eta, phi)

            # if eta == 9 or eta == 12 or eta == -9 or eta == -12:
            if phi == 6 or phi == 10:
                hHotStripe_pt.Fill(pt)


        ## NB: only TT in emualtor have non-zero values for hwEtEm and hwEtHad
        for i in range (0, tEmul.L1TT_hwpt.size()):
            em = tEmul.L1TT_hwem.at(i)
            had = tEmul.L1TT_hwhad.at(i)
            # if had == 0: continue
            pt  = tEmul.L1TT_hwpt.at(i)
            eta = tEmul.L1TT_hweta.at(i)
            phi = tEmul.L1TT_hwphi.at(i)
            # print "TT:" , i, pt, eta, phi
            # if pt < 5 : continue
            hmapTTEtaPhiEmul.Fill(eta, phi)
            if had == 0:
                hmapTTEtaPhiEmulECALOnly.Fill (eta, phi)
            if em == 0:
                hmapTTEtaPhiEmulHCALOnly.Fill (eta, phi)

            if pt == 255:
                hmapEtaPhiEmulSaturated.Fill(eta, phi)

    c1 = TCanvas ("c1", "c1", 800, 600)
    pad1 = TPad ("pad1", "pad1", 0, 0.251, 1, 1.0)
    pad1.SetFrameLineWidth(3)
    pad1.SetLeftMargin(0.15)
    pad1.SetBottomMargin(0.02)
    pad1.SetTopMargin(0.1)
    pad1.Draw()
    # pad1.SetLogy()

    pad2 = TPad ("pad2", "pad2", 0, 0.0, 1, 0.24)
    pad2.SetLeftMargin(0.15);
    pad2.SetTopMargin(0.05);
    pad2.SetBottomMargin(0.35);
    pad2.SetGridy(True);
    pad2.SetFrameLineWidth(3)
    #pad2.SetGridx(True);
    pad2.Draw()

    leg = TLegend(0.6003571,0.89,0.8628571,0.99);
    leg.SetBorderSize(0);
    leg.SetLineColor(1);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    leg.SetFillColor(0);
    leg.SetFillStyle(0);
    leg.SetNColumns(2)

    entryEmul = leg.AddEntry("NULL","Firmware","p");
    entryEmul.SetLineColor(kRed);
    entryEmul.SetLineWidth(0);
    entryEmul.SetMarkerColor(kBlack);
    entryEmul.SetMarkerStyle(8);
    entryEmul.SetMarkerSize(1);
    entryEmul.SetTextFont(42);
    entryData = leg.AddEntry("NULL","Emulator","l");
    entryData.SetLineColor(kRed);
    entryData.SetLineWidth(2);
    entryData.SetMarkerColor(1);
    entryData.SetMarkerStyle(21);
    entryData.SetMarkerSize(0);
    entryData.SetTextFont(42);


    grRatio_pt = makeDataOverMCRatioPlot (hData_pt, hEmul_pt, "ratio_pt")
    hRatio_pt = TH1F ("hRatio_pt", "hRatio_pt", 100, hData_pt.GetBinLowEdge(1), hData_pt.GetBinLowEdge(hData_pt.GetNbinsX()+1))
    doComparison (hData_pt, hEmul_pt, c1, pad1, pad2, grRatio_pt, hRatio_pt, "pt", "hw pt [0.5 GeV]", leg)

    grRatio_eta = makeDataOverMCRatioPlot (hData_eta, hEmul_eta, "ratio_eta")
    hRatio_eta = TH1F ("hRatio_eta", "hRatio_eta", 100, hData_eta.GetBinLowEdge(1), hData_eta.GetBinLowEdge(hData_eta.GetNbinsX()+1))
    doComparison (hData_eta, hEmul_eta, c1, pad1, pad2, grRatio_eta, hRatio_eta, "eta", "hw ieta", leg)

    grRatio_phi = makeDataOverMCRatioPlot (hData_phi, hEmul_phi, "ratio_phi")
    hRatio_phi = TH1F ("hRatio_phi", "hRatio_phi", 100, hData_phi.GetBinLowEdge(1), hData_phi.GetBinLowEdge(hData_phi.GetNbinsX()+1))
    doComparison (hData_phi, hEmul_phi, c1, pad1, pad2, grRatio_phi, hRatio_phi, "phi", "hw iphi", leg)



    ######### 2d plots
    c2 = TCanvas ("c2", "c2", 800, 600)
    hmapEtaPhiEmul.SetTitle ("Emulator;ieta;phi")
    hmapEtaPhiEmul.Draw("COLZ")
    c2.Print ("mapetaphi_emul.pdf", "pdf")
    hmapEtaPhiData.SetTitle ("Firmware;ieta;phi")
    hmapEtaPhiData.Draw("COLZ")
    c2.Print ("mapetaphi_data.pdf", "pdf")

    hmapTTEtaPhiEmul.SetTitle ("TT - Emulator;ieta;iphi")
    hmapTTEtaPhiEmul.Draw("COLZ")
    c2.Print ("mapTTetaphi_emul.pdf", "pdf")
    hmapTTEtaPhiData.SetTitle ("TT - Data;ieta;iphi")
    hmapTTEtaPhiData.Draw("COLZ")
    c2.Print ("mapTTetaphi_data.pdf", "pdf")

    hmapTTEtaPhiEmulECALOnly.SetTitle ("TT - Emul ECAL only;ieta;iphi")
    hmapTTEtaPhiEmulECALOnly.Draw("COLZ")
    c2.Print ("mapTTetaphi_ECALonly_Emul.pdf", "pdf")
    hmapTTEtaPhiEmulHCALOnly.SetTitle ("TT - Emul HCAL only;ieta;iphi")
    hmapTTEtaPhiEmulHCALOnly.Draw("COLZ")
    c2.Print ("mapTTetaphi_HCALonly_Emul.pdf", "pdf")

    hmapEtaPhiEmulSaturated.Draw("COLZ")
    c2.Print ("hmapEtaPhiEmulSaturated.pdf", "pdf")

    c3 = TCanvas ("c3", "c3", 800, 600)
    hHotStripe_pt.Draw()
    c3.Print("hotStripes_pt.pdf", "pdf")

    print "CANDIATE NUMBERS -- data:" , hData_pt.Integral() , " Emul: " , hEmul_pt.Integral()
    print hHotStripe_pt.Integral()
    raw_input()

