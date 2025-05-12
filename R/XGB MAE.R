#Company-Level vs Pooled Model Comparison (MAE)
library(data.table)
library(xgboost)
library(Metrics)

# Per-company model results
files <- list.files("CSV Masters", pattern = "\\.csv$", full.names = TRUE)
individual_results <- list()

for (file in files) {
  df <- fread(file)
  df[, `:=`(
    Close_lag1 = shift(Close, 1),
    Sentiment_lag1 = shift(MA50, 1),
    Target = shift(Close, type = "lead")
  )]
  df <- na.omit(df)
  if (nrow(df) < 30) next
  
  df[, `:=`(
    Close_lag1 = scale(Close_lag1),
    Sentiment_lag1 = scale(Sentiment_lag1),
    Target = scale(Target)
  )]
  
  train_size <- floor(0.8 * nrow(df))
  train <- df[1:train_size]
  test <- df[(train_size + 1):.N]
  
  dtrain <- xgb.DMatrix(as.matrix(train[, .(Close_lag1, Sentiment_lag1)]), label = train$Target)
  dtest <- xgb.DMatrix(as.matrix(test[, .(Close_lag1, Sentiment_lag1)]), label = test$Target)
  
  model <- xgboost(data = dtrain, nrounds = 100, objective = "reg:squarederror", verbose = 0)
  preds <- predict(model, dtest)
  
  company <- tools::file_path_sans_ext(basename(file))
  individual_results[[company]] <- data.frame(Company = company, MAE = mae(test$Target, preds))
}

# Combine
individual_df <- rbindlist(individual_results)

# Global model
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

set.seed(42)
split <- sample(1:nrow(pooled), 0.8 * nrow(pooled))
train <- pooled[split]
test <- pooled[-split]

dtrain <- xgb.DMatrix(as.matrix(train[, .(Close_lag1, Sentiment_lag1, Company_ID)]), label = train$Target)
dtest <- xgb.DMatrix(as.matrix(test[, .(Close_lag1, Sentiment_lag1, Company_ID)]), label = test$Target)

global_model <- xgboost(data = dtrain, nrounds = 100, objective = "reg:squarederror", verbose = 0)
global_preds <- predict(global_model, dtest)
global_mae <- mae(test$Target, global_preds)

# Print comparison
print(individual_df)
cat("\nGlobal Model MAE:", round(global_mae, 4), "\n")
