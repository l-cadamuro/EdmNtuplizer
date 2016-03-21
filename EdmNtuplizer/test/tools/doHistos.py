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

    gStyle.SetOptStat(0)

    fData = TFile.Open ("../L1Ntuple_data.root")
    fEmul = TFile.Open ("../L1Ntuple_emul.root")

    tData = fData.Get("Tree/L1EdmTree")
    tEmul = fEmul.Get("Tree/L1EdmTree")

    # -----------------------------------------------------
    ############ HISTOS DEFINITION

    hData_pt = TH1F ("hData_pt", "hData_pt", 256, 0, 256)
    hEmul_pt = TH1F ("hEmul_pt", "hEmul_pt", 256, 0, 256)

    hData_eta = TH1F ("hData_eta", "hData_eta", 70, -35, 35)
    hEmul_eta = TH1F ("hEmul_eta", "hEmul_eta", 70, -35, 35)

    hData_phi = TH1F ("hData_phi", "hData_phi", 75, 0, 75)
    hEmul_phi = TH1F ("hEmul_phi", "hEmul_phi", 75, 0, 75)


    nData = tData.GetEntries()
    nEmul = tEmul.GetEntries() 
    # nData = 100
    # nEmul = 100

    if nData != nEmul:
        print "** ERROR: Data / Emul trees have different entries: " , nData , "/" , nEmul
        sys.exit()

    print "Start loop on tree ..."
    for ev in range (0, nData):
        
        if ev % 1000 == 0:
            print ev , " / " , nData

        tData.GetEntry(ev)
        print " ====== EV:", ev, tData.EventNumber

        for i in range(0,tData.L1Tau_hwpt.size()):
            pt = tData.L1Tau_hwpt.at(i)
            if pt == 0: continue # skip dummy candidates
            hData_pt.Fill(pt)
            eta = tData.L1Tau_hweta.at(i)
            hData_eta.Fill(eta)
            phi = tData.L1Tau_hwphi.at(i)
            hData_phi.Fill(phi)
            print "TAU: " , i , pt, eta, phi

        tEmul.GetEntry(ev)
        for i in range(0,tEmul.L1Tau_hwpt.size()):
            pt = tEmul.L1Tau_hwpt.at(i)
            hEmul_pt.Fill(pt)
            eta = tEmul.L1Tau_hweta.at(i)
            hEmul_eta.Fill(eta)
            phi = tEmul.L1Tau_hwphi.at(i)
            hEmul_phi.Fill(phi)


    c1 = TCanvas ("c1", "c1", 800, 600)
    pad1 = TPad ("pad1", "pad1", 0, 0.251, 1, 1.0)
    pad1.SetFrameLineWidth(3)
    pad1.SetLeftMargin(0.15)
    pad1.SetBottomMargin(0.02)
    pad1.SetTopMargin(0.1)
    pad1.Draw()

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
    raw_input()

