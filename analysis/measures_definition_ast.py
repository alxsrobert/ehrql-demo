from ehrql import INTERVAL, create_measures, codelist_from_csv, months, years
from ehrql.tables.tpp import (
    patients,
    clinical_events,
    medications,
    practice_registrations,
)

index_date = "2024-03-31"

measures = create_measures()
measures.configure_dummy_data(population_size=10000)

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

# Patient has an asthma diagnosis up to the end of each interval
has_asthma_diagnosis = (
    clinical_events.where(clinical_events.snomedct_code.is_in(asthma_codes))
    .where(clinical_events.date.is_on_or_before(INTERVAL.end_date))
    .exists_for_patient()
)

# Patient has an asthma medication in the year before the index date
one_year_before = INTERVAL.end_date - years(1)
has_asthma_medication = (
    medications.where(medications.dmd_code.is_in(asthma_medication_codes))
    .where(medications.date.is_on_or_between(one_year_before, INTERVAL.end_date))
    .exists_for_patient()
)

# Numerator
asthma_numerator = has_asthma_diagnosis & has_asthma_medication

# Denominator
asthma_denominator = practice_registrations.exists_for_patient_on(INTERVAL.end_date)

# Define measures
measures.define_measure(
    name="asthma",
    numerator=asthma_numerator,
    denominator=asthma_denominator,
    group_by={"sex": patients.sex},
    intervals=months(12).starting_on(index_date),
)
