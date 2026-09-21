# Task 2b: Calculate monthly prevalence of the diabetes register

Using the `measures` framework, calculate how the prevalence of the QOF diabetes register changes month by month during the 2023/24 NHS financial year.

We recommend working on the dataset definition for the diabetes register (_Task 1b_) first, but this is not needed.

## Background

Have a look at our paper on the [Impact of COVID-19 on recorded blood pressure screening and hypertension management in England: An analysis of monthly changes in Quality and Outcomes Framework indicators in OpenSAFELY](https://www.medrxiv.org/content/10.1101/2023.07.20.23292883v2). The subsection _Implementation of QOF business rules in analytic code_ in the Methods section outlines the approach.

If you get stuck, have a look at `solutions/measures_definition_dm.py`.

## Steps

Have a read of [Using the measures framework](https://docs.opensafely.org/ehrql/explanation/measures/) in our docs, then work through the steps below.

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-dm017-measures`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Open the starter file**
   - Open `analysis/measures_definition_dm.py`. The comments in the file show where to add each part of the measures definition.
   - If you haven't worked on _Task 1b_, add the two diabetes codelists first (see step 2 in _Task 1b_).

3. **Add each codelist to the measures definition**
   - This is the same as step 4 in _Task 1b_.

4. **Define numerator and denominator rules**
   - Write these like you would in a dataset definition. The difference is that you use `INTERVAL.start_date` and `INTERVAL.end_date` ([more on the `INTERVAL` placeholder](https://docs.opensafely.org/ehrql/explanation/measures/#the-interval-placeholder)) instead of `index_date`, so ehrQL works them out for each month. For example, to calculate patient age at the end of every monthly interval:

      ```py
      # Field number: 4
      # PAT_AGE: The age of the patient in full years at the achievement date.
      pat_age = patients.age_on(INTERVAL.end_date)
      ```

      or to get the clinical events up to the end of each month:

      ```py
      # Clinical events up to the end of each interval
      selected_events = clinical_events.where(
          clinical_events.date.is_on_or_before(INTERVAL.end_date)
      )

      # Date of the latest diabetes diagnosis (DMLAT_DAT)
      dmlat_dat = (
          selected_events.where(selected_events.snomedct_code.is_in(dm_cod))
          .sort_by(selected_events.date)
          .last_for_patient()
          .date
      )
      ```

5. **Define your measures**
   - Work out what `dm017_numerator` and `dm017_denominator` should be. Add sex as a breakdown variable using the `group_by` argument (see [Grouping by multiple features](https://docs.opensafely.org/ehrql/explanation/measures/#grouping-by-multiple-features)):

      ```py
      # Define measures
      measures.define_measure(
          name="dm017",
          numerator=dm017_numerator,
          denominator=dm017_denominator,
          group_by={"sex": patients.sex},
          intervals=months(12).starting_on("2023-04-01"),
      )
      ```

6. **Test your code using `opensafely exec`**
   - Run `opensafely exec ehrql:v1 generate-measures analysis/measures_definition_dm.py` in the terminal every now and then to see if your code works.

7. **Update the `project.yaml` file**
   - Add an action for generating measures:

      ```yaml
      generate_measures_dm:
        run: >
          ehrql:v1 generate-measures analysis/measures_definition_dm.py
          --output output/measures_dm.csv
        outputs:
          moderately_sensitive:
            measure: output/measures_dm.csv
      ```

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
