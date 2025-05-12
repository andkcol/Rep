library(data.table)
library(lmtest)
library(ggplot2)

dataFolder <- "CSV Masters"
files <- list.files(dataFolder, full.names = TRUE, pattern = "\\.csv$")

results <- list()

for(file in files){
    df <- fread(file)

    df <- df[order(as.Date(Date, format = "%d/%m/%Y"))]
    df <- na.omit(df[, .(Close, Avg)])

    test <- tryCatch({
        grangertest(Close ~ Avg, order = 2, data = df)}, error = function(e) NULL)
    
    if(!is.null(test)){
        company <- tools::file_path_sans_ext(basename(file))
        pvalue <- test$`Pr(>F)`[2]
        results[[company]] <- data.frame(
            Company = company,
            F_Stat = test$F[2],
            P_Value = pvalue
        )
    }
}

grangerDF <- rbindlist(results)

print(grangerDF)

ggplot(grangerDF, aes(x = reorder(Company, P_Value), y = P_Value)) +
    geom_col(fill = ifelse(grangerDF$P_Value < 0.05, "chartreuse3", "steelblue")) +
    geom_hline(yintercept = 0.05, linetype = "dashed", color = "red") +
    labs(title = "Granger Causality Test for Sentiment Score",
        x = "Company", y = "P-Value") + 
    coord_flip() + theme_minimal()
