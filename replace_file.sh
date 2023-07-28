
#!/bin/bash
#export NAME1=IL-23_renumbered.pdb
export NAME1=IL-27_renumbered.pdb
#export NAME1=IL-35_renumbered.pdb
#export NAME1=IL-12p70_renumbered.pdb

broken_files=$(find experiments -name $NAME1)

for broken_file in $broken_files; do
    replacement_file=inputs/Cytokines/$NAME1
    cp $replacement_file $broken_file
done