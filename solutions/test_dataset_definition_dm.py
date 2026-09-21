# Solution for Task 6: Write assurance tests for your dataset definition
# Run the codelist commands from step 2 of Task 1b before running this file

from datetime import date
from dataset_definition_dm import dataset

test_data = {
    # Correctly not expected in population
    # No clinical events
    1: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [{"start_date": date(2010, 1, 1)}],
        "clinical_events": [{}],
        "expected_in_population": False,
    },
    # Correctly expected in population
    # Diabetes diagnosis and no diabetes resolved code
    2: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [{"start_date": date(2010, 1, 1)}],
        "clinical_events": [
            {"date": date(2020, 1, 1), "snomedct_code": "111552007"},
        ],
        "expected_in_population": True,
        "expected_columns": {
            "dmlat_dat": date(2020, 1, 1),
            "dmres_dat": None,
            "pat_age": 74,
        },
    },
    # Correctly not expected in population
    # Diabetes resolved code after the latest diabetes diagnosis (rule 1)
    3: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "practice_registrations": [{"start_date": date(2010, 1, 1)}],
        "clinical_events": [
            {"date": date(2020, 1, 1), "snomedct_code": "111552007"},
            {"date": date(2021, 1, 1), "snomedct_code": "315051004"},
        ],
        "expected_in_population": False,
    },
    # Correctly not expected in population
    # Aged under 17 years old on the index date (rule 2)
    4: {
        "patients": {"date_of_birth": date(2010, 1, 1)},
        "practice_registrations": [{"start_date": date(2010, 1, 1)}],
        "clinical_events": [
            {"date": date(2020, 1, 1), "snomedct_code": "111552007"},
        ],
        "expected_in_population": False,
    },
}
