# Solution for Task 1b: Create a dataset definition using the diabetes QOF rules
# Run the codelist commands from step 2 of Task 1b before running this file

from ehrql import create_dataset, codelist_from_csv
from ehrql.tables.tpp import patients, clinical_events, practice_registrations

index_date = "2024-03-31"

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

# Diabetes codelists
dm_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
)
dmres_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code",
)

# Patient is registered with a GP practice on the index date
has_registration = practice_registrations.exists_for_patient_on(index_date)

# Date of the latest diabetes diagnosis (DMLAT_DAT)
dataset.dmlat_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dm_cod))
    .where(clinical_events.date.is_on_or_before(index_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# Date of the latest diabetes resolved code (DMRES_DAT)
dataset.dmres_dat = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dmres_cod))
    .where(clinical_events.date.is_on_or_before(index_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# Patient age on the index date (PAT_AGE)
dataset.pat_age = patients.age_on(index_date)

# Rule 1: Latest diabetes diagnosis is not followed by a diabetes resolved code
dm_reg_r1 = (dataset.dmres_dat < dataset.dmlat_dat) | (
    dataset.dmlat_dat.is_not_null() & dataset.dmres_dat.is_null()
)

# Rule 2: Patient is aged 17 years or older
dm_reg_r2 = dataset.pat_age >= 17

# Define population
dataset.define_population(has_registration & dm_reg_r1 & dm_reg_r2)
