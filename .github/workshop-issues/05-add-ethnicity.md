# Task 3: Add ethnicity

Add patient ethnicity to one of your dataset definitions (_Task 1a_ or _Task 1b_) or measures definitions (_Task 2a_ or _Task 2b_).

## Steps

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-ethnicity`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Add the ethnicity codelist**
   - Run the following command in the terminal. This adds the codelist to `codelists/codelists.txt` and downloads the `.csv` file to the `codelists/` folder:

     ```bash
     opensafely codelists add https://www.opencodelists.org/codelist/opensafely/ethnicity-snomed-0removed/22911876/
     ```

3. **Add the codelist to your file**
   - The `category_column` argument groups the codes into 5 ethnicity groups, see the [How to work with codelists](https://docs.opensafely.org/ehrql/how-to/codelists/) guide for more info:

     ```py
     # Ethnicity codelist
     ethnicity_codes = codelist_from_csv(
         "codelists/opensafely-ethnicity-snomed-0removed.csv",
         column="code",
         category_column="Label_6",
     )
     ```

4. **Define ethnicity**
   - Use the latest recorded ethnicity code for each patient. In a measures definition, use `INTERVAL.end_date` instead of `index_date`:

     ```py
     # Patient ethnicity
     ethnicity = (
         clinical_events.where(clinical_events.snomedct_code.is_in(ethnicity_codes))
         .where(clinical_events.date.is_on_or_before(index_date))
         .sort_by(clinical_events.date)
         .last_for_patient()
         .snomedct_code.to_category(ethnicity_codes)
     )
     ```

5. **Add ethnicity to your file**
   - In a dataset definition, add ethnicity as a variable:

     ```py
     dataset.ethnicity = ethnicity
     ```

   - In a measures definition, add ethnicity as a breakdown variable:

     ```py
     group_by={
         "sex": patients.sex,
         "ethnicity": ethnicity,
     },
     ```

6. **Test your code using `opensafely exec`**
   - Run `opensafely exec ehrql:v1 generate-dataset analysis/<your-dataset-definition>.py` or `opensafely exec ehrql:v1 generate-measures analysis/<your-measures-definition>.py` in the terminal.

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
