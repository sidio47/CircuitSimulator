#!/usr/bin/env python

#--------------------------------------------------------------------------------
# System
import os

#--------------------------------------------------------------------------------
# Local
import spawn_real_time_child as srtc

#--------------------------------------------------------------------------------
# Globals

n_list      = [1, 2, 4, 8, 16, 32, 64, 68]
n_list      = [1, 2, 4]
N_list      = [1, 2, 4]
N_list      = [1]
np_list     = [""]
input_list  = ["HT10", "HT11", "HT12", "HT13", "HT14", "HT15", "HT16", "HT17"]
input_list  = ["HT10", "HT11", "HT12"]
queue_list  = ["normal"]
binary_list = ["mpibackend", "mpibackend-opt"]
prof_dict   = {"bare":"ibrun", \
               "remora":"remora ibrun", \
                "vtune":"ibrun amplxe-cl -collect hpc-performance -result-dir="}
                   
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#-------------------------------------------------------------------------------- 

def read_template(filepath):
  return open(filepath, "r").read()

#--------------------------------------------------------------------------------

def fill_template(template, n, N, p, prof, prof_dict, np, binary, input_file):
  name  = "n" + str(n) + "_N" + str(N) + "_prof" + str(prof).split(" ")[0] + "_input" + str(input_file)
  batch = template
  batch = batch.replace("<<<name>>>", str(name))
  batch = batch.replace("<<<n>>>", str(n))
  batch = batch.replace("<<<N>>>", str(N))
  batch = batch.replace("<<<p>>>", str(p))
  if prof != "vtune":
    batch = batch.replace("<<<prof>>>", str(prof_dict[prof]))
  else:
    batch = batch.replace("<<<prof>>>", str(prof_dict[prof])+"vtune_"+name)
  batch = batch.replace("<<<np>>>", str(np))
  batch = batch.replace("<<<input_file>>>", str(input_file))
  batch = batch.replace("<<<binary>>>", str(binary))

  return name, batch

#--------------------------------------------------------------------------------

def submit_job(start_dir, template, n, N, p, prof, prof_dict, np, binary, input_file):
  name, batch = fill_template(template, n, N, p, prof, prof_dict, np, binary, input_file)
  open("batch_" + name,"w").write(batch)
  cmd = "ssh login1 \"cd " + start_dir + "&& sbatch batch_{0} && cat batch_{0}\"".format(name)
  # Slurm batch submit
  return_code = srtc.spawn_real_time_child(total_num_processes = 1   ,\
                                           command             = cmd )

#--------------------------------------------------------------------------------

def run(template):
  start_dir = os.getcwd()
  for n in n_list:
    for N in N_list:
      for input_file in input_list:
        for p in queue_list:
          for prof in prof_dict.keys() or []:
            for np in np_list or []:
              for binary in binary_list:
                submit_job(start_dir, template, n, N, p, prof, prof_dict, np, binary, input_file)


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

if __name__ == "__main__":
  template_path = "./HT.template"
  template  = read_template(template_path)
  run(template)
  
