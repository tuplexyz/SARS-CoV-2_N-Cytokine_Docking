library(dplyr)
library(readxl)
library(stringr)
library(treeio)
library(ggtree)
library(ggplot2)


## Load in Tree

tree <- read.tree("RAxML_bestTree.N-Proteins_aligned.tre") %>% 
  # root("SARS-CoV-2-WA1-N_A")
  root("OC43-N_A")

## Fix Tip Label Formatting
pretty_tips <- tree$tip.label %>% 
  str_replace_all("-N_A", "") %>% 
  str_replace_all("-2-", "-2 ") %>% 
  str_replace_all("_", ".") %>% 
  str_replace_all("-DeltaA", "") 

tree$tip.label <- pretty_tips


## Log(Branch Length)

tree$edge.length <- log(tree$edge.length) * -1


## Make tree

ggtree(tree, layout='rectangular') +
  geom_tiplab(color='black', offset = 4) +
  # geom_tippoint(color="#FDAC4F", offset = 6, size=3) +
  geom_label(aes(x = branch,
                 label = sprintf("%.0e", exp(branch.length*-1))),
            fill='white') +
  geom_strip('SARS-CoV-2 WA1', 'SARS-CoV-2 XBB', barsize=1, color='blue', 
             label = "SARS-CoV-2 Variants", offset = 45, offset.text = 1) +
  geom_strip('OC43', 'BANAL-20-52', barsize=1, color='orange', 
             label = "Reference Coronaviruses", offset = -70, offset.text = 1) +
  # geom_treescale(x=45, y=2,
  #                width = 10,
  #                label = "ln(branch length) * -1") +
  ggplot2::xlim(0, 200)



