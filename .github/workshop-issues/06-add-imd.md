# Task 4: Add IMD

Add the Index of Multiple Deprivation (IMD) quintile of each patient to one of your dataset definitions (_Task 1a_ or _Task 1b_) or measures definitions (_Task 2a_ or _Task 2b_).

## Steps

1. **Create a new branch (optional)**
   - If you know Git, create a new branch for this task, e.g., `<github-user-name>/add-imd`. If you're new to Git and GitHub, skip this step and work on `main`.

2. **Import the `addresses` table**
   - The IMD quintile is available in the [`addresses`](https://docs.opensafely.org/ehrql/reference/schemas/tpp/#addresses) table. Add `addresses` to the tables you import at the top of your file:

     ```py
     from ehrql.tables.tpp import addresses
     ```

3. **Define IMD quintile**
   - Use the address that was active on the index date. In a measures definition, use `INTERVAL.end_date` instead of `index_date`:

     ```py
     # Patient IMD quintile
     imd_quintile = addresses.for_patient_on(index_date).imd_quintile
     ```

4. **Add IMD quintile to your file**
   - In a dataset definition, add IMD quintile as a variable:

     ```py
     dataset.imd_quintile = imd_quintile
     ```

   - In a measures definition, add IMD quintile as a breakdown variable:

     ```py
     group_by={
         "sex": patients.sex,
         "imd_quintile": imd_quintile,
     },
     ```

5. **Test your code using `opensafely exec`**
   - Run `opensafely exec ehrql:v1 generate-dataset analysis/<your-dataset-definition>.py` or `opensafely exec ehrql:v1 generate-measures analysis/<your-measures-definition>.py` in the terminal.

## When you're done

Commit your changes. If you used a branch, merge it into `main` with a pull request, so the next task starts from your latest code.
