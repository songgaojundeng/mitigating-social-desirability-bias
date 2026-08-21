# Mitigating Social Desirability Bias in Random Silicon Sampling
This repository contains the code and data for the paper "Mitigating Social Desirability Bias in Random Silicon Sampling," accepted to TMLR 2026. 

### Data
Within the data folder, you'll find the `ANES` and `WVS` data including questionnaires and statistical data . Raw dataset can be downloaded from [American National Election Studies (ANES)](https://electionstudies.org/data-center/) and [World Values Survey Wave 7 (2017-2022)
](https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp).

### Code
We have reproduced and modified the user/system prompts described in [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144). The code has been modified and augmented based on the code used by [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144).

`common.py` is a script for using the OpenAI API. Insert your own OpenAI API key and select the desired model as the `engine` argument. In [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144), `gpt-3.5-turbo-0613` was adopted. In this paper, `gpt-4.1-mini` was adopted.

`common_llama8b.py` and `common_llama3170b.py` are scripts for using the Llama 3.1-8B-instruct and Llama 3.1-70B-instruct model, respectively. The model and required python packages were downloaded locally in the same directory.

`anes2012.py`, `anes2016.py`, `anes2020.py`, and `anes2024.py` are scripts for converting demographic information of respondents from each respective ANES dataset into first-person prompts. Similarly, `anesxxxx_thirdperson.py` converts it into third-person prompts.                                                            

`main_mq.py` is a script for the multiple question experiment. It facilitates random silicon sampling using ANES 2020 data for 10 survey questions selected in our study (8 for ANES 2024).  You can run 
``` 
python main_mq.py <year> <pov: first/third> <questionnaire_version: original/reformulated> <none/priming/preamble>
```
to conduct random silicon sampling on the ANES data for the specified year.
 

`main_mq_wvs_country.py` is a script for the WVS survey. It facilitates random silicon sampling using WVS country data for 10 survey questions selected in our study.  You can run 
``` 
python main_mq_wvs_country.py <country: DEU/NLD/GBR> <questionnaire_version: original/reformulated> <none/priming/preamble>
```


### Results
The folder `Publication Results` contains all random silicon sampling results obtained in this study.

### Analysis
The folder `analysis` contains all code used for analyzing the results.

#### Citation [to be updated]

If you find this repository or our work useful in your research, please consider citing our paper:

@article{...} 