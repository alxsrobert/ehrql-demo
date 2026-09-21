# Task 5: Visualise your results

Write a [scripted action](https://docs.opensafely.org/actions-scripts/) in R or Python to visualise the monthly trends of the measures you calculated for asthma (_Task 2a_) or the diabetes register (_Task 2b_).

If you get stuck, have a look at `solutions/visualise_measures.R`.

## Steps

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/visualise-measures`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Open the starter file**
   - Open `analysis/visualise_measures.R` if you want to use R or `analysis/visualise_measures.py` if you want to use Python.

3. **Load the output from the `generate-measures` action**
   - For example in R (the starter file already loads these packages):

      ```R
      # Load packages
      library(readr)
      library(ggplot2)
      library(scales)
      library(here)

      # Load data
      df_measures <- read_csv(here("output", "measures_dm.csv"))
      ```

   - or in Python:

      ```py
      # Load data
      df_measures = pd.read_csv("output/measures_ast.csv")
      ```

4. **Write and test your plotting code**
   - Write code to visualise the monthly trends of your measures. In our [QOF paper](https://www.medrxiv.org/content/10.1101/2023.07.20.23292883v2.full-text) we chose to visualise the trends like [this](https://www.medrxiv.org/content/medrxiv/early/2023/07/31/2023.07.20.23292883/F1.large.jpg), see panel B for the Hypertension register. For example in R:

      ```R
      # Create plot
      plot_measures <- df_measures |>
        ggplot(aes(x = interval_start, y = ratio, colour = sex)) +
        geom_point() +
        geom_line(alpha = .2) +
        scale_x_date(date_breaks = "1 month", labels = label_date_short())

      # Save plot as .png
      ggsave(here("output", "measures_dm.png"), plot_measures)
      ```

   - You can use R or Python on your own computer, but your package versions may differ from OpenSAFELY's and cause errors. It's safest to test your code in the OpenSAFELY environment. You can check which [R, Python, and Stata packages are available](https://docs.opensafely.org/requesting-libraries/).
   - To open an R console with the same packages as OpenSAFELY, run:

     ```bash
     opensafely exec r:v3 R
     ```

     or for `ipython`:

     ```bash
     opensafely exec python:v2 ipython
     ```

   - For more details see our documentation on [How to use the OpenSAFELY command-line interface](https://docs.opensafely.org/opensafely-cli/#exec-interactive-development)

5. **Update the `project.yaml` file**
   - Add an action for visualising the measures. Your script uses the output from _Task 2a_ or _Task 2b_, so add that action under `needs`.
   - If you're using Python, use `python:v2 analysis/visualise_measures.py` instead.

      ```yaml
      visualise_measures:
        run: r:v3 analysis/visualise_measures.R
        needs: [generate_measures_dm]
        outputs:
          moderately_sensitive:
            plot: output/measures_dm.png
      ```

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
