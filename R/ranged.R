library(data.table)

filePath <- "CSV Masters/Zoom.csv"
startDate <- as.Date("02/05/2020", format = "%d/%m/%Y")
endDate <- as.Date("02/05/2025", format = "%d/%m/%Y")

df <- fread(filePath)

df[, Date := as.Date(Date, format = "%d/%m/%Y")]

filteredDF <- df[Date >= startDate & Date <= endDate]

filteredDF <- na.omit(filteredDF)

corrValue <- cor(filteredDF$Close, filteredDF$Avg)
cat("Correlation between Close and sentiment score:", round(corrValue, 4), "\n")
