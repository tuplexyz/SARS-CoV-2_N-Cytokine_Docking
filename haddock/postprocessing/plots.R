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
    ),
    # cytokine_class = factor(cytokine_class)
    # cytokine_class_color = case_when(
    #   cytokine_class == "β-Chemokine" ~ "#E69F00",
    #   cytokine_class == "α-Chemokine" ~ "#56B4E9",
    #   cytokine_class == "Interferon" ~ "#009E73",
    #   cytokine_class == "Interleukin" ~ "#0072B2",
    #   cytokine_class == "Tumor Necrosis Factor" ~ "#D55E00",
    #   cytokine_class == "γ-Chemokine" ~ "#CC79A7",
    #   .default = "#000000"
    # )
  )

# class_levels <- levels(factor(experiment_results$cytokine_class))

# names(haddock_experiment_results) <- c("experiment_name", "n_protein", "cytokine_protein", paste0("haddock_", names(haddock_experiment_results)[4:32]))

## AF2 Results
af2_experiment_results <- read_csv("../../alphafold2_multimer/experiment_results.csv")

colnames(af2_experiment_results) <- paste("af2", colnames(af2_experiment_results), sep = "_") %>% sub("af2_af2_", "af2_", .)


# ## AF2 PRODIGY Results
# af2_prodigy_results <- read_csv("../../alphafold2_multimer/best_AF2_and_GDock_experiment_results.csv")
# 
# # names(af2_prodigy_results) <- paste0("af2_prodigy_", names(af2_prodigy_results))
# 
# ## AF2 FoldX Results
# af2_foldx_results <- read_csv("../../alphafold2_multimer/Best_rankedInteraction_af2_fx.csv") %>% 
#   select(experiment, protein_A, protein_B, `Van der Waals`) %>% 
#   group_by(experiment) %>% 
#   slice(which.min(`Van der Waals`))
# names(af2_foldx_results) <- paste0("af2_foldx_", names(af2_foldx_results))


# af2_experiment_results <- af2_prodigy_results %>%
#   inner_join(af2_foldx_results,
#              by = c("n_protein" = "af2_foldx_protein_A", "cytokine_protein" = "af2_foldx_protein_B"))


## Get Genetic Distances
N_alignment <- read.alignment(file="../inputs/N-Proteins_aligned.fasta", format="fasta")
N_dist <- dist.alignment(N_alignment) %>% 
  as.matrix() %>% 
  as.data.frame() %>% 
  setNames(paste0('dist_from_', names(.))) %>% 
  tibble::rownames_to_column(var = "n_protein") %>% 
  mutate(n_protein = n_protein %>% str_replace("_A", "")) %>% 
  select(n_protein, `dist_from_SARS-CoV-2-WA1-N_A`)


## Make dataframe of all results
experiment_results <- haddock_experiment_results %>%
  left_join(N_dist, by=c("n_protein" = "n_protein")) %>% 
  left_join(af2_experiment_results, by = c("n_protein" = "af2_n_protein",
                                           "cytokine_protein" = "af2_cytokine_protein")) %>% 
  mutate(wa1_wet_hit = case_when(
    cytokine_protein %in% c(
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
      "CXCL14") ~ TRUE,
    TRUE ~ FALSE),
    oc43_wet_hit = case_when(
      cytokine_protein %in% c(
        "CCL5",
        "CCL11",
        "CCL13",
        "CCL20",
        "CCL21",
        "CCL25",
        "CCL26",
        "CCL28",
        "CXCL4",
        "CXCL9",
        "CXCL10",
        "CXCL11",
        "CXCL12alpha",
        "CXCL12beta",
        "CXCL13",
        "CXCL14",
        "IL27") ~ TRUE,
      TRUE ~ FALSE),
    wet_hit = case_when(
      wa1_wet_hit ~ "SARS-CoV-2 Wet Hit",
      oc43_wet_hit ~ "HCoV-OC43 Wet Hit",
      TRUE ~ "Not Wet Hit"),
    wet_hit_symbol = case_when(
      wa1_wet_hit ~ "†",
      oc43_wet_hit ~ "‡",
      TRUE ~ "")
  )

# readr::write_csv(experiment_results, "full_experiment_results.csv")


## Filter to wet hits in SARS-CoV-2
experiment_results_filtered <- experiment_results %>% 
  filter(wet_hit == "SARS-CoV-2 Wet Hit",
         startsWith(n_protein, "SARS-CoV-2")
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

###################################
## SCATTERPLOTS: WET HIT CYTOKINES

dist_by_haddock_gibbs_line_prodigy_wh <- ggplot(experiment_results_filtered,
                                             aes(
                                               x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                               y = haddock_prodigy_deltaG_kcalpermol,
                                               group = cytokine_protein,
                                               color = n_protein
                                             )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -11
  ) +
  facet_wrap(~ cytokine_protein, ncol = 3) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, PRODIGY)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")

## Line Chart (HADDOCK FoldX Delta G)
dist_by_haddock_gibbs_line_foldx_wh <- ggplot(experiment_results_filtered,
                                           aes(
                                             x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                             y = haddock_foldx_deltaG_kcalpermol,
                                             group = cytokine_protein,
                                             color = n_protein
                                           )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -11
  ) +
  facet_wrap(~ cytokine_protein, ncol = 3) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, FoldX)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")



## Line Chart (HADDOCK VDW Energy)
dist_by_haddock_vdw_line_wh <- ggplot(experiment_results_filtered,
                                   aes(
                                     x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                     y = haddock_Evdw,
                                     group = cytokine_protein,
                                     color = n_protein
                                   )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -35
  ) +
  facet_wrap(~ cytokine_protein, ncol = 3) +
  labs(y='van der Waals Energy\n(HADDOCK)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


## Line Chart (AF2 FoldX Delta G)
dist_by_af2_gibbs_line_foldx_wh <- ggplot(experiment_results_filtered,
                                       aes(
                                         x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                         y = af2_foldx_dG,
                                         group = cytokine_protein,
                                         color = n_protein
                                       )
) +
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = 200
  ) +
  facet_wrap(~ cytokine_protein, ncol = 3) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, FoldX)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


## Line Chart (AF2 PRODIGY Delta G)
dist_by_af2_gibbs_line_prodigy_wh <- ggplot(experiment_results_filtered,
                                         aes(
                                           x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                           y = af2_prodigy_deltaG_kcalpermol,
                                           group = cytokine_protein,
                                           color = n_protein
                                         )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -11
  ) +
  facet_wrap(~ cytokine_protein, ncol = 3) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, PRODIGY)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")

## Line Chart (AF2 FoldX VDW)
dist_by_af2_vdw_line_wh <- ggplot(experiment_results_filtered,
                               aes(
                                 x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                 y = `af2_Van der Waals`,
                                 group = cytokine_protein,
                                 color = n_protein
                               )) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -25
  ) +
  facet_wrap(~ cytokine_protein, ncol = 3) +
  labs(y='van der Waals Energy\n(AlphaFold2, FoldX)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


ggarrange(dist_by_haddock_gibbs_line_prodigy_wh,
          dist_by_af2_gibbs_line_prodigy_wh,
          dist_by_haddock_gibbs_line_foldx_wh,
          dist_by_af2_gibbs_line_foldx_wh,
          dist_by_haddock_vdw_line_wh,
          dist_by_af2_vdw_line_wh,
          labels = c(
            "H.a", 
            "AF.a",
            "H.b",
            "AF.b",
            "H.c",
            "AF.c"
          ),
          ncol = 2, nrow = 3) ## Export as 12.75in x 16.5in PDF

###################################
## SCATTERPLOTS: SIGNIFICANT CYTOKINES

## Line Chart (HADDOCK PRODIGY Delta G)
sig_had_pro_er <- experiment_results %>% 
  filter(startsWith(n_protein, "SARS-CoV-2")) %>% 
  group_by(cytokine_protein) %>% 
  summarize(cor.test(`dist_from_SARS-CoV-2-WA1-N_A`, 
                     haddock_prodigy_deltaG_kcalpermol,
                     alternative = "two.sided",
                     method = "spearman")[["p.value"]]) %>% 
  rename(p_value = 2) %>% 
  filter(p_value <= 0.05)

dist_by_haddock_gibbs_line_prodigy_sig <- ggplot(experiment_results %>%
                                               filter(startsWith(n_protein, "SARS-CoV-2"),
                                                      cytokine_protein %in% sig_had_pro_er$cytokine_protein) %>% 
                                                 mutate(cytokine_protein = paste0(cytokine_protein, "   ",
                                                                                  wet_hit_symbol)),
                                             aes(
                                               x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                               y = haddock_prodigy_deltaG_kcalpermol,
                                               group = cytokine_protein,
                                               color = n_protein
                                             )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -11
  ) +
  facet_wrap(~ cytokine_protein, ncol = 2) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, PRODIGY)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")

## Line Chart (HADDOCK FoldX Delta G)
sig_had_fol_er <- experiment_results %>% 
  filter(startsWith(n_protein, "SARS-CoV-2")) %>% 
  group_by(cytokine_protein) %>% 
  summarize(cor.test(`dist_from_SARS-CoV-2-WA1-N_A`, 
                     haddock_foldx_deltaG_kcalpermol,
                     alternative = "two.sided",
                     method = "spearman")[["p.value"]]) %>% 
  rename(p_value = 2) %>% 
  filter(p_value <= 0.05)

dist_by_haddock_gibbs_line_foldx_sig <- ggplot(experiment_results %>%
                                             filter(startsWith(n_protein, "SARS-CoV-2"),
                                                    cytokine_protein %in% sig_had_fol_er$cytokine_protein),
                                           aes(
                                             x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                             y = haddock_foldx_deltaG_kcalpermol,
                                             group = cytokine_protein,
                                             color = n_protein
                                           )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = 0
  ) +
  facet_wrap(~ cytokine_protein, ncol = 2) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, FoldX)',
       # x='Variant',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")



## Line Chart (HADDOCK VDW Energy)
sig_had_vdw_er <- experiment_results %>% 
  filter(startsWith(n_protein, "SARS-CoV-2")) %>% 
  group_by(cytokine_protein) %>% 
  summarize(cor.test(`dist_from_SARS-CoV-2-WA1-N_A`, 
                     haddock_Evdw,
                     alternative = "two.sided",
                     method = "spearman")[["p.value"]]) %>% 
  rename(p_value = 2) %>% 
  filter(p_value <= 0.05)

dist_by_haddock_vdw_line_sig <- ggplot(experiment_results %>%
                                     filter(startsWith(n_protein, "SARS-CoV-2"),
                                            cytokine_protein %in% sig_had_vdw_er$cytokine_protein),
                                   aes(
                                     x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                     y = haddock_Evdw,
                                     group = cytokine_protein,
                                     color = n_protein
                                   )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -60
  ) +
  facet_wrap(~ cytokine_protein, ncol = 2) +
  labs(y='van der Waals Energy\n(HADDOCK)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


## Line Chart (AF2 FoldX Delta G)
sig_af2_fol_er <- experiment_results %>% 
  filter(startsWith(n_protein, "SARS-CoV-2")) %>% 
  group_by(cytokine_protein) %>% 
  summarize(cor.test(`dist_from_SARS-CoV-2-WA1-N_A`, 
                     af2_foldx_dG,
                     alternative = "two.sided",
                     method = "spearman")[["p.value"]]) %>% 
  rename(p_value = 2) %>% 
  filter(p_value <= 0.05)

dist_by_af2_gibbs_line_foldx_sig <- ggplot(experiment_results %>%
                                         filter(startsWith(n_protein, "SARS-CoV-2"),
                                                cytokine_protein %in% sig_af2_fol_er$cytokine_protein),
                                       aes(
                                         x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                         y = af2_foldx_dG,
                                         group = cytokine_protein,
                                         color = n_protein
                                       )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = 25
  ) +
  facet_wrap(~ cytokine_protein, ncol = 2) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, FoldX)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


## Line Chart (AF2 PRODIGY Delta G)
sig_af2_pro_er <- experiment_results %>% 
  filter(startsWith(n_protein, "SARS-CoV-2")) %>% 
  group_by(cytokine_protein) %>% 
  summarize(cor.test(`dist_from_SARS-CoV-2-WA1-N_A`, 
                     af2_prodigy_deltaG_kcalpermol,
                     alternative = "two.sided",
                     method = "spearman")[["p.value"]]) %>% 
  rename(p_value = 2) %>% 
  filter(p_value <= 0.05)

dist_by_af2_gibbs_line_prodigy_sig <- ggplot(experiment_results %>%
                                           filter(startsWith(n_protein, "SARS-CoV-2"),
                                                  cytokine_protein %in% sig_af2_pro_er$cytokine_protein),
                                         aes(
                                           x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                           y = af2_prodigy_deltaG_kcalpermol,
                                           group = cytokine_protein,
                                           color = n_protein
                                         )
) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -20
  ) +
  facet_wrap(~ cytokine_protein, ncol = 2) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, PRODIGY)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")

## Line Chart (AF2 FoldX VDW)
sig_af2_vdw_er <- experiment_results %>% 
  filter(startsWith(n_protein, "SARS-CoV-2")) %>% 
  group_by(cytokine_protein) %>% 
  summarize(cor.test(`dist_from_SARS-CoV-2-WA1-N_A`, 
                     `af2_Van der Waals`,
                     alternative = "two.sided",
                     method = "spearman")[["p.value"]]) %>% 
  rename(p_value = 2) %>% 
  filter(p_value <= 0.05)

dist_by_af2_vdw_line_sig <- ggplot(experiment_results %>%
                                 filter(startsWith(n_protein, "SARS-CoV-2"),
                                        cytokine_protein %in% sig_af2_vdw_er$cytokine_protein),
                               aes(
                                 x = `dist_from_SARS-CoV-2-WA1-N_A`,
                                 y = `af2_Van der Waals`,
                                 group = cytokine_protein,
                                 color = n_protein
                               )) + 
  geom_point() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           # aes(color = cytokine_class_color),
           label.x = min(experiment_results_filtered$`dist_from_SARS-CoV-2-WA1-N_A`),
           label.y = -15
  ) +
  facet_wrap(~ cytokine_protein, ncol = 2) +
  labs(y='van der Waals Energy\n(AlphaFold2, FoldX)',
       x='Distance from SARS-CoV-2 WA1 N',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")


ggarrange(dist_by_haddock_gibbs_line_prodigy_sig,
          dist_by_af2_gibbs_line_prodigy_sig,
          dist_by_haddock_gibbs_line_foldx_sig,
          dist_by_af2_gibbs_line_foldx_sig,
          dist_by_haddock_vdw_line_sig,
          dist_by_af2_vdw_line_sig,
          labels = c(
            "H.a", 
            "AF.a",
            "H.b",
            "AF.b",
            "H.c",
            "AF.c"
            ),
          ncol = 2, nrow = 3) ## Export as 8.5in x 11in PDF

## Boxplots
library(ggpubr)

### HADDOCK
bp_haddock_gibbs_prodigy_wa1 <- ggplot(experiment_results %>% 
                                         filter(n_protein == "SARS-CoV-2-WA1-N"),
                                       aes(x = wa1_wet_hit,
                                           y = haddock_prodigy_deltaG_kcalpermol)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=wa1_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, PRODIGY)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_haddock_gibbs_prodigy_oc43 <- ggplot(experiment_results %>% 
                                          filter(n_protein == "OC43-N"),
                                        aes(x = oc43_wet_hit,
                                            y = haddock_prodigy_deltaG_kcalpermol)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=oc43_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, PRODIGY)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means() 

bp_haddock_gibbs_foldx_wa1 <- ggplot(experiment_results %>% 
                                       filter(n_protein == "SARS-CoV-2-WA1-N"),
                                     aes(x = wa1_wet_hit,
                                         y = haddock_foldx_deltaG_kcalpermol)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=wa1_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, FoldX)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means() 

bp_haddock_gibbs_foldx_oc43 <- ggplot(experiment_results %>% 
                                        filter(n_protein == "OC43-N"),
                                      aes(x = oc43_wet_hit,
                                          y = haddock_foldx_deltaG_kcalpermol)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=oc43_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(HADDOCK, FoldX)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_haddock_vdw_wa1 <- ggplot(experiment_results %>% 
                               filter(n_protein == "SARS-CoV-2-WA1-N"),
                             aes(x = wa1_wet_hit,
                                 y = haddock_Evdw)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=wa1_wet_hit)) +
  labs(y='van der Waals Energy\n(HADDOCK)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_haddock_vdw_oc43 <- ggplot(experiment_results %>% 
                                filter(n_protein == "OC43-N"),
                              aes(x = oc43_wet_hit,
                                  y = haddock_Evdw)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=oc43_wet_hit)) +
  labs(y='van der Waals Energy\n(HADDOCK)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()


### AF2
bp_af2_gibbs_prodigy_wa1 <- ggplot(experiment_results %>% 
                                     filter(n_protein == "SARS-CoV-2-WA1-N"),
                                   aes(x = wa1_wet_hit,
                                       y = af2_prodigy_deltaG_kcalpermol)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=wa1_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, PRODIGY)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means() 

bp_af2_gibbs_prodigy_oc43 <- ggplot(experiment_results %>% 
                                      filter(n_protein == "OC43-N"),
                                    aes(x = oc43_wet_hit,
                                        y = af2_prodigy_deltaG_kcalpermol)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=oc43_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, PRODIGY)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_af2_gibbs_foldx_wa1 <- ggplot(experiment_results %>% 
                                   filter(n_protein == "SARS-CoV-2-WA1-N"),
                                 aes(x = wa1_wet_hit,
                                     y = af2_foldx_dG)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=wa1_wet_hit)) +
  
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, FoldX)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_af2_gibbs_foldx_oc43 <- ggplot(experiment_results %>% 
                                    filter(n_protein == "OC43-N"),
                                  aes(x = oc43_wet_hit,
                                      y = af2_foldx_dG)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=oc43_wet_hit)) +
  labs(y='Predicted Gibbs Energy\n(AlphaFold2, FoldX)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_af2_vdw_wa1 <- ggplot(experiment_results %>% 
                           filter(n_protein == "SARS-CoV-2-WA1-N"),
                         aes(x = wa1_wet_hit,
                             y = `af2_Van der Waals`)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=wa1_wet_hit)) +
  labs(y='van der Waals Energy\n(AlphaFold2, FoldX)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()

bp_af2_vdw_oc43 <- ggplot(experiment_results %>% 
                            filter(n_protein == "OC43-N"),
                          aes(x = oc43_wet_hit,
                              y = `af2_Van der Waals`)) +
  geom_boxplot() +
  geom_dotplot(binaxis = 'y', stackdir = 'center', position = position_dodge(), aes(fill=oc43_wet_hit)) +
  labs(y='van der Waals Energy\n(AlphaFold2, FoldX)',
       x='Wet Hit') +
  facet_wrap(~n_protein) +
  scale_fill_manual(values=c("#5D2689", "#F5BD1F")) + 
  theme_linedraw() +
  theme(legend.position = "none") +
  stat_compare_means()


ggarrange(bp_haddock_gibbs_prodigy_wa1,
          bp_haddock_gibbs_foldx_wa1,
          bp_haddock_vdw_wa1,
          bp_af2_gibbs_prodigy_wa1,
          bp_af2_gibbs_foldx_wa1,
          bp_af2_vdw_wa1,
          bp_haddock_gibbs_prodigy_oc43,
          bp_haddock_gibbs_foldx_oc43,
          bp_haddock_vdw_oc43,
          bp_af2_gibbs_prodigy_oc43,
          bp_af2_gibbs_foldx_oc43,
          bp_af2_vdw_oc43,
          # labels = c("SARS-CoV-2 WA-1 Wet Hits", "HCoV-OC43 Wet Hits"),
          ncol = 6, nrow = 2)

