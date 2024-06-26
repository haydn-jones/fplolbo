import numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
import torch

DRUGS = [
    "CC(Nc1nc(-c2cnccn2)nc(Cl)c1-c1c(F)cc(F)cc1F)C(F)(F)F",
    "O=C(c1c[nH]cn1)c1nccc2c1[nH]c1ccccc12",
    "Cc1ccc(Sc2nc(-c3ccccc3)ccc2C#N)cc1",
    "CS(=O)(=O)c1ccc(Cc2nnc3n2N=C(c2ccc(O)c(C(N)=O)c2)CS3)cc1",
    "N#Cc1cnc2ccc(NCCN3CCOCC3)cc2c1Sc1ccc(F)c(Cl)c1",
    "COCC1CCN(C(C(=O)O)c2c(F)cccc2OC(C)C)CC1",
    "C[S+](O)c1ccccc1-c1nnc(N=C(N)N)s1",
    "CS(=O)(=O)NCCc1cc(-c2ccnc3[nH]nc(C(F)(F)F)c23)cc(C2(C#N)CC2)c1",
    "CC(C)(C)NC(=O)C1Cc2c(sc3ccccc23)CN1",
    "COc1ccc(CCNC(=O)c2c(O)nc3ccccc3c2O)cc1OC",
    "CC1(C)CCC2(C(=O)NC(Cc3ccccc3)C(=O)O)CCC3(C)C(=CCC4C5(C)Cc6c([nH]c7ccc(Cl)cc67)C(C)(C)C5CCC43C)C2C1",
    "COc1cccc2c(NN=Cc3cccc4ccccc34)cc(C)nc12",
    "CCc1ccc(OC)c(C(OC)c2ccc(Cl)cc2)c1",
    "N=C(NC1CCCCCCC1)c1ccc(N2CCN(c3ccc(C(=N)NC4CCCCCCC4)cc3)CC2)cc1",
    "CCOCC1CN(S(=O)(=O)CC)Cc2nn(C)cc21",
    "NC(=O)c1cc(-c2cnc(C3CC3)s2)c2ccc(CN3CCOC(C(F)(F)F)C3)cc2n1",
    "O=C1N=C(N2N=C(c3ccccc3)CC2c2ccccc2O)C(=Cc2ccc(O)cc2)S1",
    "CC(CO)Nc1cc(-n2ncc3cc(C#N)cnc32)ncc1C(O)=NCCC1CC1",
    "O=C(O)CC(c1ccccc1Cl)n1ccc2cc(OCCc3ccc4c(n3)NCCC4)ccc21",
    "CCc1ccc(NC(=O)Cc2c(C(=O)O)n(C)c3ccccc23)cc1",
    "Cc1cc(C)nc(NC(=C(C#N)C#N)N2CCN(c3cccc(C(F)(F)F)c3)CC2)c1",
    "Cc1cc(OCCCc2c(C(=O)NS(=O)(=O)CCNC(=O)Cc3cn(C)c4ccccc34)[nH]c3ccccc23)cc(C)c1Cl",
    "CCCn1c(=O)c2c(nc(C=Cc3cccc(Cl)c3)n2C)n(C)c1=O",
    "Nc1nonc1C(=O)NN=Cc1ccncc1",
    "CC(C)n1c(=O)c(C(=O)NC2CC3CCC(C2)N3CCCN2CCN(S(C)(=O)=O)CC2)cc2ccccc21",
    "O=C(CNC(=O)c1coc(-c2ccccc2)n1)NC(Cc1ccccc1)C(=O)NC(Cc1c[nH]cn1)C(=O)O",
    "NS(=O)(=O)c1ccc(Oc2cnc3ccc(=O)n(CCN4CCC(c5nc6cc(Cl)ccc6[nH]5)CC4)c3c2)cc1",
    "CCCCOc1ccc(C(=O)NN=C(C)C2(O)Cc3c(O)c4c(c(O)c3C(OC3CC(N)C(O)C(C)O3)C2)C(=O)c2c(OC)cccc2C4=O)cc1",
    "Oc1ccc(-c2cc(-c3ccccc3Cl)no2)cc1",
    "Cc1ccc(NC(=O)c2cc(F)cc(C#N)c2)cc1",
    "O=C1NC(=O)C(c2ccc(Oc3ccccc3)cc2)(N2CCCN(C(=O)CCC3CCCC3)CC2)C(=O)N1",
    "CCN1CCN(Cc2ccc(NC(=O)c3ccc(C)c(C#Cc4cnc5cccnn45)c3)cc2C(F)(F)F)CC1",
    "CC1CCN(CCCOc2ccc(=O)n(-c3ccc(Cl)c(Cl)c3)n2)CC1",
    "N#Cc1ccc(C2C3=C(CCC3=O)N(c3cccc(C(F)(F)F)c3)C(=O)N2C(O)=NCCCO)cc1",
    "COCc1cn(C2OC(CO)C(O)C2O)c(=O)nc1N",
    "Cc1ccc(S(=O)(=O)N2CCCC2C(=O)O)cc1",
    "CCCN(CCC)CC(O)COc1ccc([N+](=O)[O-])cc1",
    "CCc1nc2c(C)cc(C)nc2n1Cc1ccc(C(C(C)C)C(C)C(=O)O)cc1",
    "COc1ccc(C(=O)c2cc(O)c3c(c2)Cc2cccc(O)c2C3=O)cc1",
    "CN1CCCC1C=C1CCCC(=CC2CCCN2C)C1=O",
    "CC(C)N(CCNC(=O)CN1CCCC1=O)C(C)C",
    "COc1ccccc1CNC(=NO)c1ccc(C)nc1Oc1ccc2ccccc2c1",
    "Cc1ccc(-c2nnc(-c3cccc(NC(=O)CCCCO)c3)o2)cc1",
    "COC(=O)C(O)C1OC(=O)C(c2ccc([N+](=O)[O-])cc2)=C1O",
    "CC12CC(CCCC(F)(F)C(F)(F)C(F)(F)C(F)(F)CC[S+]([O-])CCCC(F)(F)C(F)(F)F)C3c4ccc(O)cc4CCC3C1CCC2O",
    "CC(C)(C)c1cnc(CSc2cnc(NC(=O)CCCC(=O)NO)s2)o1",
    "CC(C)=CCc1cc(O)ccc1O",
    "CC(C)(C)c1ccc2c(c1)C(=O)c1ccc(C3=NCCN3)cc1S2(=O)=O",
    "CCCN(C(=O)c1cc2c(s1)-c1ccccc1OC2)c1ccc(C(C)C)cc1",
    "Cn1c(CCC(=O)Nc2ccc(N3CCOCC3)cc2)nc(=O)c2ccccc21",
    "O=C(COC(=O)C12CC3CC(CC(Cl)(C3)C1)C2)N1CCCCC1",
    "Cn1c(SCC(=O)NC2CCCCC2)nnc1-c1ccccc1F",
    "CCCNC(=O)c1ccc(NC(=O)N2Cc3ccc(OC)cc3C2)cc1",
    "O=C(O)c1ccccc1NC(=O)N1CCN(c2ncc3ccccc3n2)CC1",
    "CCC(=O)Nc1c2sscc-2n(C)c1=O",
    "CCCC1CC(=O)CC23CCN(CC4CC4)C(Cc4ccc(O)cc42)C13",
    "CC(C=CC(C)C1CC(O)C2C1(C)CCC1C3(C)CCC(O)C(O)C3C(O)CC12O)C(C)CO",
    "COc1ccc(-c2sc3cccc[n+]3c2S)cc1",
    "COc1cc(-c2noc(C3CC(=O)N(c4ccc5c(c4)OCCO5)C3)n2)cc(OC)c1OC",
    "CCOc1ccc(-n2nc(CO)c(C(=O)NCc3cccnc3)n2)cc1",
    "COc1ccc(CNC(=NO)c2cccnc2OCc2ccccc2)cc1",
    "O=C(OCCCC(=O)N1CCOCC1)c1ccccc1",
    "C=CCN1C2CCC1C1CCC2N1C(c1ccc(C(=O)NC2CCCCC2)cc1)c1cccc(OC)c1",
    "O=C(O)C1CCN(c2cc3cccnc3c(-c3cccc(Cl)c3)n2)CC1",
    "CCc1ccccc1-c1cccc2cc(CNCCCC(=O)O)sc12",
    "Cc1noc(C)c1CC(=O)NCc1ccnc(OCC(F)(F)F)c1",
    "CC1CCCCN1CCCNC(=O)c1cc(Sc2ccc(Cl)cc2)nc2ccccc12",
    "O=C(NCCO[N+](=O)[O-])c1ccc2ccccc2n1",
    "CCNC(=O)c1c2c(N3CCN(C)CC3)ncnc2n2ccccc12",
    "COc1ccc2[nH]c3nc(SCC(=O)Nc4nc(C(C)(C)C)cs4)nnc3c2c1",
    "CC(C)CCC(=O)C(C)CCCC1(C)OCC(CCO)CCC1O",
    "COc1ccc(NC(=O)c2ccccc2Oc2ccccc2)cc1",
    "Cc1ccc(NP(=O)(O)OP(=O)(O)OP(=O)(O)OP(=O)(O)OCC2OC(n3cnc4c(N)ncnc43)C(O)C2O)cc1",
    "CC1CCN(C(=O)c2ccc(-c3ccccc3Cl)o2)CC1",
    "COc1ccc2c(c1)C(=O)N(CC1(C#Cc3ccc(C(N)C(F)(F)F)cc3)NC(=O)NC1=O)C2",
    "C=C1C(=O)OC(CCc2ccccc2)C1CCCC",
    "Cc1cc2c(C)noc2cc1-c1ccc(C(=O)Nc2ccccc2F)s1",
    "O=C(NCC(C(=O)O)S(=O)(=O)c1c(Cl)cccc1Cl)C1=NOC2(CCC(CNc3ncc[nH]3)CC2)C1",
    "COc1cc(OC2OC(COC3OC(CO)C(O)C(O)C3O)C(O)C(O)C2O)c2c(O)c3c(=O)cc(C)oc3cc2c1",
    "CC(C)(C)OC(=O)NC(Cc1ccccc1)CC(O)C(Cc1ccccc1)NC(=O)c1cc(O)ccc1Cl",
    "Oc1cc(Cc2cccc3ccccc23)nc(SC2CCCC2)n1",
    "O=c1[nH]ncn1-c1nc(-c2ccsc2)cs1",
    "CNC(=O)c1c(-c2ccc(F)cc2)oc2nc(NCC(F)(F)F)c(-c3ccc(F)c(C(=O)NC(C)(C)c4ncon4)c3)cc12",
    "COc1ccc(-n2nc(C)c3c(-c4ccc(F)cc4)c(C=CC(O)CC(O)CC(=O)O)c(C(C)C)nc32)cc1",
    "Cc1ccccc1C(CC(=NO)c1ccncc1)c1ccc(N(C)C)cc1",
    "O=C(O)C1C(c2ccccc2)C(C(=O)N2CCOCC2)C1c1ccccc1",
    "CCOc1ccc(CCNC(=O)c2nnn(CC(=O)Nc3c(C)cc(C)cc3C)c2N)cc1OCC",
    "CCOc1nn(-c2cccc(C(F)(F)F)n2)c(C)c1Cc1ccccc1",
    "N#Cc1c(N)ncnc1N1CCC(c2nc(-c3ccc(F)c(C(F)(F)F)c3)cn2CC2CCCN2)CC1",
    "Cc1ccc(N2CCOC3CN(Cc4cnn(C)c4)CC32)nn1",
    "CN(CC(c1ccccc1)c1ccccc1)C(=O)Cc1cc(C(F)(F)F)cc(C(F)(F)F)c1",
    "Cn1cc(NC(=O)c2cc(NC(=O)c3cc(-c4sccc4C#N)cn3C)cn2C)cc1C(=O)NCCN1CCOCC1",
    "CC1(C)CC2CC(C)(CN2C(S)=Nc2ccccc2F)C1",
    "Cc1cc(N2C3CCCC2CC3)ccc1CNC(=O)Nc1cccc2[nH]ncc12",
    "O=C(COc1ccc(Cl)cc1Cl)NN=Cc1cccnc1",
    "Cc1ccc2c(c1)N(C(=O)N1CCC(C(=O)NCCc3ccc(Cl)cc3)CC1)CC(C)O2",
    "CCOc1ccc(C2CC(=O)c3c([nH]c(C(=O)OC4CCCCCC4)c3C)C2)cc1",
    "Cc1ccc(S(=O)(=O)N2CCN(C(=O)c3ccccc3)C2c2ccccc2)cc1",
    "COC(=O)c1sc2ccccc2c1NC(=O)c1cccc(Br)c1",
    "COc1ccc(C=C(C#N)C(=O)NN=C(C)c2cc3cccc(OC)c3oc2=O)cc1OC",
    "COC(=O)c1ccc(NC(=O)Cn2nc(SC)n(N)c2=S)cc1",
    "CCOC(=O)Cn1cncc1-c1ccc([N+](=O)[O-])cc1",
    "COc1ccc(CCNC(=O)c2ccc(NC(=O)CC3SC(N4CCCCC4)=NC3=O)cc2)cc1OC",
    "CC(=N)Nc1ccc(NC(C)=N)cc1",
    "CCCN(N=O)C(=O)Nc1ccc(C2CC(=O)N(C)C2=O)cc1",
    "Cn1cc(C(=O)NOc2cccc(Cl)c2)c(OCc2cccc(C(F)(F)F)c2)n1",
    "CCN(CC)c1ncnc2c1nc(Sc1ccc(Cl)cc1)n2C1OC2COP(=O)(O)OC2C1O",
    "O=C1C2=C(C3=NCCc4c[nH]c1c43)C1(C=CN2)C=C(Br)C(O)C(Br)=C1",
    "CCCCCC[P+](CCCC)(CCCC)CCCC",
    "Cc1nc(CN2CCCN(C(=O)c3cnccn3)CC2)cs1",
    "N#Cc1ccc2c(c1)C1CCCN(C(=O)c3ccc4nc[nH]c4c3)C1CC2",
    "Cc1ccc(Nc2nccc(N(C)c3ccc4c(C)n(C)nc4c3)n2)cc1S(N)(=O)=O",
    "Cc1ccccc1C(=O)N1CCC(N2CCC(n3c(=O)[nH]c4ccccc43)CC2)CC1",
    "COc1cccc(CNC2CN3CCC2CC3)c1OC",
    "COc1ccccc1-c1cccn2nc(Nc3ccc4c(c3)CCN(CCS(C)(=O)=O)CC4)nc12",
    "Clc1ccc(-c2sc(CNC3CCCC3)nc2-c2ccc(Cl)cc2Cl)cc1",
    "COc1cc2c(NC3=CC(=O)C(OCc4ccccc4)=CC3=O)ncnc2cc1OCC1CCN(C)CC1",
    "CC(C(O)=Nc1cccc(F)c1)c1ccc(OC2CCN(c3nc(N(C)C)ncc3F)C2)cc1",
    "CCOC(=O)C1C(=O)NC(SCC(=O)OC)=C(C#N)C1c1ccccc1OCC",
    "O=C(c1ncc(-c2ccccn2)o1)C1CCCC1",
    "C=CCNC(=S)N=c1ccccn1Cc1ccccc1",
    "Cn1ccc2ccc(-c3noc(-c4ccc(O)cc4)n3)cc21",
    "Cc1ccc(C(=O)O)c(N)[n+]1[O-]",
    "CC(=O)CC(=O)C=Cc1ccc(OC(C)=O)cc1",
    "Fc1cc2nc(SSC3CCCCC3)[nH]c2cc1Cl",
    "COc1ccc2nc(S(=O)(=O)c3cccc(C=CC(=O)NO)c3)ccc2c1",
    "CNC(=O)CSc1nc(-c2cc(OC)c(OC)cc2Cl)c2c(C#N)c[nH]c2n1",
    "CCCCc1nc2cc(C(=O)O)ccc2n1Cc1ccc(-c2ccccc2-c2nn[nH]n2)cc1",
    "CC(C)(C)c1cc(NC(=O)Nc2ccc(NC(=O)c3cccc(O)n3)cc2)no1",
    "COC(=O)CNC(=O)C12CCC(C)(C)CC1C1=CCC3C4(C)Cc5nc6ccccc6nc5C(C)(C)C4CCC3(C)C1(C)CC2",
    "C=C1c2ccccc2C(=O)N(C)c2ccc(N)cc21",
    "COC(=O)C1=C(c2ccc(F)cc2OCc2ccccc2)CC2CCC1N2C(=O)NCc1ccc(Br)cc1",
    "Cn1c([N+](=O)[O-])cnc1C=Cc1ccccc1Cl",
    "Cc1nnc(C2CCN(c3ccccn3)CC2)n1Cc1ccccc1",
    "CC1(N2CC(CC#N)(n3cc(-c4ncnc5[nH]ccc45)cn3)C2)CCN(C(=O)c2cccc(F)c2)CC1",
    "COc1ccc(NC(=O)CN(C)C(=O)COc2ccccc2Cc2ccccc2)cc1",
    "CCn1ncc(-c2cc(C(F)(F)F)nc(N3CCC(N)CC3)n2)c1C",
    "O=C(CC(NC(=O)c1ccccc1)c1ccccc1)Nc1cccc2ccccc12",
    "C[n+]1ccc(NC2C(=O)N3C2SC(C)(C)C3C(=O)[O-])cc1",
    "CC(=O)c1ccc2c(c1)C(NC(=O)Nc1ccccc1)C(O)C(C)(C)O2",
    "CC(C)c1nc(CN(C)C(=O)NC(C(=O)NC(Cc2ccccc2)CC(O)C(N)Cc2ccccc2)C(C)C)cs1",
    "N#CC1=C(N)N(c2nc[nH]n2)C2=C(C(=O)CCC2)C1c1ccccc1",
    "CC(C)(O)CNC(=O)c1ccc(-c2ccc3nc(C(C(=O)NCCS(N)(=O)=O)S(=O)(=O)Cc4ccc(F)cc4)sc3c2)cc1",
    "CC(=O)c1ccc(NC(=O)CN2CCCCCC2)cc1",
    "CCC(C)NC(=O)c1cccc(C)c1",
    "COc1ccccc1CC(=O)N1CCCC(n2nc(C)nc2C)C1",
    "COc1ccc(CC(=O)NN=C(C)CC(=O)NCc2ccco2)cc1OC",
    "Cc1ccc(C2=NOC(C)(c3nnc(-c4cccc(Cl)c4)o3)C2)cc1",
    "c1ccc(OCc2nn3c(-c4[nH]nc5c4CCC5)nnc3s2)cc1",
    "O=C(NN=Cc1ccc(I)cc1)c1ccncc1",
    "CCCCC(CN(O)C=O)C(=O)N1CC2(CC2)CC1C(=O)Nc1nccc(-c2cccnc2)n1",
    "CCCn1nnnc1COC(=O)C1Cc2cc(Cl)ccc2O1",
    "CCOc1ccc(CN(CCO)CCO)cc1C(=O)OC",
    "O=C(OCc1ccc(N2C(=O)CNCC2C(=O)NCc2ccccc2Cl)cc1)c1ccccc1",
    "Ic1ccc(CN2CCCCC2)cc1CN1CCCCC1",
    "N#Cc1cccc(C(=O)N2CCC(c3ccc(C(=O)NC(=N)N)cc3C(F)(F)F)CC2)c1",
    "COC(=O)c1ccc(CN2CC(c3ccc(OC)c4oc5ccccc5c34)CC2=O)c(F)c1",
    "Cc1ccc(NC(=O)N2CCCN(CCCCCNC(=O)C=Cc3ccc(Cl)c(Cl)c3)CC2)cc1",
    "COc1ccc(-c2csc(N3CCC(c4ccccc4)CC3)n2)cc1",
    "CCOC(=O)NC1=C(N2CC2C)C(=O)C(NC(=O)OCC)=C(N2CC2C)C1=O",
    "Cc1cc(NS(C)(=O)=O)ccc1-c1ccc(Oc2ccccc2)cc1",
    "CCC(Nc1c(Nc2cccc(C(=O)NC3CC3)c2O)c(=O)c1=O)c1ccccc1",
    "Cc1cc(C)c2cc(C(=O)N(C)C3CCN(C)CC3)[nH]c2c1",
    "O=C(O)c1ccnc(-c2cn(C3CCCN(C(=O)Cc4ccccc4)C3)nn2)c1",
    "CC1CN(C(=O)C=Cc2ccc3c(c2)OCO3)CC(C)O1",
    "CCn1c2ccccc2c2cc(C(=O)C(=O)Nc3ccc(OC)c(OC)c3)ccc21",
    "O=C(Cn1c2c(c(-c3cc(Cl)ccc3Cl)cc1=O)C(=O)CC2)Nc1ccc(C(=O)O)cc1",
    "CCN(C(=O)COC(=O)c1ccccc1OCc1ccc(Cl)cc1)C1CCS(=O)(=O)C1",
    "CC(C)N(C)CCC(=O)N1CCCC(c2ccc(C(=O)O)cc2)C1",
    "Cc1nn(Cc2ccccc2Cl)c(Cl)c1C(=O)OCC(=O)NCc1ccco1",
    "COc1cc(C(=O)c2ccn(-c3ccc(F)cc3)c2)cc(OC)c1OC",
    "Cc1cc(F)ccc1Nc1c(C(=O)N2CCC(c3ccccc3)CC2)cnc2c(S(=O)(=O)NC(=O)CO)cnn12",
    "COc1cc(C=C2C(=O)NC(=S)NC2=O)ccc1OCc1ccccc1Cl",
    "O=C(CSc1nc(-c2ccccc2)c(-c2ccccc2)[nH]1)Nc1ccc2c(c1)OCO2",
    "Cn1cc(-c2ccc3nc(NC(=O)c4ccc(F)cc4)cn3n2)c(-c2ccc(F)cc2)n1",
    "Cc1cccc(CC(NC(=O)C(c2ccccc2)c2ccccc2)C(=O)NC(C#N)CCCc2cccc(C(=O)O)c2)c1",
    "N=C(O)n1cc(N=C(O)N2CC(F)CC2C(O)=NCc2cncc(F)c2)c2ccccc21",
    "CCC(C(=O)Nc1cc(-c2cn3nc(OC)ccc3n2)ccc1Cl)c1ccccc1",
    "OCC1OC(c2ccc(Cl)c(Cc3nnc(-c4ccoc4)s3)c2)C(O)C(O)C1O",
    "CCC1(CCCc2cc(=O)oc3nc(C(F)F)[nH]c(=O)c23)CC1",
    "O=[N+]([O-])c1cn2c(n1)OCC(OCCOc1ccc(-c3ccc(OC(F)(F)F)cc3)cn1)C2",
    "O=[N+]([O-])c1ccc(CNCCCCCCNCCSSCCNCCCCCCNCc2ccc([N+](=O)[O-])cc2)cc1",
    "CCOc1c(-c2noc3ccc(C(C)=CC(=O)O)cc23)cc(C(C)C)cc1C(C)C",
    "CC(CNCc1coc(-c2ccc(Cl)cc2Cl)n1)c1ccccc1",
    "NS(=O)(=O)c1ccc(C(=O)NCC(=O)NC(Cc2ccc([N+](=O)[O-])cc2)C(=O)O)cc1",
    "CC1(C)c2cc(C(=O)O)ccc2C(=O)c2c1[nH]c1cc(C#N)ccc21",
    "CC=CCC=C(C)C(CCC(C)=CC=C(C)C(=O)c1c(O)cc(C(C)CCC=CNC(=O)OC)oc1=O)OC(=O)CCCCCCCCC",
    "CC(C)CC(C)NCc1ccc(C(F)(F)F)cc1",
    "CC(C)CC1C(=O)N(CC(=O)O)CC(c2ccccc2Cl)c2ccccc21",
    "CCOc1ccccc1C(=O)Nn1c(C)cc(C)cc1=O",
    "O=C(NCc1ccco1)C(=Cc1cccc(C(F)(F)F)c1)c1nc2ccccc2[nH]1",
    "CC1(CC2=Cc3ccccc3CC2)CN=CN1",
    "Cc1cccc(N(CC(=O)NCc2ccco2)C(=O)CCC(=O)Nc2nccs2)c1",
    "CC(CCCCCCCCc1ccccc1)CC1(C)CCC(O)(CC(=O)O)OO1",
    "CCCOc1ccc(N2C(=O)CC(N(C(=O)c3ccco3)c3ccc(OCCC)cc3)C2=O)cc1",
    "CNc1nc(-c2nc3cnc(N4CCN(C)CC4)cc3n2Cc2ccccc2)cn2c(C)nnc12",
    "Oc1nc2ccccc2n1C1=CCNCC1",
    "CC(C)(Cc1ccc(Oc2ccc(C(N)=O)cn2)cc1)NCC(O)COc1cccc2c1C(Cc1ccccc1)(Cc1ccccc1)C(=O)N2",
    "O=C1N(c2ccc(-c3ccccc3)cc2)CCC12CCN(Cc1ccccc1)CC2",
    "Cc1nc2c(OCC3CCCCC3)cccn2c1C(O)=NC(C)(CO)c1nnc(C(F)(F)F)o1",
    "COCCCN1C(=O)CCC2CN(Cc3ccc4nonc4c3)CCC21",
    "CC(=O)N1CCc2cc(S(=O)(=O)NC(Cc3ccccc3)C(=O)NCc3ccccc3Cl)ccc21",
    "NC(=O)c1sc2nc3c(c(-c4ccco4)c2c1N)CCCCCCCC3",
    "Cc1ccc(C)c(OCC(=O)Nc2cccc(S(=O)(=O)NC3=NCCCCC3)c2)c1",
    "COc1cccc(C=CC(=O)c2c(O)cc(OC)cc2OC)c1",
    "COc1ccc(-c2ccc3c(c2)c(C#Cc2ccsc2)c(-c2cc(OC)cc(OC)c2)n3C)cc1",
    "CN1CC(C(=O)N2CCN(c3ccc4nsnc4n3)CC2)CC2Cc3c(cccc3OCc3ccccc3)CC21",
    "CC(C)(C)c1ccc(S(=O)(=O)NC2CCC(n3cc(C(=O)N4CCCC4)nn3)CC2)cc1",
    "O=C(NCCc1cc2nc(-c3ccncc3)ccn2n1)C1CC1",
    "Cc1cccc(-c2noc(CCCC(=O)NCC3CCCO3)n2)c1",
    "CC(O)(C(=O)N1CCN(Cc2ccccc2)CC1)C(F)(F)F",
    "COc1ccc(C(=O)c2ccc(=O)n(-c3cccc(C)c3)c2)c(O)c1",
    "O=C(CN1CCOCC1)N1CCCCN2C(CO)C(c3ccc(-c4ccccc4F)cc3)C2C1",
    "O=C(Oc1cc(O)c2c(=O)c3ccccc3oc2c1)c1ccccc1Cl",
    "O=C(c1ccco1)N1CCN(c2ccc(=O)n(CCCN3CCN(c4ccccc4Cl)CC3)n2)CC1",
    "c1ccc2c(c1)nc1n2C2(N3CCOCC3)CCCC2C1N1CCOCC1",
    "CC(C)CN(c1cccc(Cl)c1)S(=O)(=O)c1ccc(-c2ccc(NS(C)(=O)=O)cc2)cc1",
    "COc1cc(C=C2SC(=Nc3ccccc3)N(C(CCCNC(=N)N)C(=O)N3CSCC3C(N)=O)C2=O)cc(OC)c1O",
    "CCCCNCCNc1ccnc2cc(Cl)ccc12",
    "Cc1cc(C(F)(F)F)n2nc(C(=O)N(Cc3cncn3Cc3cccc(F)c3)CC3CC3)cc2n1",
    "CC(=O)Nc1cccc(Cn2c(C(=O)O)c(-c3ccccc3F)c3cc(Cl)ccc32)c1",
    "c1csc(-c2ccc(-c3ncncc3-c3ccsc3)s2)c1",
    "COC(=O)c1cc2c(cc1Cl)Sc1nnc(Nc3ccccc3)n1S2(=O)=O",
    "CC(C)(C)N=C(S)NCc1ccco1",
    "Cc1cc(NC(=O)C[S+]([O-])c2cn(Cc3cccc(Cl)c3)c3ccccc23)no1",
    "CC(=O)c1ccc(Oc2c3ccccc3nc3oc4ccccc4c23)cc1",
    "CC(C)(C)c1ccc(S(=O)(=O)NC(Cc2cccc(C(=N)N)c2)C(=O)N2CCN(S(C)(=O)=O)CC2)cc1",
    "CCN(CC(=O)NCc1ccc(Cl)cc1)C(=O)CSc1cc(C)ccc1C",
    "CSc1ccccc1C(=O)Nc1ccc2c(c1)OCO2",
    "Nc1cccc(C(=O)Nc2cc(-c3ccccc3)ccc2O)c1",
    "CCCCCCCCCCCCCCCCCCNC(=O)OCC1(COP(=O)([O-])OCC[n+]2ccsc2)CCCC1",
    "COc1cc(NC(C)CCCN)c2nccc(C(OC)OC)c2c1Oc1cccc(C(F)(F)F)c1",
    "CN1CCCC1Cc1c[nH]c2ccc(C3=CCN(C(S)=NC45CC6CC(CC(C6)C4)C5)CC3)cc12",
    "Cc1cc(N2C(=O)C(O)=C(C(=O)c3ccc(F)cc3)C2c2ccc(Cl)cc2)no1",
    "Cc1ccc2[nH]c(-c3n[nH]cc3Nc3cc(Cl)nc(Sc4ccc(NC(=O)C5CC5)cc4)n3)nc2c1",
    "O=C(C1CC(=O)N(c2n[nH]c3cc(Br)ccc23)C1)N1CCSCC1",
    "CCc1ccc(NC(=O)N(CCN(C)C)C(C)c2cccnc2)cc1",
    "CN1CCN(NC(=O)c2cnn(-c3ccc(Cl)cc3Cl)c2-c2ccc(Cl)cc2)CC1",
    "O=C(Nc1nc(-c2ccccc2)nc2c1nnn2Cc1ccccc1)c1cccc(C(F)(F)F)c1",
    "CC(C)C(=O)C=C(O)C(=O)O",
    "CC(C)(C)C(=O)Oc1ccc(CC2NC(=O)COC2=O)cc1O",
    "COc1ccc(C)cc1NC(=O)OC1CC2CCCC(C1)N2CCc1ccc(N(C)C)cc1",
    "CC1CCC2C(CCC(=O)C(C)(C)C)C(=O)OC3OC4(C)CCC1C32OO4",
    "CCC=CCC=CCC=CC=CCC=CCC=CCCC(=O)NCc1ccc(O)c(OC)c1",
    "Cc1cc(C)n2nc3c(C#N)c(-c4ccccc4)cc(C(F)(F)F)c3c2n1",
    "COc1ccc(C)cc1-n1cnc2cc(C(=O)NC3CCCC3)ccc21",
    "O=C1NC(=O)c2c1c1c3cc(F)c(F)cc3[nH]c1c1c2c2cc(F)c(F)cc2n1C1OC(CO)C(O)C(O)C1O",
    "Cc1cccc(COc2ccc(C(C)NS(N)(=O)=O)cc2)c1",
    "CC(Nc1cccc(F)c1)c1cc(C(=O)N(C)C)cc2c(=O)cc(N3CCOCC3)oc12",
    "CN(C)CCON=CC1CCC2(O)CC(c3cccnc3)CCC12C",
    "C1CCC(C2OOCCCOO2)CC1",
    "COc1ccc2[nH]cc(CCN=C(S)Nc3ccc(Br)cn3)c2c1",
    "CCCCCCC(=O)CCC1(C)C2Cc3ccc(O)cc3C1(C)CCN2C",
    "COc1cc(C(=O)C=Cc2ccc(Br)cc2)cc(OC)c1OC",
    "Cn1nc(-c2ccccc2)cc1NCc1coc(-c2ccc(C(C)(C)C)cc2)n1",
    "OC1CN(Cc2ccc3c(c2)OCCO3)CCC12CCCO2",
    "Cc1ccc2ccccc2c1N1C(=O)N(c2c(C)ccc3ccccc23)C(Cc2ccccc2)C(O)C(O)C1Cc1ccccc1",
    "Sc1nnc(C(c2ccccc2)c2ccccc2)[nH]1",
    "CCc1sc(NC(=O)Cc2ccc(S(=O)(=O)CC)cc2)nc1-c1ccccc1",
    "CCC1CCCCN1CCCNC(=O)c1cn(C)c2ccc(S(=O)(=O)N(C)C3CCCCC3)cc2c1=O",
    "CC1(C)CN(C2CC3(C)C(CCC4C5CCC(C(=O)CCl)C5(C)CC(=O)C43)CC2O)CCO1",
    "Cc1cccc(CC(Nc2ccccc2)C(=O)NC(C#N)COCc2cccc(O)c2)c1",
    "CC1C(=NN2C(=O)CNC2=S)CC(c2ccccc2)NC1c1ccccc1",
    "O=C(NC(CO)c1ccccc1)c1cc(-c2ccccc2)nc2ccccc12",
    "O=C(O)C1=CC(O)C(O)C(O)C1",
    "O=C(Nc1cc(Cl)cc(Cl)c1)c1cc([N+](=O)[O-])ccc1O",
    "NC(=S)N=Nc1c(O)n(Cc2ccc(Br)cc2)c2ccccc12",
    "CN(C)c1ccc(NC(=O)Nc2ccnc3ccc(Br)cc23)cc1",
    "CN(C)CCN(C)C(=O)c1ccc(-c2nn(C)c(=NC3CCCCC3)s2)cc1",
    "CNc1nc(Nc2ccc(C(=O)N3CCOCC3)cc2O)ncc1Cl",
    "CCOc1cc(C(=O)NC(Cc2ccccc2)C(O)CNC(C)(C)c2cccc(OC)c2)cc(N2CCCS2(=O)=O)c1",
    "CCOc1ccc(CN2CCNC(=O)C2CC(=O)NCCCC2CCCC2)cc1",
    "CCN1CCN(c2ccc3c(c2)ncn3-c2ccnc(NC(C)c3ccccc3)n2)C1=O",
    "CN1CCN(c2cnc3cc(C(F)(F)F)cc(NCc4cccc(S(=O)(=O)N(C)C)c4)c3c2)CC1",
    "O=C1c2c(O)cccc2C(C(=O)Cc2ccc(Cl)c(Cl)c2)c2cccc(O)c21",
    "CCCCOc1ccccc1C(=O)CC(=O)C(=O)O",
    "COCCCNC(=O)c1c(-n2cnnn2)sc2c1CCC2",
    "O=c1c2ccccc2ncn1CCCCN1CCN(c2ccccc2)CC1",
    "CC(C=CC1CC2(CO2)CC(C)(C)O1)=CCC1CCC(NC(=O)C=CC(C)OC(=O)c2ccccc2)CC1",
    "Cc1ccc(C(=O)Nc2cc(C(C)(C)C)nn2C)cc1Oc1ncnc2cnc(N3CCOCC3)nc12",
    "Cc1nccn1C(=S)SCCCC#N",
    "CC(C)NCc1cccc(-c2ccc(NC(=O)c3ccc(C#N)cc3)cc2)c1",
    "CC1CN2c3c(cc4c(N5CCCCC5)noc4c3F)CC3(C(O)=NC(=O)N=C3O)C2C(C)O1",
    "O=C(NC(Cc1c[nH]cn1)C(=O)O)OCc1ccccc1",
    "C=C1C(=O)OC2C=C(C)C(O)CC=C(C)CC(OC(=O)C(C)=CC)C12",
    "COC(=O)CN(CCc1ccccc1)C(=O)C(C)(Cc1c[nH]c2ccccc12)NC(=O)OC1C2CC3CC(C2)CC1C3",
    "CC(C)Cc1ccc(C(C)C(=O)OCCOCCOCCOC(=O)c2cc(O)c3c(c2)C(=O)c2cccc(O)c2C3=O)cc1",
    "Cc1ccccc1C(=O)N1CCN(c2ccc(NC(=O)c3ccc4c(c3)OCCO4)cc2)CC1",
    "Clc1ccc(Cc2nnc(SCc3ccccc3)[nH]2)c(Oc2ccccc2Cl)c1",
    "CC(C=O)c1ccccc1",
    "COc1ccc(C=NNC(=O)Cn2nnc3ccccc32)cc1OC",
    "C=CCc1ccc(OCCOc2cccc3ccc(C)nc23)c(OC)c1",
    "CCC(C(=O)Nc1ccc(C(C)C)cc1)n1nc(C)n2c(cc3cc(C)ccc32)c1=O",
    "CC(C(=O)N1CCN(C(=O)c2ccc(F)cc2)CC1)n1ccnc1",
    "CNC(=S)N(CCc1ccccc1)Cc1cc2cc(OC)c(OC)cc2nc1O",
    "Cc1cc(N)n(-c2cc(C)c3ccccc3n2)n1",
    "CN1CCN(C(=O)Cc2ccc(Nc3ncc(Br)c(Nc4cc(C5CC5)n[nH]4)n3)cc2)CC1",
    "CCN(CC)c1ccc(NC(=O)c2ccccc2Br)cc1S(=O)(=O)Nc1ccccc1OC",
    "Cc1c(NC(=O)CN2C(=O)NC3(CCCC3)C2=O)c(=O)n(-c2ccccc2)n1C",
    "Cc1sc(N)c(C(=O)c2cc(C)c3ccccc3c2)c1C",
]


def smiles_to_desired_scores(smiles_list, task_id: int) -> list:
    scores = []
    targ_fp = get_fingerprint(DRUGS[task_id])
    for smiles_str in smiles_list:
        try:
            smiles_fp = get_fingerprint(smiles_str)
     
            sim = DataStructs.FingerprintSimilarity(targ_fp, smiles_fp)
            scores.append(sim)
        except:
            scores.append(float('nan'))

    return torch.tensor(scores)


def get_fingerprint(smiles: str):
    fpgen = AllChem.GetRDKitFPGenerator()
    return fpgen.GetFingerprint(Chem.MolFromSmiles(smiles))


def get_fingerprint_bitvector(smiles: str) -> np.array:
    return np.array(get_fingerprint(smiles))


def get_fingerprint_onbits(smiles: str) -> np.array:
    return get_fingerprint_bitvector(smiles).nonzero()[0]
