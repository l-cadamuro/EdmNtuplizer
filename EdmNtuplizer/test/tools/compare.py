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


if __name__ == "__main__":


    gStyle.SetOptStat(0)

    f = TFile.Open("linearized_L1Tree.root")
    t = f.Get("linearTree")

    hData_pt = TH1F ("hData_pt", "hData_pt", 256, 0, 256)
    hEmul_pt = TH1F ("hEmul_pt", "hEmul_pt", 256, 0, 256)

    hData_pt.SetMarkerStyle(8)
    hData_pt.SetMarkerSize(1)
    hData_pt.SetMarkerColor(kBlack)

    # hEmul_pt.SetLineStyle(8)
    hEmul_pt.SetLineWidth(1)
    hEmul_pt.SetLineColor(kRed)

    # events showing difference -- non merged!
    faultyEvts = [
    1955350,
    1968083,
    1980709,
    1975359,
    1985310,
    1994940,
    2006601,
    2009490,
    2009811,
    2029459,
    2040480,
    2052999,
    2055781,
    2062950,
    2073222,
    2068728,
    1437529,
    1441274,
    1448229
    ]

    for i in range (0, t.GetEntries()):
        t.GetEntry(i)
        # if t.EventNumber not in faultyEvts: continue
        # if t.EventNumber != 1968083: continue
        if t.isMerged: continue
        # if t.data_hwpt != t.emul_hwrawpt:
        #     print t.EventNumber
        hData_pt.Fill (t.data_hwpt)
        hEmul_pt.Fill (t.emul_hwrawpt)
        # print "DIFF eta, phi: " , t.emul_hweta, t.emul_hwphi , "EMUL: " , t.emul_hwrawpt , "FIRM: " , t.data_hwpt

        if t.data_hwpt != t.emul_hwrawpt:
            print "DIFF eta, phi: " , t.emul_hweta, t.emul_hwphi , "EMUL: " , t.emul_hwrawpt , "FIRM: " , t.data_hwpt

    # t.Draw("data_hwpt>>hData_pt", "!isMerged")
    # t.Draw("emul_hwrawpt>>hEmul_pt", "!isMerged")


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


    raw_input()