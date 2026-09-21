from ehrql import INTERVAL, create_measures, codelist_from_csv, months, years
from ehrql.tables.tpp import (
    patients,
    clinical_events,
    medications,
    practice_registrations,
)

measures = create_measures()
measures.configure_dummy_data(population_size=10000)

# Asthma codelists

# Patient has an asthma diagnosis up to the end of each interval

# Patient has an asthma medication in the year before the end of each interval

# Numerator

# Denominator

# Define measures
