# Cancer Prediction

The replication of the paper *Histopathology images predict multi-omics  aberrations and prognoses in colorectal  cancer patients*.

## Requirements

TODO

## Data Preparation

### TCGA

Data source: [GDC Data Portal](https://portal.gdc.cancer.gov/)

Filter: 
- Cases
    - Primary Site: colon, rectum
    - Program: TCGA
    - Project: TCGA-COAD, TCGA-READ
- Files
    - Data Type: Slide Image
    - Experimental Strategy: Tissue Slide

Download tool: [gdc-data-transfer-tool](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)

## Data Proprocessing

TODO

## Feature Extraction

TODO

## Survival Prediction

TODO

## Code Commit Specification

It is recommended that the commit message be written in the following format:

\<type\>: \<subject\>

The message types are:
- feat - new features
- fix - fix bugs
- docs - documentations or comments
- style - code format
- refactor - refactoring, optimization (neither adding new features nor fixing bugs)
- perf - performance optimization
- test - adding tests
- chore - changes to the build process or auxiliary tools
- revert - roll back
- build - build package
