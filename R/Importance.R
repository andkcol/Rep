library(data.table)
library(xgboost)

# Load and combine data
files <- list.files("CSV Masters", pattern = "\\.csv$", full.names = TRUE)
all_data <- rbindlist(lapply(files, function(file) {
  df <- fread(file)
  df[, Date := as.Date(Date, format = "%d/%m/%Y")]
  df[, Company := tools::file_path_sans_ext(basename(file))]
  df[, `:=`(
    Sentiment_lag1 = shift(Avg, 1),
    Sentiment_lag7 = shift(MA7, 1),
    Sentiment_lag20 = shift(MA20, 1),
    Sentiment_lag50 = shift(MA50, 1),
    Target = shift(Close, type = "lead")
  )]
  return(df[, .(Company, Sentiment_lag1, Sentiment_lag7, 
                Sentiment_lag20, Sentiment_lag50, Target)])
}), fill = TRUE)

all_data <- na.omit(all_data)
all_data[, Company_ID := as.integer(as.factor(Company))]
all_data[, `:=`(
  Sentiment_lag1 = scale(Sentiment_lag1),
  Sentiment_lag7 = scale(Sentiment_lag7),
  Sentiment_lag20 = scale(Sentiment_lag20),
  Sentiment_lag50 = scale(Sentiment_lag50),
  Target = scale(Target)
)]

# Train XGBoost
dtrain <- xgb.DMatrix(data = as.matrix(all_data[, .(Sentiment_lag1, 
                      Sentiment_lag7, Sentiment_lag20, Sentiment_lag50)]), 
                      label = all_data$Target)
model <- xgboost(data = dtrain, nrounds = 100, objective = "reg:squarederror", 
                 verbose = 0)

# Feature importance
importance <- xgb.importance(model = model)
print(importance)
xgb.plot.importance(importance)
