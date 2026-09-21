# Task 2a: Calculate monthly prevalence of asthma

Using the `measures` framework, calculate the monthly prevalence of asthma during the 2023/24 NHS financial year.

We recommend working on the dataset definition for asthma (_Task 1a_) first, but this is not needed.

If you get stuck, have a look at `solutions/measures_definition_ast.py`.

## Steps

Have a read of [Using the measures framework](https://docs.opensafely.org/ehrql/explanation/measures/) in our docs, then work through the steps below.

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-asthma-measures`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Open the starter file**
   - Open `analysis/measures_definition_ast.py`. The comments in the file show where to add each part of the measures definition.
   - If you haven't worked on _Task 1a_, add the three asthma codelists first (see step 2 in _Task 1a_).

3. **Add each codelist to the measures definition**
   - This is the same as step 4 in _Task 1a_.

4. **Define numerator and denominator rules**
   - Write these like you would in a dataset definition. The difference is that you use `INTERVAL.start_date` and `INTERVAL.end_date` ([more on the `INTERVAL` placeholder](https://docs.opensafely.org/ehrql/explanation/measures/#the-interval-placeholder)) instead of `index_date`, so ehrQL works them out for each month:

      ```py
      # Patient has an asthma diagnosis up to the end of each interval
      has_asthma_diagnosis = (
          clinical_events.where(clinical_events.snomedct_code.is_in(asthma_codes))
          .where(clinical_events.date.is_on_or_before(INTERVAL.end_date))
          .exists_for_patient()
      )

      # Patient has an asthma medication in the year before the end of each interval
      one_year_before = INTERVAL.end_date - years(1)
      has_asthma_medication = (
          medications.where(medications.dmd_code.is_in(asthma_medication_codes))
          .where(medications.date.is_on_or_between(one_year_before, INTERVAL.end_date))
          .exists_for_patient()
      )

      # Numerator
      asthma_numerator = has_asthma_diagnosis & has_asthma_medication

      # Denominator
      asthma_denominator = practice_registrations.exists_for_patient_on(INTERVAL.end_date)
      ```

5. **Define your measures**
   - Add sex as a breakdown variable using the `group_by` argument (see [Grouping by multiple features](https://docs.opensafely.org/ehrql/explanation/measures/#grouping-by-multiple-features)):

      ```py
      # Define measures
      measures.define_measure(
          name="asthma",
          numerator=asthma_numerator,
          denominator=asthma_denominator,
          group_by={"sex": patients.sex},
          intervals=months(12).starting_on("2023-04-01"),
      )
      ```

6. **Test your code using `opensafely exec`**
   - Run `opensafely exec ehrql:v1 generate-measures analysis/measures_definition_ast.py` in the terminal every now and then to see if your code works.

7. **Update the `project.yaml` file**
   - Add an action for generating measures:

      ```yaml
      generate_measures_ast:
        run: >
          ehrql:v1 generate-measures analysis/measures_definition_ast.py
          --output output/measures_ast.csv
        outputs:
          moderately_sensitive:
            measure: output/measures_ast.csv
      ```

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
