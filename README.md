# spacetrees
Code to estimate dispersal rates and locate genetic ancestors from genome-wide genealogies. Associated with the paper, Osmond & Coop 2024: https://elifesciences.org/articles/72177. Forked from https://github.com/osmond-lab/spacetrees.

This version of the code has been updated to allow for ancient samples.

Formerly referred to as sparg, but that name is now reserved for inferring spatial histories from full ancestral recombination graphs (https://github.com/osmond-lab/sparg).

# set up (copied from https://github.com/osmond-lab/spacetrees)

Here is how to get set up and run spacetrees, from the command-line:

- Clone this directory, `git clone https://github.com/raghav034/spacetrees.git`.
- Move into this directory, `cd spacetrees`.
- Install Python v3.11.5 (https://www.python.org/downloads/release/python-3115/). On my server we can do this with `module load NiaEnv/2022a python/3.11.5`. May also work with similar versions. 
- Create virtual environment, `python -m venv venv`. Make sure you are using the correct version of Python to do this.
- Activate virtual environment, `source venv/bin/activate`.
- Install Python packages, `pip install -r requirements.txt`.
- Install tsconvert, which isn't available via pip.
	- `git clone https://github.com/tskit-dev/tsconvert.git`. This was v0.1.dev57+g057435c for me, June 7, 2024.
	- `cd tsconvert`
	- `pip install .`
	- move back to the main working directory, `cd -`
- Install Relate. See https://myersgroup.github.io/relate/index.html for more info and options.
	- On my server I downloaded the source code with `git clone https://github.com/MyersGroup/relate.git` in June 2025. This is roughly version 1.2.2.
	- Move into the Relate directory, `cd relate/build`.
        - On my server I had to load these tools to build relate, `module load cmake/3.22.5 gcc/11.3.0`.
    	- `cmake ..`
    	- `make` 
	- move back to the main working directory, `cd -`
- Run spacetrees via snakemake
	- you should now be able to estimate dispersal and locate genetic ancestors with spacetrees via snakemake! simply write `snakemake all -c1` in the command line (-c1 indicates 1 thread, use more if you have them, but this example should run in less than a minute or two with -c1)
	- on our server we have to first enter `export XDG_CACHE_HOME=$SCRATCH` so that snakemake writes to a write-able location
	- TODO: lots more detail needed about how to customize your options within Snakefile
	- TODO: show how to do this when you have multiple chromosomes
- Plot
	- make virtual environment accessible in Jupyter notebook with `python -m ipykernel install --name $myenv --user` and `venv2jup`
	- TODO: some may need to install Jupyter?
	- open the Jupyter notebook plots.ipynb. I do this through my server's JupyterHub, https://ondemand.scinet.utoronto.ca
	- run the code (command+enter to execute a cell)
- Get in touch!
	- raghav.singhal@mail.utoronto.ca for inquiries specific to this fork
	- mm.osmond@utoronto.ca for inquires about the original repo (found at https://github.com/osmond-lab/spacetrees)

Directories:

- data: move input files (such as .anc, .mut, .poplabels) to this directory. Snakemake spits out output to this directory as well. Best to add 
this directory to your .gitignore
- plots: Any plots generated using jupyterhub are contained here
- relate: Local installation of the relate framework (https://myersgroup.github.io/relate/). Do not change anything here after installation
- tsconvert: Local installing of the tsconvert framework (https://github.com/tskit-dev/tsconvert). Do not change

Files:
- Snakefile: The main snakemake file that orchestrates the entire pipeline. Read documentation at https://snakemake.readthedocs.io/en/stable/ to 
learn how it works
- spacetrees.py: Contains useful functions and calculations used by the snakefile to perform various steps of the inference pipeline
- spacetrees_old.py: An older version of the spacetrees.py logic, maintained as a useful reference point
- utils.py : More helper methods
- Jupyter notebooks:
	- get_locations.ipynb: Takes the initial .poplabels file as input along with metadata for both ancient and contemporary samples. It then filters out samples that don't have associated metadata (latitutde and longitude information) and creates .locations files where the order of locations corresponds with the poplabels files. The locations file is twice the length of the poplabels file (it has the same location twice for a single sample) to account for a diploid population. It also has some code at the end to generate a new poplabels and locations file for samples within a particular latitude and longitude range for both ancients and samples. This might be useful if you want to focus your inference to a subset of the samples. Also contains code to extract a test set of the samples we want to "forget" locations for as future steps. 
	Important note: If you are generating new poplabels and locations file you have to make sure your anc and mut files match up with them. Take a look at extract_subtrees rule within the Snakefile to understand how to do so.
	ancients_new.ipynb: Contains all the code to generate many different plots for ancients and contemporary samples. 
	find_lat_lon.ipynb: Helps extract samples within a desired latitudinal and longitudinal range
	All the other jupyter notebooks (.ipynb files) contain code of the many iterations along the way or were used for debugging and may not be up to date or accurate.

Snakefile and future steps:

To run a new inference you will need your desired .anc, .mut, .coal, and .locations files. The .locations file can be extracted from your .poplabels file as described in the get_locations.ipynb notebook above. If you generated new locations and/or poplabels files that have the number of samples altered you MUST run the extract_subtrees rule to get new anc and mut files and then feed those in to the Snakefile before running the inference. Steps:
1) run the "extract_subtrees" rule using "snakemake extract_subtrees". You have to change the input and output file names and path as appropriate for your files
2) Once you get back the new anc, mut ,and poplabels files from extract_subtrees take these new files and feed them into the Snakefile by changing the anc and mut file names on top. Locations should correspond with these new anc and mut files since you used to same poplabels file to make the locations file as well as the anc and mut files.
3) Change dispersal_loci to the loci you want to use to infer dispersal (may not be applicable if using BLUP)
4) Change ancestor_loci to the loci you want the locate ancestors at
5) Change ancestor_times to the times at which you want to locate ancestors. A log time scale was used here
Note: "config.py" has some code to estimate which loci you want to use. Paste the output directly to the Snakefile and don't use numpy directly in the Snakefile as it 
can cause a segmentation fault on Niagara
6) Now you can run the inference using "snakemake all" or "snakemake locate_forgotten" depending on your use case. Change the wildcards as needed for your use.

For future steps we want to quantify accuracy by forgetting locations of some samples and predicting those sample locations with and without ancient samples. These files with the test data (the samples we want to forget locations of) can be generated using the "get_locations.ipynb" file as described above 


Additional notes:
- After creating the virtual environment (assuming its named "venv") and installing packages, upon subsequent launches you can simply run 
my startup.sh script to perform all the startup steps. Simply run '. startup.sh' from inside snakemake
- I started working on a script (run.sh) to automate the setup, but there might be errors with it. Please be careful is using it to setup your project