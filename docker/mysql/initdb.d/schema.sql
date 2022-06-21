CREATE TABLE person(
    person_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    document INT NOT NULL UNIQUE,
    dateOfBirth DATE,
    PRIMARY KEY (person_id)
);

CREATE TABLE animal(
    animal_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    cost FLOAT NOT NULL,
    species VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    PRIMARY KEY (animal_id),
    CONSTRAINT UC_Animal UNIQUE (name, species, owner_id)
);

CREATE TABLE species(
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (name)
);

ALTER TABLE animal
ADD FOREIGN KEY(owner_id)
REFERENCES person(person_id)
ON DELETE CASCADE;

ALTER TABLE animal
ADD FOREIGN KEY(species)
REFERENCES species(name)
ON DELETE CASCADE;