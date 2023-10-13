#-----------------------------------------------------------------------------------------------------------------------
# The purpose of this script is to combine PTR and abundance matrices from all partitions for a single sample
#
# Author:
#   Vitalii Stebliankin (vsteb002@fiu.edu)
#-----------------------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import os
import argparse

#-----------------------------------------------------------------------------------------------------------------------
# Directories
#-----------------------------------------------------------------------------------------------------------------------

def get_type(genome):
    if "plasmid" in genome:
        return "plasmid"
    elif ("contig" in genome) or ("caffold" in genome):
        return "draft"
    else:
        return "chromosome"

# Directories

# JiIn dataset:
#RESULTS_DIR="/Users/stebliankin/Desktop/FLINTproject/data/JiInData"

# Antibiotics dataset:
#RESULTS_DIR="/Users/stebliankin/Desktop/FLINTproject/data/antibiotics"


# RESULTS_DIR="/scratch/vsteb002/results"
# ptr_out_dir = "/scratch/vsteb002/combined_results"

class CombinePartitionsPlugin:
 def input(self, inputfile):
  self.RESULTS_DIR = inputfile
 def run(self):
  pass
 def output(self, outputfile):
  ptr_out_dir = outputfile

  if not os.path.exists(ptr_out_dir):
    os.mkdir(ptr_out_dir)

  #-----------------------------------------------------------------------------------------------------------------------
  # Get list of samples
  #-----------------------------------------------------------------------------------------------------------------------
  # We are assuming that each folder in RESULTS_DIR is a sample

  samples = os.listdir(self.RESULTS_DIR)


  for sample in samples:
    if sample != ".DS_Store":
        ptr_out_path = ptr_out_dir + "/bPTR_" + sample + ".txt"
        abundance_out_path = ptr_out_dir + "/abundance_" + sample + ".txt"

        results_dir = os.path.join(self.RESULTS_DIR, sample)
        print(results_dir)
        if os.path.exists(ptr_out_path):
            os.remove(ptr_out_path)
        if os.path.exists(abundance_out_path):
            os.remove(abundance_out_path)
        # Merging PTR files:
        with open(ptr_out_path, "a") as ptr_out:
            for partition in range(1, 65):
                ptr_file_partition=results_dir+"/" + "ptr.tsv"


                if os.path.exists(ptr_file_partition):
                    with open(ptr_file_partition, "r") as tmp_file:
                        for i,row in enumerate(tmp_file.readlines()):
                            if (i==0):
                                pass
                            else:
                                if "n/a" not in row:
                                    row = row.replace("\n", "")
                                    attributes = row.split("\t")
                                    genome_path = attributes[0]
                                    ori = attributes[1]
                                    ter = attributes[2]
                                    ptr = attributes[3]

                                    genome = genome_path.split("/")[-1].split("_")[0] +"_" + genome_path.split("/")[-1].split("_")[1]

                                    #ptr_out.write(genome + "\t" + ori + "\t" + ter + "\t" + ptr + "\n")
                                    ptr_out.write(genome + "\t" + ptr + "\n")

                #else:
                #    if (sample == "1"):
                #       print(sample+" DOES NOT EXIST")
        # Merging Abundance Files:
        with open(abundance_out_path, "a") as abundance_out:
            for partition in range(1,65):
                abundance_file_partition = results_dir + "/result.abundance.txt"
                if os.path.exists(abundance_file_partition):

                    with open(abundance_file_partition, 'r') as tmp_file:
                        for i, row in enumerate(tmp_file.readlines()):
                            if i==0:
                                pass
                            else:
                                abundance_out.write(row)

