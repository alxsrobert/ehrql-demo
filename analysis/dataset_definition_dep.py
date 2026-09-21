from ehrql import create_dataset, codelist_from_csv
from ehrql.tables.tpp import patients, clinical_events

index_date = "2024-03-31"

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

# Depression codelists

# Patient is alive on the index date

# Patient age on the index date

# Date of the latest depression diagnosis

# Date of the latest depression resolved code

# Patient is aged 17 years or older

# Patient has an unresolved depression diagnosis

# Define population
