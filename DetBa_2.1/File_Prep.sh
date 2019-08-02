#!/bin/bash
#
#       File_Prep.sh
#       Author: Bassam Haddad
#
#               

n=0

echo "How many input files are there?"
read num_files

echo "What would you like to name your outfile?"
read outs

while [ $n -lt $num_files ]
do
        file="$1$n"                     #The $1 is how you can have arguments in bash, it will use the first argument after the script

        out="$outs"

        out="$out$n"

        head -n-1 $file > $out

        ((n++))
done
