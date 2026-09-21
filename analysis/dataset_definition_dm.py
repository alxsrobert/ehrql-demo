from ehrql import create_dataset, codelist_from_csv
from ehrql.tables.tpp import patients, clinical_events, practice_registrations

index_date = "2024-03-31"

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

# Diabetes codelists

# Patient is registered with a GP practice on the index date

# Date of the latest diabetes diagnosis (DMLAT_DAT)

# Date of the latest diabetes resolved code (DMRES_DAT)

# Patient age on the index date (PAT_AGE)

# Rule 1: Latest diabetes diagnosis is not followed by a diabetes resolved code

# Rule 2: Patient is aged 17 years or older

# Define population
