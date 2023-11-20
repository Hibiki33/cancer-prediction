# Cancer Prediction

The replication of the paper *Histopathology images predict multi-omics  aberrations and prognoses in colorectal  cancer patients*.

## Requirements

```
python==3.10
pytorch==1.12.0 
torchvision==0.13.0
tensorflow==2.10
```

Upon our testing on CUDA 11.6 and 11.7, the following command lines work.

```shell
conda create --name your_env_name python=3.10
conda activate your_env_name
conda install pytorch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0 cudatoolkit=11.6 -c pytorch -c conda-forge
pip install tensorflow==2.10
```

### Openslide

```
pip install Openslide-python
```

#### For Windows:

Download from [OpenSlide](https://openslide.org/download/), add **bin** and **lib** to environment variables.

If you encounter any errors during the `import openslide` process, find the file lowlevel.py from your error message, then add the code following:

```python
import os
os.add_dll_directory("<your openslide bin path>")
```

#### For Ubuntu:

```
apt install python-openslide
```

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

### Refactoring

example:

```
python ./data_preprocessing/refactor_tcga_files.py --json_name E:/frb-cancer-prediction/TCGA20/metadata.cart.2023-11-20.json --input_path E:/frb-cancer-prediction/TCGA20 --output_path ./dataset/TCGA20/origin
```

### Tiling

example:

```
python ./data_preprocessing/tiling.py --input_path ./dataset/TCGA20/origin --output_path ./dataset/TCGA20/tiled
```

### Feature Extraction

TODO

### Normaliztion

TODO

## Survival Prediction

### Temporary notes by wfy

I think prediction.py will run, but with my testing data it has no enough dimentions and will get error in model.

Besides, to get it run, I manually set some parameters.

In utils/prediction.py:

```
loss_function = weibull_loglik_discrete
optimizer = Adam(lr=0.0001)
epochs = 1
```

in which loss_function can be chosen from the 3 given ones in utils/prediction_model.py

In utils/prediction_data_gen.py:

```
n = 1
xi = 0
xj = 1
```

I don't know its use.

**Haven't apply codes after 'evaluation'.**

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
