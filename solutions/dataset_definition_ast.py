# Solution for Task 1a: Create a dataset definition for asthma
# Run the codelist commands from step 2 of Task 1a before running this file

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

# Patient is registered with a GP practice on the index date
has_registration = practice_registrations.exists_for_patient_on(index_date)

# Patient age and sex
dataset.age = patients.age_on(index_date)
dataset.sex = patients.sex

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

# Define population
dataset.define_population(has_registration)
