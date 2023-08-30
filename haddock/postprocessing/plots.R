library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(ggplot2)
library(ggpubr)
library(forcats)
library(ape)
library(seqinr)

## HADDOCK Experiment Results

haddock_experiment_results <- read_csv("experiment_results.csv") %>% 
  mutate(
    cytokine_class = case_when(
      startsWith(cytokine_protein, "CCL") ~ "β-Chemokine",
      startsWith(cytokine_protein, "CX") ~ "α-Chemokine",
      startsWith(cytokine_protein, "IFN") ~ "Interferon",
      startsWith(cytokine_protein, "IL") ~ "Interleukin",
      startsWith(cytokine_protein, "INF") ~ "Interferon",
      startsWith(cytokine_protein, "TNF") ~ "Tumor Necrosis Factor",
      startsWith(cytokine_protein, "XCL") ~ "γ-Chemokine",
      .default = as.character(cytokine_protein)
    )
  ) %>% 
  filter(
    !startsWith(cytokine_protein, "INF"),
    !startsWith(cytokine_protein, "IL-6R"),
    startsWith(n_protein, "SARS-CoV-2")
  )

names(haddock_experiment_results) <- c("n_protein", "cytokine_protein", paste0("haddock_", names(haddock_experiment_results)[3:27]))


## FoldX Results (from AlphaFold2 Experiments)
af2_foldx_results <- read_csv("../../alphafold2_multimer/Best_rankedInteraction_af2_fx.csv")
names(af2_foldx_results) <- paste0("af2_foldx_", names(af2_foldx_results) )

## Get Genetic Distances
N_alignment <- read.alignment(file="../inputs/N-Proteins_aligned.fasta", format="fasta")
N_dist <- dist.alignment(N_alignment) %>% 
  as.matrix() %>% 
  as.data.frame() %>% 
  setNames(paste0('dist_from_', names(.))) %>% 
  tibble::rownames_to_column(var = "n_protein") %>% 
  mutate(n_protein = n_protein %>% str_replace("_A", "")) %>% 
  select(n_protein, `dist_from_SARS-CoV-2-WA1-N_A`)
  

experiment_results_filtered <- haddock_experiment_results %>%
  left_join(N_dist, by=c("n_protein" = "n_protein")) %>% 
  left_join(af2_foldx_results, by = c("n_protein" = "af2_foldx_protein_A", "cytokine_protein" = "af2_foldx_protein_B")) %>% 
  filter(cytokine_protein %in% c(
    "CCL5",
    "CCL11",
    "CCL21",
    "CCL26",
    "CCL28",
    "CXCL4",
    "CXCL9",
    "CXCL10",
    "CXCL11",
    "CXCL12beta",
    "CXCL14"),
    # !n_protein %in% c("OC43-N", "MERS-CoV-N", "SARS-CoV-N")
  )


variant_order = c(
  "OC43-N",
  "MERS-CoV-N",
  "RaTG13-N",
  "BANAL-20-52-N",
  "SARS-CoV-N",
  "SARS-CoV-2-WA1-N", # Wuhan
  "SARS-CoV-2-B.1.1-N", #Pre-Alpha from Europe
  "SARS-CoV-2-B.1.1.7-N",# Alpha
  "SARS-CoV-2-B.1.351-N", # Beta
  "SARS-CoV-2-P.1-N", # Gamma
  "SARS-CoV-2-B.1.617.2-DeltaA-N", # Delta
  "SARS-CoV-2-B.1.1.529-N", # Omicron
  "SARS-CoV-2-BA.1.1-N",
  "SARS-CoV-2-BA.2-N",  
  "SARS-CoV-2-BA.4-N",
  "SARS-CoV-2-BQ.1-N", # Nigerian Lineage
  "SARS-CoV-2-XBB-N" # Kraken
)

## Box Plots
# ggplot(experiment_results_filtered,
#        aes(x = factor(n_protein, variant_order),
#            y = haddock_prodigy_deltaG_kcalpermol
#            # color = cytokine_protein
#            )
#        ) + 
#   geom_boxplot() +
#   # geom_jitter(shape=16,
#   #             position=position_jitter(0.2)) +
#   # geom_point(position=position_jitterdodge(jitter.width=0, dodge.width = 0.3, seed = 1337),
#   #            aes(color=factor(cytokine_protein)), show.legend = F) +
#   facet_wrap(~ haddock_cytokine_class,
#              nrow = 2,
#              ncol = 3) +
#   labs(y='Gibbs Energy',
#        x='Variant',
#        color = "Cytokine Class") +
#   # coord_flip() +
#   theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
#         legend.position = "none")



## Line Chart (HADDOCK PRODIGY Delta G)
dist_by_haddock_gibbs_line <- ggplot(experiment_results_filtered,
       aes(
         # x = factor(n_protein, variant_order),
         x = `dist_from_SARS-CoV-2-WA1-N_A`,
         y = haddock_prodigy_deltaG_kcalpermol,
           group = cytokine_protein,
           color = haddock_cytokine_class
           )
       ) + 
  # geom_line() +
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           aes(color = "black"),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           # label.x = 1,
           label.y = max(experiment_results_filtered$haddock_prodigy_deltaG_kcalpermol) * 1.2
           ) +
  facet_wrap(~ cytokine_protein) +
  labs(y='Gibbs Energy\n(HADDOCK/PRODIGY)',
       # x='Variant',
       x='Distance from SARS-CoV-2-WA1-N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


## Line Chart (HADDOCK VDW Energy)
dist_by_haddock_vdw_line <- ggplot(experiment_results_filtered,
       aes(
         x = `dist_from_SARS-CoV-2-WA1-N_A`,
         y = haddock_Evdw,
         group = cytokine_protein,
         color = haddock_cytokine_class
       )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           aes(color = "black"),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = max(experiment_results_filtered$haddock_Evdw) * 1.2
  ) +
  facet_wrap(~ cytokine_protein) +
  labs(y='van der Waals Energy\n(HADDOCK)',
       x='Distance from SARS-CoV-2-WA1-N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")

## Line Chart (AF2 FoldX Interaction Energy)
dist_by_af2_inteng_line <- ggplot(experiment_results_filtered,
                               aes(
                                 x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                 y = `af2_foldx_Interaction Energy`,
                                 group = cytokine_protein,
                                 color = haddock_cytokine_class
                               )) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           aes(color = "black"),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = max(experiment_results_filtered$`af2_foldx_Interaction Energy`) * 1.2
  ) +
  facet_wrap(~ cytokine_protein) +
  labs(y='Interaction Energy\n(AlphaFold2/FoldX)',
       x='Distance from SARS-CoV-2-WA1-N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")

## Line Chart (AF2 FoldX VDW)
dist_by_af2_vdw_line <- ggplot(experiment_results_filtered,
                                     aes(
                                       x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                       y = `af2_foldx_Van der Waals`,
                                       group = cytokine_protein,
                                       color = haddock_cytokine_class
                                     )) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           aes(color = "black"),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = max(experiment_results_filtered$`af2_foldx_Van der Waals`) * 1.2
  ) +
  facet_wrap(~ cytokine_protein) +
  labs(y='van der Waals Energy\n(AlphaFold2/FoldX)',
       x='Distance from SARS-CoV-2-WA1-N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


ggarrange(dist_by_haddock_gibbs_line, dist_by_haddock_vdw_line, 
          dist_by_af2_inteng_line, dist_by_af2_vdw_line, 
          labels = c("H.a", "H.b", "AF.a", "AF.b"),
          ncol = 2, nrow = 2)

## Correlations

# haddock_experiment_results_pvt <- haddock_experiment_results %>% 
#   select(n_protein, cytokine_protein, prodigy_deltaG_kcalpermol, starts_with("dist_")) %>% 
#   pivot_longer(!c(n_protein, cytokine_protein, prodigy_deltaG_kcalpermol), names_to = "distance_from", values_to = "distance")
# 
# haddock_correlations <- haddock_experiment_results_pvt %>% 
#   group_by(cytokine_protein, distance_from) %>% 
#   summarize(
#     correlation = cor.test(
#       x = prodigy_deltaG_kcalpermol,
#       # y = `dist_from_OC43-N_A`,
#       y = distance,
#       method = "spearman"
#       )[['estimate']],
#     p_value = cor.test(
#       x = prodigy_deltaG_kcalpermol,
#       # y = `dist_from_OC43-N_A`,
#       y = distance,
#       method = "spearman"
#     )[['p.value']],
#     ) %>% 
#   filter(p_value < 0.05)
# 
# 
# ggplot(correlations,
#        aes(x = distance_from,
#            y = cytokine_protein,
#            fill = correlation)) + 
#   geom_tile() +
#   labs(y='Cytokine Protein',
#        x='Distance from ...',
#        color = "Spearman Correlation") +
#   theme_bw() +
#   theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))
