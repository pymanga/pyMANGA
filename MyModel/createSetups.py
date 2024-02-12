import itertools
import os
import sys
sys.path.append('.')
from CreateNewFile import CreateNewFile

path_to_manga = 'C:/Users/marie/Documents/GRIN/git_repos/pyMANGA/MANGA.py'
absolute_path = os.getcwd()

basic_setup_dir = "setup"
species_file = "Saltmarsh.py"

# Create dictionary with parameters
parameter_ref = {"%irag%": [0.005],
                #"%ihag%": [0.01],
                #"%irbg%": [0.005],
                #"%ihbg%": [0.01],
                 #"%gr%": [0.6],
                 "%wrag%": [0.25],
                 "%whag%": [0.25],
                 "%mh%": [1.5]}

pp = [0.5, 1, 1.5]

parameters = {}
for key in parameter_ref:
    parameters[key] = [parameter_ref[key][0] * i for i in pp]


# Iterate through parameter combinations
keys = list(parameters)
i = 1
runfile_object = open('runmangajobs.py', 'a')

for values in itertools.product(*map(parameters.get, keys)):
    setup = dict(zip(keys, values))
    rest = (1-(setup["%wrag%"] + setup["%whag%"]))
    setup["%wrbg%"] = rest/2
    setup["%whbg%"] = rest/2
    setup["%ihag%"] = 0.01
    setup["%ihbg%"] = 0.01
    setup["%irbg%"] = 0.005
    setup["%gr%"] = 1

    #print("setup: ", setup)
    replacements = setup
    new_setup_name = "set"
    for k, v in setup.items():
        n = k.replace("%", "") + "_" + str(round(v, 3)).replace(".", "-")
        new_setup_name += "_" + n
    print(i, new_setup_name)

    new_setup_dir = new_setup_name
    project_file_name = new_setup_name + "/setup.xml"
    new_species_dir = absolute_path + "/" + new_setup_name + "/" + species_file

    i += 1
    CreateNewFile(basic_setup_dir=basic_setup_dir,
                  filename=species_file,
                  replacements=replacements,
                  new_setup_dir=new_setup_dir)
    print(new_species_dir)
    CreateNewFile(basic_setup_dir=basic_setup_dir,
                  filename="setup.xml",
                  replacements={"%out_dir%": new_setup_name,
                                "%spec%": new_species_dir},
                  new_setup_dir=new_setup_dir)

    runfile_object.write('os.system("py ' + path_to_manga + ' -i ' + project_file_name + '")\n')

runfile_object.close()
