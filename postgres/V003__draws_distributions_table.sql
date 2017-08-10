CREATE TABLE uploads (
    upload BIGSERIAL PRIMARY KEY,

    domain_name text,

    draw integer REFERENCES draws
);
