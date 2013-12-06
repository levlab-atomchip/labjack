CREATE TABLE system_states (
    _id serial PRIMARY KEY,
    name text
);

CREATE TABLE sensors (
    _id serial PRIMARY KEY,
    name text NOT NULL,
    unit text NOT NULL,
    channel REFERENCES channels NOT NULL,
    postprocessor REFERENCES postprocessors NOT NULL,
    install_date timestamp DEFAULT CURRENT_TIMESTAMP,
    remove_date timestamp CONSTRAINT remove_after_install CHECK (remove_date > install_date),
    environmental boolean,
    installed boolean,
    faulted boolean,
    description text
);

PREPARE sensor_add(text, text, text, text, boolean, text) AS
INSERT INTO sensors (name, unit, channel, postprocessor, install_date, remove_date, environmental, installed, faulted, description)
SELECT $1, $2, c._id, p._id, DEFAULT, null, $5, false, false, $6
FROM channels c, postprocessors p
WHERE c.name = $3
AND p.name = $4
;

CREATE TABLE states_sensors_map (
    state_id REFERENCES system_states NOT NULL,
    sensor_id REFERENCES sensors NOT NULL
);

CREATE TABLE sensor_data (
    sensor REFERENCES sensors NOT NULL ON DELETE RESTRICT,
    time timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    value float NOT NULL,
    system_state REFERENCES system_states
);

CREATE TABLE runs (
    _id serial PRIMARY KEY,
    start_time timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    end_time timestamp CONSTRAINT end_after_start CHECK (end_time > start_time) NOT NULL,
    name text
);

CREATE TABLE annotations (
    sensor REFERENCES sensors NOT NULL ON DELETE RESTRICT,
    time timestamp NOT NULL,
    description text NOT NULL
);

CREATE TABLE channels (
    _id serial PRIMARY KEY,
    DAQ REFERENCES daqs,
    type REFERENCES channel_types,
    driver REFERENCES drivers,
    name text,
    address text
);

PREPARE channel_add(text, text, text, text, text) AS
INSERT INTO channels (DAQ, type, driver, name, address)
SELECT d._id, t._id, dr._id, $4, $5
FROM daqs d, channel_types t, drivers dr
WHERE d.name = $1
AND t.name = $2
AND dr.name = $3
;

CREATE TABLE daqs (
    _id serial PRIMARY KEY,
    name text UNIQUE
);

CREATE TABLE channel_types(
    _id serial PRIMARY KEY,
    name text UNIQUE
);

CREATE TABLE drivers (
    _id serial PRIMARY KEY,
    name text UNIQUE,
);

CREATE TABLE postprocessors(
    _id serial PRIMARY KEY,
    name text UNIQUE,
);

INSERT INTO channel_types name VALUES 'AIN24';
INSERT INTO daqs name VALUES 'MIMIR_Labjack';
INSERT INTO postprocessors name VALUES 'raw_result';
INSERT INTO drivers name VALUES 'AIN24_Driver';

EXECUTE channel_add('MIMIR_Labjack', 'AIN24', 'AIN24_Driver', 'MIMIR_AIN0', '0');
EXECUTE sensor_add('Test Photodiode', 'Volts', 'MIMIR_AIN0', 'raw_result', true, 'DET36A Photodiode for testing data logging');
