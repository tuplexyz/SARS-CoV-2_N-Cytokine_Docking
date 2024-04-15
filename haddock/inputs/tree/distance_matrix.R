## Distance Matrix Creation
library(dplyr)
library(seqinr)

## Read in alignment
alignment <- read.alignment("../N-Proteins_aligned_modified.fasta","fasta")

## Calculate distance matrix
dist <- dist.alignment(alignment)
dist_mat <- dist %>% as.matrix()

## Convert distances to percent identity
dist_pct <- 100*(1-dist^2)
dist_pct_mat <- dist_pct %>% as.matrix()

## Replace the upper triangle with the distances, lower with percentages
dist_pct_mat[upper.tri(dist_pct_mat)] <- dist_mat[upper.tri(dist_mat)]

## Convert to data.frame
dist_df <- dist_pct_mat %>% as.data.frame()

## Write matrix as csv
readr::write_csv(dist_df, "N-Proteins_aligned_modified_distance_matrix.csv")
