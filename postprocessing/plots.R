library(readr)
library(dplyr)
library(ggplot2)
library(ggpubr)
library(forcats)

experiment_results <- read_csv("experiment_results.csv")

experiment_results <- experiment_results %>% 
  mutate(
    cytokine_class = case_when(
      startsWith(cytokine_protein, "CCL") ~ "β-Chemokine",
      startsWith(cytokine_protein, "CX") ~ "α-Chemokine",
      startsWith(cytokine_protein, "IFN") ~ "Interferon",
      startsWith(cytokine_protein, "IL") ~ "Interleukin",
      startsWith(cytokine_protein, "INF") ~ "Interleukin",
      startsWith(cytokine_protein, "TNF") ~ "Tumor Necrosis Factor",
      startsWith(cytokine_protein, "XCL") ~ "γ-Chemokine",
      .default = as.character(cytokine_protein)
    )
  )

variant_order = c(
  "RaTG13-N",
  "BANAL-20-52-N",
  "OC43-N",
  "SARS-CoV-N",
  "MERS-CoV-N",
  "SARS-CoV-2-WA1-N",
  "SARS-CoV-2-B.1.351-N",
  "SARS-CoV-2-B.1.617.2-DeltaA-N",
  "SARS-CoV-2-B.1.1-N",
  "SARS-CoV-2-B.1.1.7-N",
  "SARS-CoV-2-B.1.1.529-N",
  "SARS-CoV-2-BA.1.1-N",
  "SARS-CoV-2-BA.2-N",  
  "SARS-CoV-2-BA.4-N",
  "SARS-CoV-2-BQ.1-N",
  "SARS-CoV-2-P.1-N",
  "SARS-CoV-2-XBB-N"
)

## Box Plots
ggplot(experiment_results,
       aes(x = factor(n_protein, variant_order),
           y = prodigy_deltaG_kcalpermol
           # color = cytokine_protein
           )
       ) + 
  geom_boxplot() +
  # geom_jitter(shape=16,
  #             position=position_jitter(0.2)) +
  geom_point(position=position_jitterdodge(jitter.width=0, dodge.width = 0.3, seed = 1234),
             aes(color=factor(cytokine_protein)), show.legend = F) +
  facet_wrap(~ cytokine_class,
             nrow = 2,
             ncol = 3) +
  labs(y='Gibbs Energy',
       x='Variant',
       color = "Cytokine Class") +
  # coord_flip() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")



## Line Chart
ggplot(experiment_results,
       aes(x = factor(n_protein, variant_order),
           y = prodigy_deltaG_kcalpermol,
           group = cytokine_protein,
           color = cytokine_class
           )
       ) + 
  geom_line() +
  geom_smooth(method = lm,
              se = FALSE,
              col='grey',
              linewidth=0.7) +
  stat_cor(method = "spearman",
           aes(color = "black"),
           label.x = 1,
           label.y = max(experiment_results$prodigy_deltaG_kcalpermol) * 1.2) +
  facet_wrap(~ cytokine_protein) +
  labs(y='Gibbs Energy',
       x='Variant',
       color = "Cytokine Class") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1),
        legend.position = "none")
