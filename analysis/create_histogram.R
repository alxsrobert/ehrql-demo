# Load packages
library(readr)
library(ggplot2)
library(here)

# Load data
df <- read_csv(here("output", "depression_dataset.csv"))

# Create histogram
histogram_age <- df |>
  ggplot(aes(x = age)) +
  geom_histogram()

# Save histogram as .png
ggsave(here("output", "histogram_age.png"), histogram_age)
