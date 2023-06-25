BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> a2a3deb4e461

CREATE TABLE users (
    id SERIAL NOT NULL, 
    balance INTEGER NOT NULL, 
    PRIMARY KEY (id)
);

INSERT INTO alembic_version (version_num) VALUES ('a2a3deb4e461') RETURNING alembic_version.version_num;

COMMIT;

