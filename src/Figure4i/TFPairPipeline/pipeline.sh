#!/bin/bash

# bash script to run Yingnan's pipeline easily and quickly
# based off of command history provided by Liam

# Input should be
#   input directory - directory holding your input files
#   output directory - directory where final output should be stored
#                      output from intermediate steps of this pipeline
#                      will be stored in a script-made directory called
#                      'intermediate-output'

# File format:
#  * Contact files should begin with condition name, and contain string
#      specific_differential
#  * ATAC-seq files should begin with condition name, and contain string scATAC
#  * Condition names should match case between contact files and ATAC-seq files


function check_exit_status() {
    if [ $1 -ne 0 ]; then
	echo 'script failed to exit properly'
	exit $1
    fi
}

# script variables, change to fit your system as necessary
input_dir=$1
output_dir=$2
input_files=${input_dir}/*.list
error_message="Usage: pipeline.sh <input_dir> <output_dir>"
base_dir=$(pwd)
# venv_path="$(pwd)/../MultiCondition_Project/multicondition/"
venv_path="$(pwd)/../multicondition/"

# activate the python virtual environment
source $venv_path/bin/activate
if [ $? -ne 0 ]; then
    echo "Could not activate python virtual environment"
    exit $?
fi

# Check for arguments
if [ $# -lt 2  ]; then
    echo "Not enough arguments"
    echo $error_message
    exit -1
fi

if [ ! -d $input_dir  ]; then
    echo "Input directory does not exist"
    echo $error_message
    exit -1
fi

if [ ! -d $output_dir  ]; then
    echo "Output directory does not exist"
    echo $error_message
    exit -1
fi

# make an output directory for output from each step
# here to keep the output folder clean and make the final output easy to find
if [ ! -d ${output_dir}/intermediate_output ]; then
    mkdir ${output_dir}/intermediate_output
fi
part_output_dir=${output_dir}/intermediate_output

# let the user know what we're using as input
echo "Using condition files:"
for i in $input_files; do
    echo "$(basename $i)"
done
echo

echo "Using ATAC-seq peak files:"
for i in ${input_dir}/*scATAC*;do
    echo "$(basename $i)"
done
echo


# Step One: Extract unique windows for each condition
echo step 1
for file in $input_files; do
    prefix=$(echo $file | cut -d '_' -f 1 | rev | cut -d '/' -f 1 | rev)
    echo $prefix
    python $base_dir/ExtractUniqueWindows/extract_windows.py $file ${part_output_dir}/${prefix}_unique_windows.bed
    check_exit_status $?
done


# Step Two: Bedtools intersect each condition with the corresponding ATAC-seq data
echo step 2
for file in ${part_output_dir}/*_unique_windows.bed; do
    prefix=$(echo $(basename $file) | cut -d '_' -f 1 | rev | cut -d '/' -f 1 | rev)
    atac_file=${input_dir}/all_${prefix}_peaks.tsv
    # for each file, need to find corresponding scATAC file and then run bedtools with it
    bedtools intersect -a $file -b $atac_file > ${part_output_dir}/${prefix}_unique_in_atac.bed
    check_exit_status $?
done


# Step Three: Generate motif files with rgt-motifanalysis
echo step 3
for file in ${part_output_dir}/*_unique_in_atac.bed; do
    # use on unique windows, not on atac - don't quote
    # this should be hocomoco

    # hocomoco 11
    # rgt-motifanalysis matching --organism mm10 --motif-dbs $HOME/rgtdata/motifs/hocomoco/ --output-location $part_output_dir --input-files $file --fpr 0.00001 &

    # hocomoco 12
    rgt-motifanalysis matching --organism mm10 --motif-dbs $HOME/rgtdata/motifs/hocomoco12_mouse_241011_2 --output-location ./$part_output_dir --input-files $file --fpr 0.00001 &

    # Dominika PWMs
    # rgt-motifanalysis matching --organism mm10 --motif-dbs $HOME/rgtdata/motifs/PWM --output-location ./$part_output_dir --input-files $file --fpr 0.00001 &
done
wait


# Step Four: change motif to TF names based on conversions in MOUSE_mono_motifs.tsv from HOCOMOCO
echo step 4
for file in ${part_output_dir}/*mpbs.bed; do
    # cd to put MOUSE_mono_motifs.tsv in working directory
    cd MotifFinding
    # hocomoco 11
    # python ${base_dir}/MotifFinding/correct_motif_names.py ${base_dir}/${file%.*}

    # hocomoco 12
    python ${base_dir}/MotifFinding/match_motifs_to_tfs.py ${base_dir}/${file%.*}

    # dominika PWM
    # ([A-z0-9,]+)* replace with nothing
    # \t\n replace with \n

    # echo $file
    # # sed 's|\(\[A-z0-9,\]\+\)*| |g' $file > ${file}.corrected.bed
    # sed 's|[()]||g' $file > ${file}.corrected.bed
    # # sed 's|\t\n|\n|g' ${file}.corrected.bed > ${file}.corrected.bed
    # awk -v OFS='\t' -i inplace '{$1 = $1; print}' ${file}.corrected.bed
    cd ..
    check_exit_status $?
done


# Step Five: intersect with the TF file
echo step 5
for file in ${part_output_dir}/*corrected.bed; do
    echo $file
    prefix=$(echo $(basename $file) | cut -d '_' -f 1 | rev | cut -d '/' -f 1 | rev)
    bedtools intersect -a ${base_dir}/${part_output_dir}/${prefix}_unique_in_atac.bed -b $file -wa -wb > ${part_output_dir}/${prefix}_tf_unique_in_atac.bed
    check_exit_status $?
done


# Step Six: generate feature tables
echo step 6
for file in ${part_output_dir}/*_tf_unique_in_atac.bed; do
    echo $file
    prefix=$(echo $(basename $file) | cut -d '_' -f 1 | rev | cut -d '/' -f 1 | rev)
    cd Generate-Feature-Table
    
    python getTF_windows.py ${base_dir}/$file ${base_dir}/${part_output_dir}/${prefix}_unique_windows.bed > ${base_dir}/${part_output_dir}/${prefix}.dataset.tfs.csv

    # Dominika HOMER stuff
    # python getFeatureTable.py ${base_dir}/$file ${base_dir}/${part_output_dir}/${prefix}_unique_windows.bed ${base_dir}/${part_output_dir}/${prefix}.dataset.tfs.csv
    check_exit_status $?
    cd ..
done


# Step Seven: get subset of TFs (List 6)
echo step 7
for file in ${part_output_dir}/*.dataset.tfs.csv; do
    prefix=$(echo $(basename $file) | cut -d '.' -f 1 | rev | cut -d '/' -f 1 | rev)
    cd ProcessFeatureTable
    # list 6 should be TF_list2
    # this is configured inside the script
    python get_subset_of_feature_table.py ${base_dir}/$file ${base_dir}/${input_dir}/TF_list10_WTS3_multicondition.csv ${base_dir}/${part_output_dir}/${prefix}_list_6.csv
    check_exit_status $?

    # Dominika PWM
    # cp $base_dir/$file $base_dir/${file}_list_6.csv
    cd ..
done

# Run tf_list_6 tables through fp analysis

# Step Eight: fix column orientation
echo step 8
nfor file in ${part_output_dir}/*_list_6.csv; do
    # this can be made more succinct by generalizing fix_column_orientation,
    # but I don't want to right now
    for file2 in ${part_output_dir}/*_list_6.csv; do
	cd Feature_Pair_Analysis
	if [ ! "$file" = "$file2" ]; then
	    python fix_column_orientation.py ${base_dir}/$file ${base_dir}/$file2
	    check_exit_status $?
	fi
	cd ..
    done
done


# Step Nine: generate feature pairs and filter zero contact pairs
echo step 9
for file in ${part_output_dir}/*_list_6.csv; do
    # prefix=$(echo $(basename $file) | cut -d '_' -f 1 | rev | cut -d '/' -f 1 | rev)
    prefix=$(echo $(basename $file) | cut -d '_' -f 1 | cut -d '.' -f 1 | rev | cut -d '/' -f 1 | rev)
    cd Feature_Pair_Analysis
    echo "generating feature pairs for condition $prefix"

    echo $prefix

    # writes to <CONDITION>_contacts.feature_pair.csv
    cp ${base_dir}/${input_dir}/${prefix}_contacts.list ${base_dir}/${part_output_dir}/
    python generate_feature_pair.py ${base_dir}/${part_output_dir}/${prefix}_contacts.list ${base_dir}/$file
    check_exit_status $?

    echo "filtering zero feature contacts for condition $prefix"

    # writes to <CONDITION>_contacts.feature_pair.filter_zero_feature_contacts.csv
    python filter_zero_feature_contacts.py ${base_dir}/${part_output_dir}/${prefix}_contacts.feature_pair.csv
    check_exit_status $?
    cd ..
done


# # Step Nine Point Five: move the filtered CSVs to the output folder because that's where my
# # multi-condition pipeline ends for now
echo step 9.5
for file in ${part_output_dir}/*_contacts.feature_pair.filter_zero_feature_contacts.csv; do
    prefix=$(echo $(basename $file) | cut -d '_' -f 1 | rev | cut -d '/' -f 1 | rev)
    cp $file ${output_dir}/${prefix}.filt.csv
done


# # Step Ten: combine the foreground and background
# # do I need to use three conditions as background for each condition?
# # what changes do I need to make to the script to accomplish this goal?
# # for file in ${part_output_dir}/*_contacts.feature_pair.filter_zero_feature_contacts.csv; do
# #     python combineforeandback.py

# # need to get both files and use them at once

# # deactivate the python virtual environment
deactivate
