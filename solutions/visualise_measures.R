# Solution for Task 5: Visualise your results
# Run the generate_measures_dm action from Task 2b before running this file

# Load packages
library(readr)
library(ggplot2)
library(scales)
library(here)

# Load data
df_measures <- read_csv(here("output", "measures_dm.csv"))

# Create plot
plot_measures <- df_measures |>
  ggplot(aes(x = interval_start, y = ratio, colour = sex)) +
  geom_point() +
  geom_line(alpha = .2) +
  scale_x_date(date_breaks = "1 month", labels = label_date_short())

# Save plot as .png
ggsave(here("output", "measures_dm.png"), plot_measures)
