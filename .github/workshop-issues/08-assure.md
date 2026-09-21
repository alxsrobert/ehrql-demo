# Task 6: Write assurance tests for your dataset definition

Write _assurance tests_ for your dataset definition from _Task 1a_ (asthma) or _Task 1b_ (diabetes) following the guide on [How to test your dataset definition](https://docs.opensafely.org/ehrql/how-to/test-dataset-definition/#how-to-test-your-dataset-definition).

If you get stuck, have a look at `solutions/test_dataset_definition_dm.py`.

## Steps

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-assurance-tests`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Create a test file**
   - Create a file in `analysis/` named after your dataset definition with `test_` in front, e.g., `test_dataset_definition_dm.py`.

3. **Import dataset and modules**
   - At the beginning of the new test file you need to import your `dataset` and the `date` function. Note that in this example `dataset_definition_dm` refers to the `analysis/dataset_definition_dm.py` file, you will have to change this to the dataset definition you want to test (e.g., `dataset_definition_ast`).

      ```py
      from datetime import date
      from dataset_definition_dm import dataset
      ```

4. **Define test data and expectations**
   - Now you can start defining test data for your assurance tests, see the [Data for test patients](https://docs.opensafely.org/ehrql/how-to/test-dataset-definition/#data-for-test-patients) section in the _How-to guide_. Here are some tips for writing assurance tests:
      - **Only specify data that is needed for your tests**: You only have to specify the data that you actually want to test, e.g., if you just want to test whether a patient is currently registered with a practice you only need to define the start and end date for the practice registration. You don't have to specify all the other columns from the [`practice_registrations`](https://docs.opensafely.org/ehrql/reference/schemas/tpp/#practice_registrations) table (e.g., `practice_pseudo_id` or `practice_stp`). Every table your dataset definition uses needs an entry, even an empty one like `"clinical_events": [{}],` in the example below. The asthma definition also uses `medications`, and if you added IMD (_Task 4_) you'll need `addresses` too.

     ```py
     test_data = {
         # Correctly not expected in population
         # No clinical events
         1: {
             "patients": {"date_of_birth": date(1950, 1, 1)},
             "practice_registrations": [
                 {
                     "start_date": date(2010, 1, 1),
                 },
             ],
             "clinical_events": [{}],
             "expected_in_population": False,
         },
     }
     ```

      - **Define simple test data**: I find it helpful to create _simple_ test patients that only test one isolated aspect of my dataset definition. This means that I end up with many test patients, each testing a specific ehrQL query (e.g., a QOF exclusion rule or patient age calculation).
      - **Run assurance tests repeatedly**: Start with a simple test example and run the assurance tests repeatedly using the following command in your terminal. Adjust the file name as necessary.

      ```bash
      opensafely exec ehrql:v1 assure analysis/<name-of-test-for-dataset-definition>.py
      ```

      - **Start with writing failing tests**: Write tests expecting them to fail initially and then fix them. For example, if testing age calculation, specify an incorrect age in expected_columns to verify the test catches the error.

5. **Expand test coverage**
   - Add more test patients so that you are confident that the main ehrQL queries in your dataset definition are correct.

6. **Add tests to OpenSAFELY pipeline**
   - Add your test file to the `generate-dataset` action in the `project.yaml` file using the [`--test-data-file`](https://docs.opensafely.org/ehrql/reference/cli/#generate-dataset.test-data-file) argument so that the tests get executed every time you run your dataset definition. You'll find the test results in the log file, e.g., `metadata/<name-of-your-generate_dataset-action>.log`.

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
