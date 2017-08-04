#!/usr/bin/env python

#--------------------------------------------------------------------------------
# System
import os
import subprocess as sp
import sys
import time

#--------------------------------------------------------------------------------
# Local
import spawn_real_time_child as srtc

#--------------------------------------------------------------------------------
# Globals

n_list      = [1, 2, 4, 8, 16, 32, 64, 68]
N_list      = [1, 2, 4, 8, 16, 32]
np_list     = [""]
input_list  = ["HT10", "HT11", "HT12", "HT13", "HT14", "HT15", "HT16", "HT17", "HT18", "HT19", "HT20"]
queue_list  = ["normal"]
binary_list = ["mpibackend", "mpibackend-opt"]
prof_dict   = {"bare":"ibrun", \
               "remora":"remora ibrun", \
                "vtune":"ibrun amplxe-cl -collect hpc-performance -result-dir="}
prof_dict   = {"bare":"ibrun"}
                   
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
  count = 0
  tc = 0
  dt = 2
  invalid_job_count = 0
  for n in n_list:
    for N in N_list:
      for input_file in input_list:
        for p in queue_list:
          for prof in prof_dict.keys() or []:
            for np in np_list:
              for binary in binary_list:
 
                if n < N:
                  invalid_job_count += 1
                  continue

                tot = len(n_list) * len(N_list) * len(input_list) * len(queue_list) * len(prof_dict.keys()) * len(np_list) * len(binary_list) - invalid_job_count
                
                count += 1
                print("="*80)
                print("JOB: {0}".format(count))
                print("="*80)

                submit_job(start_dir, template, n, N, p, prof, prof_dict, np, binary, input_file)

                time.sleep(dt)
                while True:
                  p1 = sp.Popen(["squeue", "-l","-u",os.environ["USER"]], stdout=sp.PIPE)
                  p2 = sp.Popen(["grep","RUNNING"], stdin=p1.stdout, stdout=sp.PIPE)
                  p3 = sp.Popen(["wc","-l"], stdin=p2.stdout, stdout=sp.PIPE)
                  running_jobs = int(p3.communicate()[0])
                  p1 = sp.Popen(["squeue", "-l","-u",os.environ["USER"]], stdout=sp.PIPE)
                  p2 = sp.Popen(["grep","PENDING"], stdin=p1.stdout, stdout=sp.PIPE)
                  p3 = sp.Popen(["wc","-l"], stdin=p2.stdout, stdout=sp.PIPE)
                  pending_jobs = int(p3.communicate()[0])
                  if running_jobs + pending_jobs < 45:
                    sys.stdout.write("\rTICK: {0}; COUNT: {1}/{2}; {3}/{4} jobs currently running/pending...".format(tc,count,tot,running_jobs,pending_jobs))
                    sys.stdout.flush()
                    time.sleep(dt)
                    break
                  else:
                    tc += dt
                    sys.stdout.write("\rTICK: {0}; COUNT: {1}/{2}; {3}/{4} jobs currently running/pending...".format(tc,count,tot,running_jobs,pending_jobs))
                    sys.stdout.flush()
                    time.sleep(dt)



#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------

if __name__ == "__main__":
  template_path = "./HT.template"
  template  = read_template(template_path)
  run(template)
  
