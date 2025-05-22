# NLP_2025_grp_Amina-Lilja-Miko-Zosia
 Code and documents for natural language processing course, BDS 2025. From group 1: Amina, Lilja, Mikolaj and Zosia
 
 Link on GitHub: https://github.com/4Lili4/NLP_2025_grp_Amina-Lilja-Miko-Zosia

## Running the code
To install the required libraries in a new environment, open your Anaconda prompt and direct to this repository. Then paste and run the following:
```
conda env create -f requirements.yml
```
Or - for pip - use:
```
py -m venv .nlp_grp1
pip install -r requirements.txt
```

When you have the required dependencies installed, activate the environment with
```
conda activate nlp_grp1
```
or 
```
source nlp_grp1/bin/activate
```

Now, all final code and results can be run through the Main.IPYNB file in the root of the repository. Each step of the process has been converted to a python-file, with functions called from Main. This is done to centralize the results of all the code in one easily accessible place.


## Contents of files and folders
The repository contains 3 front-page files and 5 folders: 
 - The Main.IPYNB is the jupyter notebook through which all our final code can be run. It pulls functions from python-files, and lets you centralize the entire project's final code results.
 - README.md is self-explanatory - you're reading me ;-)
 - requirements.yml is our environment-file, and it contains all dependencies. It is made to be run through conda, if you use pip, you may use the .txt-file instead.
<br>

 - baseline_and_project_proposal contains our previous submissions of baseline results, project proposal and project proposal presentation
 - data-files_and_results contains all our csv- and text-files with the data from both WikiAnn and fewnerd. Any files created during the process also land in that folder
 - python_files contains all our final code that we use to get our results. The code is formatted into python-functions, that are run from the Main.IPYNB notebook.
 - Lastly, WIP_notebooks and WIP_notes_and_inspiration contain are work-in-progress files and considerations. That means all working notebooks, dataset articles etc., are in those folders.

## References:
 - dill. 2025. dill package documentation. https://dill.readthedocs.io/en/latest/index.html
 - Explosion. 2024. Training pipelines & models. https://spacy.io/usage/training".key
 - pandas. 2024. pandas documentation (version:2.2.3). https://pandas.pydata.org/docs/index.html
