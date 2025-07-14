"""
====================================================================================================================
Python script name match_motifs_to_tfs.py
Script written by Liam Speakman

Date: July 14, 2025

This script takes in a .bed file with the column form "chr start stop motif - -" and maps the motif column to the corresponding gene name 

Usage example:
>>> python3 match_motifs_to_tfs.py S3_motifs_in_atac_mpbs.bed
The above example creates a file called S3_motifs_in_atac_mpbs.corrected.bed

=====================================================================================================================
"""
import pandas as pd
import json
import sys
if not len(sys.argv) == 2:
    print("command filename")
    sys.exit(-1)
out_file = pd.read_csv(f"{sys.argv[1]}.bed", 
names=["chromosome", "start", "stop", "name", "temp1", "temp2"],
sep="\t", index_col=False)


annotation = open("H12CORE-MOUSE_annotation.jsonl")
annotation = [json.loads(line.rstrip()) for line in annotation]
annotation = [(ann["name"], ann["masterlist_info"]["species"]["MOUSE"]["gene_symbol"]) for ann in annotation]
anno_dict = {}
[anno_dict.update({k:v}) for k,v in annotation]

def map_motifs(row, anno_dict):
    if row["name"] in anno_dict:
        return anno_dict[row["name"]]
    return row["name"]
out_file["name"] = out_file.apply(lambda x: map_motifs(x, anno_dict), axis=1)
out_file.to_csv(f"{sys.argv[1]}.corrected.bed", sep="\t", header=False, index=False)
