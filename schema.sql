CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY,
    company TEXT NOT NULL CHECK (length(company) <= 127),
    position TEXT NOT NULL CHECK (length(position) <= 63),
    wage REAL CHECK (wage IS NULL OR wage >= 0),
    status TEXT NOT NULL DEFAULT 'Applied'
        CHECK (
            status IN (
                'Applied',
                'Waiting for Interview',
                'Interviewed',
                'Offer',
                'Rejected',
                'Withdrawn',
                'Other'
            )
        ),
    application_date TEXT
        CHECK (
            application_date IS NULL
            OR (
                length(application_date) = 10
                AND application_date GLOB
                    '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
            )
        ),
    notes TEXT
        CHECK (
            notes IS NULL
            OR length(notes) <= 2000
        ),
    job_url TEXT
        CHECK (
            job_url IS NULL
            OR length(job_url) <= 2048
        )
);
