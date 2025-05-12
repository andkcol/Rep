library(data.table)
library(xgboost)

files <- list.files("CSV Masters", pattern = "\\.csv$", full.names = TRUE)
allData <- rbindlist(lapply(files, function(file) {
    df <- fread(file)
    df[, Date := as.Date(Date, format = "%d/%m/%Y")]
    df[, Company := tools::file_path_sans_ext(basename(file))]
    df[, `:=`(
        Sentiment_lag1 = shift(Avg, 1,),
        Sentiment_lag7 = shift(MA7, 1,),
        Sentiment_lag20 = shift(MA20, 1,),
        Sentiment_lag50 = shift(MA50, 1,),
        Target = shift(Close, type = "lead")
    )]
    return(df[, .(Company, Sentiment_lag1, Sentiment_lag7, 
            Sentiment_lag20, Sentiment_lag50, Target)])
}), fill = TRUE)

allData <- na.omit(allData)
allData[, Company_ID := as.integer(as.factor(Company))]
allData[, `:=`(
    Sentiment_lag1 = scale(Sentiment_lag1),
    Sentiment_lag7 = scale(Sentiment_lag7),
    Sentiment_lag20 = scale(Sentiment_lag20),
    Sentiment_lag50 = scale(Sentiment_lag50),
    Target = scale(Target)
)]

dtrain <- xgb.DMatrix(data = as.matrix(allData[, .(Sentiment_lag1, 
            Sentiment_lag7, Sentiment_lag20, Sentiment_lag50)]), 
            label = allData$Target)
model <- xgboost(data = dtrain, nrounds = 100, objective = "reg:squarederror", 
            verbose = 0)

importance <- xgb.importance(model = model)
print(importance)
xgb.plot.importance(importance)
