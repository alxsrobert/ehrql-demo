from ehrql import INTERVAL, create_measures, codelist_from_csv, months
from ehrql.tables.tpp import patients, clinical_events, practice_registrations

measures = create_measures()
measures.configure_dummy_data(population_size=1000)

# Diabetes codelists

# Clinical events up to the end of each interval

# Date of the latest diabetes diagnosis (DMLAT_DAT)

# Date of the latest diabetes resolved code (DMRES_DAT)

# Patient age at the end of each interval (PAT_AGE)

# Numerator

# Denominator

# Define measures
