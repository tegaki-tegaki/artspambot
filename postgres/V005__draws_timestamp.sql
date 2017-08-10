ALTER TABLE draws ADD COLUMN ctime timestamptz DEFAULT now();

UPDATE draws SET ctime = now();

ALTER TABLE draws ALTER ctime SET NOT NULL;
