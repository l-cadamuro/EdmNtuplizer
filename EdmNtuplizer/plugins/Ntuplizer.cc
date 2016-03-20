/** \class Ntuplizer
 *
 *  Ntuplizer for EDM output of L1 unpacker - emulator.
 *
 *  $Date: 2016/03/18 $
 *  $Revision: 1.00 $
 *  \author L. Cadamuro (LLR)
 */

#include <cmath>
#include <vector>
#include <algorithm>
#include <string>
#include <map>
#include <utility>
#include <TNtuple.h>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include <FWCore/Framework/interface/ESHandle.h>
#include <FWCore/Framework/interface/LuminosityBlock.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/Common/interface/TriggerNames.h>
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/L1Trigger/interface/Tau.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/L1Trigger/interface/EtSum.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

using namespace std;

class Ntuplizer : public edm::EDAnalyzer {
 public:
  /// Constructor
  explicit Ntuplizer(const edm::ParameterSet&);
    
  /// Destructor
  virtual ~Ntuplizer();  

 private:
  //----edm control---
  virtual void beginJob() ;
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  // virtual void beginRun(edm::Run const&, edm::EventSetup const&);
  // virtual void endRun(edm::Run const&, edm::EventSetup const&);
  // virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
  // virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

  void Initialize(); 

  TTree *myTree;
  edm::EDGetTokenT<l1t::TauBxCollection>          _L1TauTag  ;
  // edm::EDGetTokenT<l1t::CaloTowerBxCollection>    _L1TTTag   ;
  // edm::EDGetTokenT<l1t::CaloClusterBxCollection>  _L1ClusTag ;

  // -------------------------------------
  // variables to be filled in output tree
  ULong64_t       _indexevents;
  Int_t           _runNumber;
  Int_t           _lumi;

  // tau L1 quantities
  vector<Int_t>   _L1Tau_hwpt;
  vector<Int_t>   _L1Tau_hweta;
  vector<Int_t>   _L1Tau_hwphi;
  vector<Int_t>   _L1Tau_hwiso;
  vector<Int_t>   _L1Tau_hwqual;

  // TT quantities
  vector<Int_t>   _L1TT_hwpt;
  vector<Int_t>   _L1TT_hweta;
  vector<Int_t>   _L1TT_hwphi;
  vector<Int_t>   _L1TT_hwiso;
  vector<Int_t>   _L1TT_hwqual;

  // cluster quantities
  vector<Int_t>   _L1clus_hwpt;
  vector<Int_t>   _L1clus_hweta;
  vector<Int_t>   _L1clus_hwphi;
  vector<Int_t>   _L1clus_hwiso;
  vector<Int_t>   _L1clus_hwqual;

};

// ----Constructor and Destructor -----
Ntuplizer::Ntuplizer(const edm::ParameterSet& pset) : 
  _L1TauTag         (consumes<l1t::TauBxCollection>         (pset.getParameter<edm::InputTag>("L1Tau")))
  // _L1TTTag          (consumes<l1t::CaloTowerBxCollection>   (pset.getParameter<edm::InputTag>("L1TT"))),
  // _L1ClusTag        (consumes<l1t::CaloClusterBxCollection> (pset.getParameter<edm::InputTag>("L1Clusters")))
{
    Initialize();
}

Ntuplizer::~Ntuplizer()
{}

void Ntuplizer::Initialize()
{
    _indexevents=0;
    _runNumber=0;
    _lumi=0;

    _L1Tau_hwpt.clear();
    _L1Tau_hweta.clear();
    _L1Tau_hwphi.clear();
    _L1Tau_hwiso.clear();
    _L1Tau_hwqual.clear();

    _L1TT_hwpt.clear();
    _L1TT_hweta.clear();
    _L1TT_hwphi.clear();
    _L1TT_hwiso.clear();
    _L1TT_hwqual.clear();

    _L1clus_hwpt.clear();
    _L1clus_hweta.clear();
    _L1clus_hwphi.clear();
    _L1clus_hwiso.clear();
    _L1clus_hwqual.clear();
}


void Ntuplizer::beginJob()
{
    edm::Service<TFileService> fs;
    myTree = fs->make<TTree>("L1EdmTree","L1EdmTree"); // FIXME: set name from input tag
    
    //Branches
    myTree->Branch("EventNumber",&_indexevents,"EventNumber/l");
    myTree->Branch("RunNumber",&_runNumber,"RunNumber/I");
    myTree->Branch("lumi",&_lumi,"lumi/I");
    
    myTree->Branch("L1Tau_hwpt", &_L1Tau_hwpt);
    myTree->Branch("L1Tau_hweta", &_L1Tau_hweta);
    myTree->Branch("L1Tau_hwphi", &_L1Tau_hwphi);
    myTree->Branch("L1Tau_hwiso", &_L1Tau_hwiso);
    myTree->Branch("L1Tau_hwqual", &_L1Tau_hwqual);

    myTree->Branch("L1TT_hwpt", &_L1TT_hwpt);
    myTree->Branch("L1TT_hweta", &_L1TT_hweta);
    myTree->Branch("L1TT_hwphi", &_L1TT_hwphi);
    myTree->Branch("L1TT_hwiso", &_L1TT_hwiso);
    myTree->Branch("L1TT_hwqual", &_L1TT_hwqual);

    myTree->Branch("L1clus_hwpt", &_L1clus_hwpt);
    myTree->Branch("L1clus_hweta", &_L1clus_hweta);
    myTree->Branch("L1clus_hwphi", &_L1clus_hwphi);
    myTree->Branch("L1clus_hwiso", &_L1clus_hwiso);
    myTree->Branch("L1clus_hwqual", &_L1clus_hwqual);
}

void Ntuplizer::endJob()
{}


// ----Analyzer (main) ----
// ------------ method called for each event  ------------
void Ntuplizer::analyze(const edm::Event& event, const edm::EventSetup& eSetup)
{
    Initialize();

    _indexevents = event.id().event();
    _runNumber = event.id().run();
    _lumi = event.luminosityBlock();

    // fill all taus
    edm::Handle<l1t::TauBxCollection>  L1TauHandle;
    event.getByToken(_L1TauTag, L1TauHandle);

    if (L1TauHandle.isValid())
    {
        for (l1t::TauBxCollection::const_iterator it = L1TauHandle->begin(0); it != L1TauHandle->end(0) ; it++)
        {
            _L1Tau_hwpt.push_back(it->hwPt());
            _L1Tau_hweta.push_back(it->hwEta());
            _L1Tau_hwphi.push_back(it->hwPhi());
            _L1Tau_hwiso.push_back(it->hwIso());
            _L1Tau_hwqual.push_back(it->hwQual());
        }
    }
    else
        edm::LogWarning("MissingProduct") << "L1Upgrade Tau not found. Branch will not be filled" << std::endl; 

    // finally, fill tree
    myTree->Fill();

}

//define this as a plug-in
DEFINE_FWK_MODULE(Ntuplizer);
