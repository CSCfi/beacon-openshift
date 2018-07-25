var app = angular.module('myApp.view2', ['siyfion.sfTypeahead']);

app.controller('View2Ctrl', function($scope) {
  
  $scope.selectedItem = null;
  
  // instantiate the bloodhound suggestion engine
  var items = new Bloodhound({
    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.item); },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: [
	{item:'A2M'},
	{item:'ABL1'},
	{item:'ADCY5'},
	{item:'AGPAT2'},
	{item:'AGTR1'},
	{item:'AIFM1'},
	{item:'AKT1'},
	{item:'APEX1'},
	{item:'APOC3'},
	{item:'APOE'},
	{item:'APP'},
	{item:'APTX'},
	{item:'AR'},
	{item:'ARHGAP1'},
	{item:'ARNTL'},
	{item:'ATF2'},
	{item:'ATM'},
	{item:'ATP5O'},
	{item:'ATR'},
	{item:'BAK1'},
	{item:'BAX'},
	{item:'BCL2'},
	{item:'BDNF'},
	{item:'BLM'},
	{item:'BMI1'},
	{item:'BRCA1'},
	{item:'BRCA2'},
	{item:'BSCL2'},
	{item:'BUB1B'},
	{item:'BUB3'},
	{item:'C1QA'},
	{item:'CACNA1A'},
	{item:'CAT'},
	{item:'CCNA2'},
	{item:'CDC42'},
	{item:'CDK1'},
	{item:'CDK7'},
	{item:'CDKN1A'},
	{item:'CDKN2A'},
	{item:'CDKN2B'},
	{item:'CEBPA'},
	{item:'CEBPB'},
	{item:'CETP'},
	{item:'CHEK2'},
	{item:'CISD2'},
	{item:'CLOCK'},
	{item:'CLU'},
	{item:'CNR1'},
	{item:'COQ7'},
	{item:'CREB1'},
	{item:'CREBBP'},
	{item:'CSNK1E'},
	{item:'CTF1'},
	{item:'CTGF'},
	{item:'CTNNB1'},
	{item:'DBN1'},
	{item:'DDIT3'},
	{item:'DGAT1'},
	{item:'DLL3'},
	{item:'E2F1'},
	{item:'EEF1A1'},
	{item:'EEF1E1'},
	{item:'EEF2'},
	{item:'EFEMP1'},
	{item:'EGF'},
	{item:'EGFR'},
	{item:'EGR1'},
	{item:'EIF5A2'},
	{item:'ELN'},
	{item:'EMD'},
	{item:'EP300'},
	{item:'EPOR'},
	{item:'EPS8'},
	{item:'ERBB2'},
	{item:'ERCC1'},
	{item:'ERCC2'},
	{item:'ERCC3'},
	{item:'ERCC4'},
	{item:'ERCC5'},
	{item:'ERCC6'},
	{item:'ERCC8'},
	{item:'ESR1'},
	{item:'FAS'},
	{item:'FEN1'},
	{item:'FGF21'},
	{item:'FGF23'},
	{item:'FGFR1'},
	{item:'FLT1'},
	{item:'FOS'},
	{item:'FOXM1'},
	{item:'FOXO1'},
	{item:'FOXO3'},
	{item:'FOXO4'},
	{item:'GCLC'},
	{item:'GCLM'},
	{item:'GDF11'},
	{item:'GH1'},
	{item:'GHR'},
	{item:'GHRH'},
	{item:'GHRHR'},
	{item:'GPX1'},
	{item:'GPX4'},
	{item:'GRB2'},
	{item:'GRN'},
	{item:'GSK3A'},
	{item:'GSK3B'},
	{item:'GSR'},
	{item:'GSS'},
	{item:'GSTA4'},
	{item:'GSTP1'},
	{item:'GTF2H2'},
	{item:'H2AFX'},
	{item:'HBP1'},
	{item:'HDAC1'},
	{item:'HDAC2'},
	{item:'HDAC3'},
	{item:'HELLS'},
	{item:'HESX1'},
	{item:'HIC1'},
	{item:'HIF1A'},
	{item:'HMGB1'},
	{item:'HMGB2'},
	{item:'HOXB7'},
	{item:'HOXC4'},
	{item:'HRAS'},
	{item:'HSF1'},
	{item:'HSP90AA1'},
	{item:'HSPA1A'},
	{item:'HSPA1B'},
	{item:'HSPA8'},
	{item:'HSPA9'},
	{item:'HSPD1'},
	{item:'HTRA2'},
	{item:'HTT'},
	{item:'IFNB1'},
	{item:'IGF1'},
	{item:'IGF1R'},
	{item:'IGF2'},
	{item:'IGFBP2'},
	{item:'IGFBP3'},
	{item:'IKBKB'},
	{item:'IL2'},
	{item:'IL2RG'},
	{item:'IL6'},
	{item:'IL7'},
	{item:'IL7R'},
	{item:'INS'},
	{item:'INSR'},
	{item:'IRS1'},
	{item:'IRS2'},
	{item:'JAK2'},
	{item:'JUN'},
	{item:'JUND'},
	{item:'KCNA3'},
	{item:'KL'},
	{item:'LEP'},
	{item:'LEPR'},
	{item:'LMNA'},
	{item:'LMNB1'},
	{item:'LRP2'},
	{item:'MAP3K5'},
	{item:'MAPK14'},
	{item:'MAPK3'},
	{item:'MAPK8'},
	{item:'MAPK9'},
	{item:'MAPT'},
	{item:'MAX'},
	{item:'MDM2'},
	{item:'MED1'},
	{item:'MIF'},
	{item:'MLH1'},
	{item:'MSRA'},
	{item:'MT-CO1'},
	{item:'MT1E'},
	{item:'MTOR'},
	{item:'MXD1'},
	{item:'MXI1'},
	{item:'MYC'},
	{item:'NBN'},
	{item:'NCOR1'},
	{item:'NCOR2'},
	{item:'NFE2L1'},
	{item:'NFE2L2'},
	{item:'NFKB1'},
	{item:'NFKB2'},
	{item:'NFKBIA'},
	{item:'NGF'},
	{item:'NGFR'},
	{item:'NOG'},
	{item:'NR3C1'},
	{item:'NRG1'},
	{item:'NUDT1'},
	{item:'PAPPA'},
	{item:'PARP1'},
	{item:'PCK1'},
	{item:'PCMT1'},
	{item:'PCNA'},
	{item:'PDGFB'},
	{item:'PDGFRA'},
	{item:'PDGFRB'},
	{item:'PDPK1'},
	{item:'PEX5'},
	{item:'PIK3CA'},
	{item:'PIK3CB'},
	{item:'PIK3R1'},
	{item:'PIN1'},
	{item:'PLAU'},
	{item:'PLCG2'},
	{item:'PMCH'},
	{item:'PML'},
	{item:'POLA1'},
	{item:'POLB'},
	{item:'POLD1'},
	{item:'POLG'},
	{item:'PON1'},
	{item:'POU1F1'},
	{item:'PPARA'},
	{item:'PPARG'},
	{item:'PPARGC1A'},
	{item:'PPM1D'},
	{item:'PPP1CA'},
	{item:'PRDX1'},
	{item:'PRKCA'},
	{item:'PRKCD'},
	{item:'PRKDC'},
	{item:'PROP1'},
	{item:'PSEN1'},
	{item:'PTEN'},
	{item:'PTGS2'},
	{item:'PTK2'},
	{item:'PTK2B'},
	{item:'PTPN1'},
	{item:'PTPN11'},
	{item:'PYCR1'},
	{item:'RAD51'},
	{item:'RAD52'},
	{item:'RAE1'},
	{item:'RB1'},
	{item:'RECQL4'},
	{item:'RELA'},
	{item:'RET'},
	{item:'RGN'},
	{item:'RICTOR'},
	{item:'RPA1'},
	{item:'S100B'},
	{item:'SDHC'},
	{item:'SERPINE1'},
	{item:'SHC1'},
	{item:'SIN3A'},
	{item:'SIRT1'},
	{item:'SIRT3'},
	{item:'SIRT6'},
	{item:'SIRT7'},
	{item:'SLC13A1'},
	{item:'SNCG'},
	{item:'SOCS2'},
	{item:'SOD1'},
	{item:'SOD2'},
	{item:'SP1'},
	{item:'SPRTN'},
	{item:'SQSTM1'},
	{item:'SST'},
	{item:'SSTR3'},
	{item:'STAT3'},
	{item:'STAT5A'},
	{item:'STAT5B'},
	{item:'STK11'},
	{item:'STUB1'},
	{item:'SUMO1'},
	{item:'SUN1'},
	{item:'TAF1'},
	{item:'TBP'},
	{item:'TCF3'},
	{item:'TERC'},
	{item:'TERF1'},
	{item:'TERF2'},
	{item:'TERT'},
	{item:'TFAP2A'},
	{item:'TFDP1'},
	{item:'TGFB1'},
	{item:'TNF'},
	{item:'TOP1'},
	{item:'TOP2A'},
	{item:'TOP2B'},
	{item:'TOP3B'},
	{item:'TP53'},
	{item:'TP53BP1'},
	{item:'TP63'},
	{item:'TP73'},
	{item:'TPP2'},
	{item:'TRAP1'},
	{item:'TRPV1'},
	{item:'TXN'},
	{item:'UBB'},
	{item:'UBE2I'},
	{item:'UCHL1'},
	{item:'UCP1'},
	{item:'UCP2'},
	{item:'UCP3'},
	{item:'VCP'},
	{item:'VEGFA'},
	{item:'WRN'},
	{item:'XPA'},
	{item:'XRCC5'},
	{item:'XRCC6'},
	{item:'YWHAZ'},
	{item:'ZMPSTE24'},
	{item:'1p36 deletion syndrome'},
	{item:'18p deletion syndrome'},
	{item:'21-hydroxylase deficiency'},
	{item:'Alpha 1-antitrypsin deficiency'},
	{item:'AAA syndrome (achalasia-addisonianism-alacrima)'},
	{item:'Aarskog–Scott syndrome'},
	{item:'ABCD syndrome'},
	{item:'Aceruloplasminemia'},
	{item:'Acheiropodia'},
	{item:'Achondrogenesis type II'},
	{item:'achondroplasia'},
	{item:'Acute intermittent porphyria'},
	{item:'adenylosuccinate lyase deficiency'},
	{item:'Adrenoleukodystrophy'},
	{item:'Alagille syndrome'},
	{item:'ADULT syndrome'},
	{item:'Albinism'},
	{item:'Alexander disease'},
	{item:'alkaptonuria'},
	{item:'Alport syndrome'},
	{item:'Alternating hemiplegia of childhood'},
	{item:'Amyotrophic lateral sclerosis'},
	{item:'Alström syndrome'},
	{item:'Alzheimer\'s disease'},
	{item:'Amelogenesis imperfecta'},
	{item:'Aminolevulinic acid dehydratase deficiency porphyria'},
	{item:'Androgen insensitivity syndrome'},
	{item:'Angelman syndrome'},
	{item:'Apert Syndrome'},
	{item:'Arthrogryposis–renal dysfunction–cholestasis syndrome'},
	{item:'Ataxia telangiectasia'},
	{item:'Axenfeld syndrome'},
	{item:'Beare-Stevenson cutis gyrata syndrome'},
	{item:'Beckwith–Wiedemann syndrome'},
	{item:'Benjamin syndrome'},
	{item:'biotinidase deficiency'},
	{item:'Björnstad syndrome'},
	{item:'Bloom syndrome'},
	{item:'Birt–Hogg–Dubé syndrome'},
	{item:'Brody myopathy'},
	{item:'Brunner syndrome'},
	{item:'CADASIL syndrome'},
	{item:'CARASIL syndrome'},
	{item:'Chronic granulomatous disorder'},
	{item:'Campomelic dysplasia'},
	{item:'Canavan disease'},
	{item:'Carpenter Syndrome'},
	{item:'Cerebral dysgenesis–neuropathy–ichthyosis–keratoderma syndrome(SEDNIK)'},
	{item:'Cystic fibrosis'},
	{item:'Charcot–Marie–Tooth disease'},
	{item:'CHARGE syndrome'},
	{item:'Chédiak–Higashi syndrome'},
	{item:'Cleidocranial dysostosis'},
	{item:'Cockayne syndrome'},
	{item:'Coffin–Lowry syndrome'},
	{item:'Cohen syndrome'},
	{item:'collagenopathy, types II and XI'},
	{item:'Congenital insensitivity to pain with anhidrosis (CIPA)'},
	{item:'Cowden syndrome'},
	{item:'CPO deficiency (coproporphyria)'},
	{item:'Cranio–lenticulo–sutural dysplasia'},
	{item:'Cri du chat'},
	{item:'Crohn\'s disease'},
	{item:'Crouzon syndrome'},
	{item:'Crouzonodermoskeletal syndrome(Crouzon syndrome with acanthosis nigricans)'},
	{item:'Darier\'s disease'},
	{item:'Dent\'s disease (Genetic hypercalciuria)'},
	{item:'Denys–Drash syndrome'},
	{item:'De Grouchy syndrome'},
	{item:'Di George\'s syndrome'},
	{item:'Distal hereditary motor neuropathies, multiple types'},
	{item:'Ehlers–Danlos syndrome'},
	{item:'Emery–Dreifuss syndrome'},
	{item:'Erythropoietic protoporphyria'},
	{item:'Fanconi anemia (FA)'},
	{item:'Fabry disease'},
	{item:'factor V Leiden thrombophilia'},
	{item:'familial adenomatous polyposis'},
	{item:'familial dysautonomia'},
	{item:'Feingold syndrome'},
	{item:'FG syndrome'},
	{item:'Friedreich\'s ataxia'},
	{item:'G6PD deficiency'},
	{item:'galactosemia'},
	{item:'Gaucher disease'},
	{item:'Gillespie syndrome'},
	{item:'Glutaric aciduria, type I and type 2'},
	{item:'GRACILE syndrome'},
	{item:'Griscelli syndrome'},
	{item:'Hailey-Hailey disease'},
	{item:'Harlequin type ichthyosis'},
	{item:'Hemochromatosis, hereditary'},
	{item:'hemophilia'},
	{item:'Hepatoerythropoietic porphyria'},
	{item:'Hereditary coproporphyria'},
	{item:'Hereditary hemorrhagic telangiectasia (Osler–Weber–Rendu syndrome)'},
	{item:'Hereditary Inclusion Body Myopathy'},
	{item:'Hereditary multiple exostoses'},
	{item:'Hereditary spastic paraplegia(infantile-onset ascending hereditary spastic paralysis)'},
	{item:'Hermansky–Pudlak syndrome'},
	{item:'Hereditary neuropathy with liability to pressure palsies (HNPP)'},
	{item:'Heterotaxy'},
	{item:'homocystinuria'},
	{item:'Huntington\'s disease'},
	{item:'Hunter syndrome'},
	{item:'Hurler syndrome'},
	{item:'Hutchinson-Gilford progeria syndrome'},
	{item:'Hyperlysinemia'},
	{item:'hyperoxaluria, primary'},
	{item:'hyperphenylalaninemia'},
	{item:'Hypoalphalipoproteinemia (Tangier disease)'},
	{item:'Hypochondrogenesis'},
	{item:'Hypochondroplasia'},
	{item:'Immunodeficiency, centromere instability and facial anomalies syndrome (ICF syndrome)'},
	{item:'Incontinentia pigmenti'},
	{item:'Ischiopatellar dysplasia'},
	{item:'Isodicentric 15'},
	{item:'Jackson–Weiss syndrome'},
	{item:'Joubert syndrome'},
	{item:'Juvenile Primary Lateral Sclerosis(JPLS)'},
	{item:'Keloid disorder'},
	{item:'Kniest dysplasia'},
	{item:'Kosaki overgrowth syndrome'},
	{item:'Krabbe disease'},
	{item:'Kufor–Rakeb syndrome'},
	{item:'LCAT deficiency'},
	{item:'Lesch-Nyhan syndrome'},
	{item:'Li-Fraumeni syndrome'},
	{item:'Lynch Syndrome'},
	{item:'lipoprotein lipase deficiency'},
	{item:'Maple syrup urine disease'},
	{item:'Marfan syndrome'},
	{item:'Maroteaux–Lamy syndrome'},
	{item:'McCune–Albright syndrome'},
	{item:'McLeod syndrome'},
	{item:'MEDNIK syndrome'},
	{item:'Mediterranean fever, familial'},
	{item:'Menkes disease'},
	{item:'Methemoglobinemia'},
	{item:'methylmalonic acidemia'},
	{item:'Micro syndrome'},
	{item:'Microcephaly'},
	{item:'Morquio syndrome'},
	{item:'Mowat-Wilson syndrome'},
	{item:'Muenke syndrome'},
	{item:'Multiple endocrine neoplasia type 1(Wermer\'s syndrome)'},
	{item:'Multiple endocrine neoplasia type 2'},
	{item:'Muscular dystrophy'},
	{item:'Muscular dystrophy, Duchenne and Becker type'},
	{item:'Myostatin-related muscle hypertrophy'},
	{item:'myotonic dystrophy'},
	{item:'Natowicz syndrome'},
	{item:'Neurofibromatosis type I'},
	{item:'Neurofibromatosis type II'},
	{item:'Niemann–Pick disease'},
	{item:'Nonketotic hyperglycinemia'},
	{item:'Nonsyndromic deafness'},
	{item:'Noonan syndrome'},
	{item:'Norman–Roberts syndrome'},
	{item:'Ogden syndrome'},
	{item:'Omenn syndrome'},
	{item:'osteogenesis imperfecta'},
	{item:'Pantothenate kinase-associated neurodegeneration'},
	{item:'Patau Syndrome (Trisomy 13)'},
	{item:'PCC deficiency (propionic acidemia)'},
	{item:'Porphyria cutanea tarda (PCT)'},
	{item:'Pendred syndrome'},
	{item:'Peutz-Jeghers syndrome'},
	{item:'Pfeiffer syndrome'},
	{item:'phenylketonuria'},
	{item:'Pipecolic acidemia'},
	{item:'Pitt–Hopkins syndrome'},
	{item:'Polycystic kidney disease'},
	{item:'Polycystic Ovarian Syndrome(PCOS)'},
	{item:'porphyria'},
	{item:'Prader-Willi syndrome'},
	{item:'Primary ciliary dyskinesia (PCD)'},
	{item:'primary pulmonary hypertension'},
	{item:'protein C deficiency'},
	{item:'protein S deficiency'},
	{item:'Pseudo-Gaucher disease'},
	{item:'Pseudoxanthoma elasticum'},
	{item:'Retinitis pigmentosa'},
	{item:'Rett syndrome'},
	{item:'Roberts syndrome'},
	{item:'Rubinstein-Taybi syndrome (RSTS)'},
	{item:'Sandhoff disease'},
	{item:'Sanfilippo syndrome'},
	{item:'Schwartz–Jampel syndrome'},
	{item:'spondyloepiphyseal dysplasia congenita (SED)'},
	{item:'Shprintzen–Goldberg syndrome'},
	{item:'sickle cell anemia'},
	{item:'Siderius X-linked mental retardation syndrome'},
	{item:'Sideroblastic anemia'},
	{item:'Sly syndrome'},
	{item:'Smith-Lemli-Opitz syndrome'},
	{item:'Smith Magenis Syndrome'},
	{item:'Spinal muscular atrophy'},
	{item:'Spinocerebellar ataxia (types 1-29)'},
	{item:'SSB syndrome (SADDAN)'},
	{item:'Stargardt disease (macular degeneration)'},
	{item:'Stickler syndrome (multiple forms)'},
	{item:'Strudwick syndrome (spondyloepimetaphyseal dysplasia, Strudwick type)'},
	{item:'Tay-Sachs disease'},
	{item:'Tetrahydrobiopterin deficiency'},
	{item:'Thanatophoric dysplasia'},
	{item:'Treacher Collins syndrome'},
	{item:'Tuberous Sclerosis Complex (TSC)'},
	{item:'Turner syndrome'},
	{item:'Usher syndrome'},
	{item:'Variegate porphyria'},
	{item:'von Hippel-Lindau disease'},
	{item:'Waardenburg syndrome'},
	{item:'Weissenbacher-Zweymüller syndrome'},
	{item:'Williams Syndrome'},
	{item:'Wilson disease'},
	{item:'Woodhouse–Sakati syndrome'},
	{item:'Wolf–Hirschhorn syndrome'},
	{item:'Xeroderma pigmentosum'},
	{item:'X-linked mental retardation and macroorchidism (fragile X syndrome)'},
	{item:'X-linked spinal-bulbar muscle atrophy (spinal and bulbar muscular atrophy)'},
	{item:'Xp11.22 deletion'},
	{item:'X-linked severe combined immunodeficiency (X-SCID)'},
	{item:'X-linked sideroblastic anemia(XLSA)'},
	{item:'XXX (triple X syndrome)'},
	{item:'XXXX syndrome (48, XXXX)'},
	{item:'XXXXX syndrome (49, XXXXX)'},
	{item:'XYY syndrome (47,XYY)'},
	{item:'Zellweger syndrome'}
    ]
  });

   
  // initialize the bloodhound suggestion engine
  items.initialize();

  $scope.itemsDataset = {
	limit: 5,
    displayKey: 'item',
    source: items.ttAdapter(),
    templates: {
      empty: [
        '<div class="tt-suggestion tt-empty-message">',
        'No results were found ...',
        '</div>'
      ].join('\n'),
    }
  };
  
  // Typeahead options object
  $scope.exampleOptions = {
    displayKey: 'title'
  };
  
});