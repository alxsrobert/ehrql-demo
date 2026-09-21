# Solution for the depression example
# The depression codelists are already in the codelists/ folder

from ehrql import create_dataset, codelist_from_csv
from ehrql.tables.tpp import patients, clinical_events

index_date = "2024-03-31"

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

# Depression codelists
dep_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-depr_cod.csv",
    column="code",
)
dep_resolved_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-depres_cod.csv",
    column="code",
)

# Patient is alive on the index date
dataset.is_alive = patients.is_alive_on(index_date)

# Patient age on the index date
dataset.age = patients.age_on(index_date)

# Date of the latest depression diagnosis
dataset.last_dep_diagnosis_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dep_codes))
    .where(clinical_events.date.is_on_or_before(index_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# Date of the latest depression resolved code
dataset.last_dep_resolved_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dep_resolved_codes))
    .where(clinical_events.date.is_on_or_before(index_date))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# Patient is aged 17 years or older
dataset.aged_17_or_older = dataset.age >= 17

# Patient has an unresolved depression diagnosis
dataset.has_unresolved_depression = dataset.last_dep_diagnosis_date.is_not_null() & (
    dataset.last_dep_resolved_date.is_null()
    | (dataset.last_dep_resolved_date < dataset.last_dep_diagnosis_date)
)

# Define population
dataset.define_population(
    dataset.is_alive & dataset.aged_17_or_older & dataset.has_unresolved_depression
)
