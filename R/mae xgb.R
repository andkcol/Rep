library(data.table)
library(xgboost)
library(Metrics)

# Start per company
files <- list.files("CSV Masters", pattern = "\\.csv$", full.names = TRUE)
indivResults <- list()

for(file in files) {
    df <- fread(file)
    df[, `:=`(
        Close_lag1 = shift(Close, 1),
        Sentiment_lag1 = shift(MA50, 1),
        Target = shift(Close, type = "lead")
    )]
    df <- na.omit(df)

    df[, `:=`(
        Close_lag1 = scale(Close_lag1),
        Sentiment_lag1 = scale(Sentiment_lag1),
        Target = scale(Target)
    )]

    trainSize <- floor(0.8 * nrow(df))
    train <- df[1:trainSize]
    test <- df[(trainSize + 1): .N]

    dtrain <- xgb.DMatrix(as.matrix(train[, .(Close_lag1, Sentiment_lag1)]), label = train$Target)
    dtest <- xgb.DMatrix(as.matrix(test[, .(Close_lag1, Sentiment_lag1)]), label = test$Target)

    model <- xgboost(data = dtrain, nrounds = 100, objective = "reg:squarederror", verbose = 0)
    pred <- predict(model, dtest)

    company <- tools::file_path_sans_ext(basename(file))
    indivResults[[company]] <- data.frame(Company = company, MAE = mae(test$Target, pred))
}

indivDF <- rbindlist(indivResults)

# Pooled Model
pooled <- rbindlist(lapply(files, function(file) {
    df <- fread(file)
    df[, `:=`(
        Close_lag1 = shift(Close, 1),
        Sentiment_lag1 = shift(MA50, 1),
        Target = shift(Close, type = "lead"),
        Company = tools::file_path_sans_ext(basename(file))
    )]
    return(df[, .(Company, Close_lag1, Sentiment_lag1, Target)])
}), fill = TRUE)

pooled <- na.omit(pooled)
pooled[, Company_ID := as.integer(as.factor(Company))]
pooled[, `:=`(
    Close_lag1 = scale(Close_lag1),
    Sentiment_lag1 = scale(Sentiment_lag1),
    Target = scale(Target)
)]

set.seed(52)
split <- sample(1:nrow(pooled), 0.8 * nrow(pooled))
train <- pooled[split]
test <- pooled[-split]

dtrain <- xgb.DMatrix(as.matrix(train[, .(Close_lag1, Sentiment_lag1, Company_ID)]), label = train$Target)
dtest <- xgb.DMatrix(as.matrix(test[, .(Close_lag1, Sentiment_lag1, Company_ID)]), label = test$Target)

poolModel <- xgboost(data = dtrain, nrounds = 100, objective = "reg:squarederror", verbose = 0)
poolPred <- predict(poolModel, dtest)
poolMAE <- mae(test$Target, poolPred)

print(indivDF)
cat("\nGlobal Model MAE:", round(poolMAE, 4), "\n")
