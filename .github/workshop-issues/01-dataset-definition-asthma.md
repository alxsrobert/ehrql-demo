# Task 1a: Create a dataset definition for asthma

Asthma: Patients with an asthma diagnosis up to the index date and an asthma medication prescribed in the year before the index date

This example is based on the [OpenSAFELY demo repository](https://github.com/bennettoxford/os_training_demonstration).

If you get stuck, have a look at `solutions/dataset_definition_ast.py`.

## Steps

Create a dataset definition for everyone who had a practice registration on 31st March 2024.

Run your code often with `opensafely exec`, like you did in the [Getting Started Tutorial](https://docs.opensafely.org/getting-started/tutorial/generate-a-first-dataset/), so you catch mistakes early. You'll see some error messages along the way, and that's normal. The [Resolving ehrQL errors](https://docs.opensafely.org/ehrql/how-to/errors/) guide can help, or ask one of the workshop helpers.

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-asthma-dataset-definition`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Add the three codelists needed for asthma**
   - Run the following commands in the terminal. Each command adds the codelist to `codelists/codelists.txt` and downloads the `.csv` file to the `codelists/` folder:

     ```bash
     opensafely codelists add https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/ast_cod/20260630/
     opensafely codelists add https://www.opencodelists.org/codelist/nhs-drug-refsets/asttrtatrisk1_cod/20260630/
     opensafely codelists add https://www.opencodelists.org/codelist/nhs-drug-refsets/c19astdrug_cod/20260630/
     ```

3. **Open the starter file**
   - Open `analysis/dataset_definition_ast.py`. The comments in the file show where to add each part of the dataset definition.

4. **Add each codelist to the dataset definition**
   - See the [How to work with codelists](https://docs.opensafely.org/ehrql/how-to/codelists/) guide for more info:

     ```py
     # Asthma codelists
     asthma_codes = codelist_from_csv(
         "codelists/nhsd-primary-care-domain-refsets-ast_cod.csv",
         column="code",
     )
     asthma_inhaled_medication_codes = codelist_from_csv(
         "codelists/nhs-drug-refsets-asttrtatrisk1_cod.csv",
         column="code",
     )
     asthma_oral_medication_codes = codelist_from_csv(
         "codelists/nhs-drug-refsets-c19astdrug_cod.csv",
         column="code",
     )
     asthma_medication_codes = asthma_inhaled_medication_codes + asthma_oral_medication_codes
     ```

5. **Include everyone who had a practice registration on 31st March 2024**
   - Run `opensafely exec ehrql:v1 generate-dataset analysis/dataset_definition_ast.py` in the terminal every now and then to see if your code works.

     ```py
     # Patient is registered with a GP practice on the index date
     has_registration = practice_registrations.exists_for_patient_on(index_date)

     # Define population
     dataset.define_population(has_registration)
     ```

6. **Add age and sex**

     ```py
     # Patient age and sex
     dataset.age = patients.age_on(index_date)
     dataset.sex = patients.sex
     ```

7. **Add the asthma variables**
   - A patient has asthma if they have an asthma diagnosis up to the index date and an asthma medication (inhaled or oral) in the year before the index date:

     ```py
     # Patient has an asthma diagnosis up to the index date
     dataset.has_asthma_diagnosis = (
         clinical_events.where(clinical_events.snomedct_code.is_in(asthma_codes))
         .where(clinical_events.date.is_on_or_before(index_date))
         .exists_for_patient()
     )

     # Patient has an asthma medication in the year before the index date
     one_year_before = index_date - years(1)
     dataset.has_asthma_medication = (
         medications.where(medications.dmd_code.is_in(asthma_medication_codes))
         .where(medications.date.is_on_or_between(one_year_before, index_date))
         .exists_for_patient()
     )

     # Patient has asthma
     dataset.has_asthma = dataset.has_asthma_diagnosis & dataset.has_asthma_medication
     ```

8. **Add an action for your dataset definition to the `project.yaml` file**
   - See [The project pipeline](https://docs.opensafely.org/actions-pipelines/) page in our docs for more:

     ```yaml
     generate_dataset_ast:
       run: >
         ehrql:v1 generate-dataset analysis/dataset_definition_ast.py
         --output output/dataset_ast.csv
       outputs:
         highly_sensitive:
           dataset: output/dataset_ast.csv
     ```

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
