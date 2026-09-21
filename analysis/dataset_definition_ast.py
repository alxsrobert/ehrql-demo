from ehrql import create_dataset, codelist_from_csv, years
from ehrql.tables.tpp import (
    patients,
    clinical_events,
    medications,
    practice_registrations,
)

index_date = "2024-03-31"

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

# Asthma codelists

# Patient is registered with a GP practice on the index date

# Patient age and sex

# Patient has an asthma diagnosis up to the index date

# Patient has an asthma medication in the year before the index date

# Patient has asthma

# Define population
