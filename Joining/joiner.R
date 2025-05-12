# Load required libraries
library(readr)
library(dplyr)
library(tidyr)

# Read the two CSV files
df1 <- read_csv("zm.csv")
df2 <- read_csv("ZM_sum.csv")

# Check and convert if date column is character
if (is.character(df1$Date)) {
  df1$Date <- as.Date(df1$Date, format = "%d/%m/%Y")  # assumes ISO-like format with possible time
}

if (is.character(df2$Date)) {
  df2$Date <- as.Date(df2$Date, format = "%d/%m/%Y")
}

# Perform an inner join on the Date column
combined <- inner_join(df1, df2, by = "Date")

# Remove rows with any NA values
cleaned <- drop_na(combined)

# Write final result to a CSV file
write_csv(cleaned, "combined_cleaned.csv")
