# Mitigating Social Desirability Bias in Random Silicon Sampling
This repository contains the code for the paper "Mitigating Social Desirability Bias in Random Silicon Sampling." All code has been anonymized for confidentiality.

### Data
Within the data folder, you'll find the ANES data from the years 2012, 2016, 2020, and 2024. Additionally, the questionnaire file `ANES_2020_multiple_questions_selected.xlsx`, used for the multiple question experiment, is also included. Each dataset can be downloaded from [American National Election Studies (ANES)](https://electionstudies.org/data-center/).

### Code
We have reproduced and modified the user/system prompts described in [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144). The code has been modified and augmented based on the code used by [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144).

`common.py` is a script for using the OpenAI API. Insert your own OpenAI API key and select the desired model as the `engine` argument. In [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144), `gpt-3.5-turbo-0613` was adopted. In this paper, `gpt-4.1-mini` was adopted

`newcommon.py` is a script for using the Llama 3.1-8B-instruct model. The model and required python packages were downloaded locally in the same directory.

`batchcommon.py` is a script for using the Llama 3.1-70B-instruct model. The model and required python packages were downloaded locally in the same directory. This file specifically batches multiple prompts into a single call to improve experimental runtime.

`anes2012.py`, `anes2016.py`, `anes2020.py`, and `anes2024.py` are scripts for converting demographic information of respondents from each respective ANES dataset into first-person prompts. Similarly, `anesxxxx_thirdperson.py` converts it into third-person prompts.                                                            

`main.py` is a script for performing random silicon sampling on the U.S. presidential election candidate choice for each year. You can run 
``` 
python main.py <year>
```
to conduct random silicon sampling on the ANES data for the specified year.

`main_mq.py` is a script for the multiple question experiment. It facilitates random silicon sampling using ANES 2020 data for 10 surveys selected in our study.

