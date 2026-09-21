# Solution for Task 2b: Calculate monthly prevalence of the diabetes register
# Run the codelist commands from step 2 of Task 1b before running this file

from ehrql import INTERVAL, create_measures, codelist_from_csv, months
from ehrql.tables.tpp import patients, clinical_events, practice_registrations

measures = create_measures()
measures.configure_dummy_data(population_size=1000)

# Diabetes codelists
dm_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
)
dmres_cod = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code",
)

# Clinical events up to the end of each interval
selected_events = clinical_events.where(
    clinical_events.date.is_on_or_before(INTERVAL.end_date)
)

# Date of the latest diabetes diagnosis (DMLAT_DAT)
dmlat_dat = (
    selected_events.where(selected_events.snomedct_code.is_in(dm_cod))
    .sort_by(selected_events.date)
    .last_for_patient()
    .date
)

# Date of the latest diabetes resolved code (DMRES_DAT)
dmres_dat = (
    selected_events.where(selected_events.snomedct_code.is_in(dmres_cod))
    .sort_by(selected_events.date)
    .last_for_patient()
    .date
)

# Patient age at the end of each interval (PAT_AGE)
pat_age = patients.age_on(INTERVAL.end_date)

# Numerator
# Rule 1: Latest diabetes diagnosis is not followed by a diabetes resolved code
dm_reg_r1 = (dmres_dat < dmlat_dat) | (dmlat_dat.is_not_null() & dmres_dat.is_null())
# Rule 2: Patient is aged 17 years or older
dm_reg_r2 = pat_age >= 17
dm017_numerator = dm_reg_r1 & dm_reg_r2

# Denominator
dm017_denominator = practice_registrations.exists_for_patient_on(INTERVAL.end_date)

# Define measures
measures.define_measure(
    name="dm017",
    numerator=dm017_numerator,
    denominator=dm017_denominator,
    group_by={"sex": patients.sex},
    intervals=months(12).starting_on("2023-04-01"),
)
