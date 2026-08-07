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
                'Withdrawn'
            )
        )
);