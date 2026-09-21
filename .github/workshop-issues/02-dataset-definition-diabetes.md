# Task 1b: Create a dataset definition using the diabetes QOF rules

Diabetes register: Patients aged at least 17 years old with an unresolved diabetes diagnosis

You can find the rules for all QOF registers and indicators on the [NHS England website](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/business-rules/quality-and-outcomes-framework-qof-business-rules-v49-2024-25). Each indicator's rules are in section 3.2.2.1 of its Word document, e.g., `Diabetes_v49.0.docx`.

## QOF rules

- **Rule 1**: Pass to the next rule all patients from the specified population who meet both of the criteria below and reject the remaining patients.
  - Have a diabetes diagnosis in the patient record up to and including the achievement date.
  - Latest diabetes diagnosis is not followed by a diabetes resolved code.
- **Rule 2**: Reject patients passed to this rule who are aged under 17 years old on the achievement date. Select the remaining patients.

If you get stuck, have a look at `solutions/dataset_definition_dm.py`.

## Steps

Build the QOF diabetes register (version 49) for the 2023/24 NHS financial year (1st April 2023 to 31st March 2024).

Run your code often with `opensafely exec`, like you did in the [Getting Started Tutorial](https://docs.opensafely.org/getting-started/tutorial/generate-a-first-dataset/), so you catch mistakes early. You'll see some error messages along the way, and that's normal. The [Resolving ehrQL errors](https://docs.opensafely.org/ehrql/how-to/errors/) guide can help, or ask one of the workshop helpers.

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-diabetes-dataset-definition`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Add the two codelists needed for the register**
   - The codelists are available at https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets. Run the following commands in the terminal. Each command adds the codelist to `codelists/codelists.txt` and downloads the `.csv` file to the `codelists/` folder:

     ```bash
     opensafely codelists add https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/dm_cod/20260630/
     opensafely codelists add https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/dmres_cod/20260630/
     ```

3. **Open the starter file**
   - Open `analysis/dataset_definition_dm.py`. The comments in the file show where to add each part of the register.

4. **Add each codelist to the dataset definition**
   - See the [How to work with codelists](https://docs.opensafely.org/ehrql/how-to/codelists/) guide for more info.

5. **Include everyone who had a practice registration on 31st March 2024** (this is slightly different to what the QOF rules actually say)
   - Run `opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition_dm.py` in the terminal every now and then to see if your code works.

     ```py
     # Patient is registered with a GP practice on the index date
     has_registration = practice_registrations.exists_for_patient_on(index_date)
     ```

6. **Add all variables needed for the register** (`DM_REG`)
   - Again, run `opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition_dm.py` in the terminal every now and then to see if your code works. For example:

     ```py
     # Field number: 6
     # DMLAT_DAT: Date of the most recent diabetes diagnosis up to and
     # including the achievement date.
     dataset.dmlat_dat = (
         clinical_events.where(clinical_events.snomedct_code.is_in(dm_cod))
         .where(clinical_events.date.is_on_or_before(index_date))
         .sort_by(clinical_events.date)
         .last_for_patient()
         .date
     )
     ```

7. **Write each rule in ehrQL**
   - Then combine the rules to define your population. See the [Combining multiple inclusion criteria](https://docs.opensafely.org/ehrql/how-to/define-population/#combining-multiple-inclusion-criteria) section in our docs:

     ```py
     # DM REGISTER (DM_REG)
     # DM_REG rule 1:
     # Pass to the next rule all patients from the specified population who meet
     # both of the criteria below: Have a diabetes diagnosis in the patient record
     # up to and including the achievement date. Latest diabetes diagnosis is not
     # followed by a diabetes resolved code.
     dm_reg_r1 = (dataset.dmres_dat < dataset.dmlat_dat) | (
         dataset.dmlat_dat.is_not_null() & dataset.dmres_dat.is_null()
     )
     ```

8. **Add an action for your dataset definition to the `project.yaml` file**
   - See [The project pipeline](https://docs.opensafely.org/actions-pipelines/) page in our docs for more:

     ```yaml
     generate_dataset_dm:
       run: >
         ehrql:v1 generate-dataset analysis/dataset_definition_dm.py
         --output output/dataset_dm.csv
       outputs:
         highly_sensitive:
           dataset: output/dataset_dm.csv
     ```

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
