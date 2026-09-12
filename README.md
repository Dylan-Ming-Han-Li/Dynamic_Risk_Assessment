# Dynamic Risk Assessment

Reproducibility repository for the study:

**Microbial dechlorination reshapes halogenated antimicrobial risk in urban river sediments**

Dylan Ming-Han Li, Qi-Hong Lu, Han-Lin Cui, Hao Wang, Shu-Hao Du, Zi Zhang, Zi-Feng Zhang, Zhi-Ling Li, Shan-Quan Wang, Ai-Jie Wang, and Bin Liang

## Overview

Environmental risks of emerging contaminants are commonly inferred from concentration snapshots of parent compounds. Such assessments characterize contaminant occurrence but do not resolve how post-depositional transformation alters chemical composition and ecological risk after contaminants enter environmental reservoirs.

This repository contains the data and computational workflow developed to quantify this **transformation-mediated risk reshaping**.

The study combines sediment measurements from **140 polluted urban rivers across 64 Chinese cities** with chemical analysis, environmental and socioeconomic information, wastewater-related variables, and metagenomic profiling.

The halogenated antimicrobials triclocarban (TCC) and triclosan (TCS) were used as a tractable contaminant system. For TCC, the parent compound and its sequential reductive dechlorination products were quantified to resolve:

- contaminant occurrence and sedimentary accumulation;
- apparent dechlorination activity;
- in situ transformation extent;
- ecological risk;
- dechlorination-associated risk attenuation;
- microbial reductive dehalogenase biomarkers; and
- environmental and anthropogenic controls on contemporary contaminant risk.

The workflow further reconstructs a counterfactual scenario without in situ sedimentary dechlorination to quantify how microbial transformation modifies the risk associated with the parent–product mixture.

## Transformation system

TCC undergoes sequential reductive dechlorination in anoxic sediments:

```text
TCC
 |
 v
DCC
 |
 v
MCC
 |
 v
NCC

Abbreviations:

TCC: triclocarban
TCS: triclosan
DCC: dichlorocarbanilide
MCC: monochlorocarbanilide
NCC: non-chlorinated carbanilide
HAMs: halogenated antimicrobials
TOC: total organic carbon
RQ: risk quotient
PNEC: predicted no-effect concentration
PLS-SEM: partial least squares structural equation modelling

Because TCC and its transformation products differ in environmental persistence and toxicity, transformation can alter ecological risk without simply eliminating the contaminant burden.

Analytical workflow

The main analytical workflow is:

Sediment samples from 140 urban rivers
                |
                v
Chemical concentration measurements
                |
                +-- TCC
                +-- TCS
                +-- DCC
                +-- MCC
                `-- NCC
                |
                v
Contaminant occurrence and sedimentary burden
                |
                v
Dechlorination signatures
                |
                +-- DCC/TCC
                +-- precursor-product coupling
                +-- activity classification
                |
                v
In situ transformation reconstruction
                |
                +-- TCC transformation fraction
                `-- chlorine removal fraction
                |
                v
Toxicity-weighted ecological risk assessment
                |
                v
Counterfactual no-in-situ-dechlorination scenario
                |
                v
Dechlorination-associated risk attenuation
                |
                v
Environmental and anthropogenic driver analysis
                |
                +-- environmental conditions
                +-- socioeconomic conditions
                `-- wastewater-related variables
                |
                v
Metagenomic biomarker analysis
                |
                +-- cdrA
                +-- prdA
                +-- pbrA3
                +-- pcbA4
                `-- rdhA8
                |
                v
PLS-SEM
                |
                v
Input-retention-transformation risk framework
                |
                v
Manuscript and Supplementary figures
Contaminant occurrence

TCC, TCS, and TCC reductive dechlorination products were quantified in urban river sediments.

Contaminant concentrations were evaluated both directly and after normalization to sediment total organic carbon where appropriate.

The analyses characterize:

nationwide occurrence of TCC and TCS;
geographical variation in contamination;
relationships with co-occurring contaminants;
TCC-derived contaminant burden; and
spatial differences in parent–product composition.

For TCC, the summed concentration of the parent compound and its reductive dechlorination products is used to represent the TCC-derived contaminant pool.

In situ dechlorination

The apparent extent of TCC reductive dechlorination is characterized using several complementary chemical signatures.

DCC/TCC ratio

The ratio:

DCC / TCC

is used as the primary scalable indicator of apparent TCC dechlorination activity.

Sediment samples are classified as:

Low activity:
DCC/TCC < 0.34

Moderate activity:
0.34 <= DCC/TCC < 1

High activity:
DCC/TCC >= 1

The threshold of 0.34 represents a conservative reference value derived from previously reported wastewater-sludge conditions.

Precursor-product coupling

Relationships along the sequential transformation pathway:

TCC -> DCC -> MCC -> NCC

are evaluated to distinguish local transformation from simple co-occurrence of compounds introduced from upstream sources.

Increasing sequence-specific precursor–product coupling is interpreted as evidence of progressively expressed in situ reductive dechlorination.

Transformation extent

Molar mass-balance reconstruction is used to estimate:

the fraction of the reconstructed TCC-derived pool transformed to dechlorination products; and
the fraction of chlorine substituents removed during transformation.
Ecological risk assessment

Ecological risk is evaluated using compound-specific risk quotients:

RQ = MEC / PNEC

where:

MEC is the measured environmental concentration; and
PNEC is the corresponding predicted no-effect concentration.

Sediment PNECs are derived from water-phase toxicity thresholds using equilibrium partitioning with compound-specific sediment–water partition coefficients.

Risk categories are defined as:

0.01 <= RQ < 0.1    Low risk
0.1  <= RQ < 1      Moderate risk
RQ >= 1              High risk

Risk estimates are evaluated for TCC and TCS and, where relevant, for the TCC parent–product mixture.

Experimentally determined effect thresholds for TCC and its dechlorination products are additionally used to examine transformation-associated changes in sublethal biological effects.

Transformation-aware risk reconstruction

To quantify the contribution of in situ dechlorination to contemporary sedimentary risk, the workflow constructs a counterfactual scenario in which sedimentary dechlorination does not occur.

Because part of the observed DCC may originate from wastewater treatment or upstream transformation, a conservative upstream allowance is retained.

Dechlorination products attributed to in situ sedimentary transformation are converted to molar-equivalent parent TCC and reassigned to the parent compound in the counterfactual scenario.

The analysis therefore compares:

Observed contemporary risk
           |
           v
Parent + transformation-product mixture

versus

Counterfactual risk
           |
           v
Reconstructed condition without
in situ sedimentary dechlorination

Risk attenuation is calculated as the relative decrease from counterfactual to observed integrated ecological risk.

This approach distinguishes transformation-mediated risk modification from differences in contaminant loading alone.

Environmental and anthropogenic drivers

Environmental, socioeconomic, and urban wastewater-related variables are integrated to investigate controls on:

contaminant occurrence;
sedimentary retention;
dechlorination activity;
dechlorination extent; and
ecological risk.

The compiled variables include information related to:

temperature and precipitation;
water and sediment physicochemical conditions;
population and economic development;
industrial structure;
wastewater discharge;
drainage infrastructure; and
centralized wastewater treatment.

Spearman rank correlations are used to characterize pairwise associations, with Benjamini–Hochberg correction for multiple comparisons where appropriate.

Reductive dehalogenase biomarkers

Metagenomic data are used to identify microbial functional biomarkers associated with TCC dechlorination.

Candidate reductive dehalogenase genes include:

cdrA;
prdA;
pbrA3;
pcbA4; and
rdhA8.

Biomarker abundances are related to chemical indicators of:

dechlorination activity; and
overall dechlorination extent.

Bootstrap resampling is used to evaluate the stability of biomarker–dechlorination associations.

Composite biomarker metrics are also evaluated to determine whether combinations of functional genes improve predictive performance relative to individual biomarkers.

PLS-SEM

Partial least squares structural equation modelling is used to quantify direct and indirect controls on contemporary TCC risk.

The structural framework represents contaminant risk as an outcome of three interacting processes:

Anthropogenic input
        |
        v
Sedimentary retention
        |
        v
In situ microbial transformation
        |
        v
Contemporary ecological risk

Latent constructs represent:

climatic conditions;
socioeconomic conditions;
wastewater-related inputs;
sedimentary retention; and
microbial dechlorination potential.

Model robustness is evaluated using measurement-model diagnostics, structural-model diagnostics, goodness-of-fit metrics, and bootstrap resampling.

The resulting framework is used to compare the relative contributions of contaminant loading, physical retention, and microbial transformation to sedimentary TCC risk.

Repository structure
Dynamic_Risk_Assessment/
|
|-- README.md
|-- LICENSE
|-- requirements.txt
|
|-- data/
|   |-- README.md
|   |-- metadata/
|   |-- source_data/
|   `-- processed/
|
|-- scripts/
|   |-- occurrence/
|   |-- dechlorination/
|   |-- risk_assessment/
|   |-- biomarkers/
|   |-- pls_sem/
|   `-- statistics/
|
|-- outputs/
|
`-- figures/
    |-- main/
    `-- supplementary/
Software

All data processing, statistical analyses, and visualizations were performed primarily using Python 3.12.

Exact package versions and dependencies used for the final analysis are documented in:

requirements.txt
Reproducing the analysis

Clone the repository:

git clone https://github.com/Dylan-Ming-Han-Li/Dynamic_Risk_Assessment.git
cd Dynamic_Risk_Assessment

Create a Python environment:

conda create -n dynamic-risk python=3.12
conda activate dynamic-risk

Install the required packages:

pip install -r requirements.txt

Detailed execution instructions and the recommended script order are documented with the analysis scripts.

Data availability

The study integrates:

sediment concentrations of halogenated antimicrobials;
TCC reductive dechlorination products;
sediment physicochemical measurements;
environmental variables;
socioeconomic indicators;
wastewater-related variables;
ecological risk metrics; and
metagenomic reductive dehalogenase biomarkers.

Processed datasets required to reproduce the reported analyses are provided in this repository where redistribution is permitted.

The provenance, definitions, units, and availability of individual variables are documented in:

data/README.md

Source data underlying the main manuscript figures are provided in:

data/source_data/

Large raw metagenomic sequencing files are not hosted directly in this GitHub repository. Accession information for publicly deposited sequencing data will be provided with the final data release.

Code availability

This repository provides the computational workflow used for:

contaminant occurrence analysis;
dechlorination-signature calculation;
precursor–product association analysis;
reconstruction of in situ transformation extent;
ecological risk assessment;
counterfactual risk reconstruction;
estimation of dechlorination-associated risk attenuation;
environmental and anthropogenic driver analysis;
microbial biomarker analysis;
PLS-SEM;
statistical analyses; and
figure generation.
Manuscript

Microbial dechlorination reshapes halogenated antimicrobial risk in urban river sediments

Dylan Ming-Han Li, Qi-Hong Lu, Han-Lin Cui, Hao Wang, Shu-Hao Du, Zi Zhang, Zi-Feng Zhang, Zhi-Ling Li, Shan-Quan Wang, Ai-Jie Wang, and Bin Liang

Citation information and the article DOI will be added following publication.

License

Code in this repository is distributed under the terms specified in the LICENSE file.

Third-party datasets and externally sourced materials remain subject to the licenses, copyright conditions, and data-use requirements of their original providers.

Contact

For questions regarding the repository:

Dylan Ming-Han Li
Department of Civil and Environmental Engineering
The Hong Kong University of Science and Technology
Hong Kong SAR, China
Email: cemh.li@connect.ust.hk

For correspondence regarding the manuscript:

Ai-Jie Wang
State Key Laboratory of Urban-Rural Water Resource and Environment
Harbin Institute of Technology
Email: wangaijie@hit.edu.cn

Bin Liang
State Key Laboratory of Urban-Rural Water Resource and Environment
Harbin Institute of Technology
Email: liangbin1214@hit.edu.cn
