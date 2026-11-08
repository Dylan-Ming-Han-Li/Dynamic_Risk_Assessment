
library(readxl)    
library(dplyr)     
library(psych)     
library(plspm)     
library(reshape2)  
library(tidyr)     
library(ggplot2)   
library(qgraph)    
library(openxlsx)  



library(readxl)

file <- "216.xlsx"

df <- read_excel(path = file)


latent_r <- list(
  Climate    = c("T_air","Precipitation"),
  SocialEco  = c("CPOP","GDP","GDP3"),
  Wastewater = c("WDV","DPL","WDPL","RDPL","CDPL"),
  Sediment   = c("TOC"),
  Gene       = c("CdrA","PbrA3","Rdase-A4","RdhA8"),
  Pollution  = c("TCCs"),
  Risk        = c("Risk")
)


latent_path_r <- rbind(
  Climate    = c(0,0,0,0,0,0,0),
  SocialEco  = c(1,0,0,0,0,0,0),
  Wastewater = c(0,1,0,0,0,0,0),
  Sediment   = c(1,0,1,0,0,0,0),
  Gene       = c(1,0,1,1,0,0,0),
  Pollution  = c(1,1,1,1,1,0,0),
  Risk        = c(1,0,1,1,1,1,0)
)
colnames(latent_path_r) <- rownames(latent_path_r)


modes <- c("A","A","A","A","B", "A", "A")



set.seed(123)
pls_res <- plspm(df, latent_path_r, latent_r, modes = modes)

# —— 6. 打印关键结果 —— 
print(pls_res$crossloadings)  # 交叉载荷
cat("Goodness-of-Fit:", pls_res$gof, "\n\n")
print(pls_res$path_coefs)     # 路径系数矩阵
print(pls_res$effects)        # 直接/间接/总效应



innerplot(pls_res,
          colpos = 'blue', colneg = 'red',
          show.values = FALSE, lcol = 'black',
          box.lwd = 1, curve = 0)
outerplot(pls_res, what = 'loadings',
          arr.width = 0.1, colpos = 'red',
          colneg = 'blue', show.values = TRUE, lcol = 'gray')
outerplot(pls_res, what = 'weights',
          arr.width = 0.1, colpos = 'red',
          colneg = 'blue', show.values = TRUE, lcol = 'gray')



effects_df <- as.data.frame(pls_res$effects) %>%
  separate(relationships, into = c("source","target"), sep = " -> ")
plot_df <- melt(effects_df,
                id.vars      = c("source","target"),
                measure.vars = c("direct","indirect","total"),
                variable.name = "effect_type",
                value.name    = "effect_size") %>%
  filter(target == "Risk") %>%
  mutate(effect_type = factor(effect_type, levels = c("direct","indirect","total")))

ggplot(plot_df, aes(x = effect_size, y = source, fill = effect_type)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(x = "标准化效应大小", y = "源潜变量", title = "对 Risk 的效应（横向展示）") +
  scale_fill_manual(values = c("direct"   = "#008CB7",
                               "indirect" = "#a5C98C",
                               "total"    = "#FFBD00")) +
  theme_bw() +
  theme(axis.text.y = element_text(size = 8),
        legend.title = element_blank()) +
  geom_vline(xintercept = 0, linetype = "solid", size = 0.25)


summary(pls_res)                        
print(pls_res$unidimensionality)        
print(pls_res$outer_model)               
print(pls_res$inner_model)               


path_names <- as.vector(outer(rownames(pls_res$path_coefs),
                              colnames(pls_res$path_coefs),
                              FUN=function(i,j) paste(i,"->",j)))
path_est  <- as.vector(pls_res$path_coefs)
R <- 1000    
boot_mat <- matrix(NA, nrow = R, ncol = length(path_est),
                   dimnames = list(NULL, path_names))

set.seed(456)
n <- nrow(df)    
for (b in seq_len(R)) {
  ii <- sample.int(n, size = n, replace = TRUE)
  dfb <- df[ii, ]
  tmp <- plspm(dfb, latent_path_r, latent_r, modes = modes)
  boot_mat[b, ] <- as.vector(tmp$path_coefs)
}


ci_low  <- apply(boot_mat, 2, quantile, probs = 0.025)
ci_high <- apply(boot_mat, 2, quantile, probs = 0.975)
ci_df <- data.frame(
  path       = path_names,
  estimate   = path_est,
  lower_95ci = ci_low,
  upper_95ci = ci_high,
  row.names  = NULL
)
print(ci_df)


wb <- createWorkbook()
addWorksheet(wb, "path_coef_CI")
writeData(wb, "path_coef_CI", ci_df)
saveWorkbook(wb,
             file = "SEM_paths_with_CI_risk.xlsx",
             overwrite = TRUE)


svg("216.svg", width = 10, height = 6)
path_t <- t(pls_res$path_coefs)
coords <- qgraph(path_t, DoNotPlot = TRUE, layout = "spring", repulsion = 1.2)
qgraph(path_t,
       layout       = coords,
       labels       = colnames(path_t),
       edge.labels  = round(path_t, 2),
       edge.label.cex = 0.8,
       label.cex    = 1,
       minimum      = 0.1,
       directed     = TRUE,
       asize        = 4,
       color        = "lightblue",
       border.width = 1,
       vsize        = 5)
dev.off()


