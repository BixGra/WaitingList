CREATE TABLE events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    thumbnail_url TEXT,
    organization_id TEXT NOT NULL,
    venue_name TEXT NOT NULL,
    venue_address TEXT,
    timezone TEXT NOT NULL
);

CREATE TABLE representations (
    id TEXT NOT NULL,
    event_id TEXT NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL
);

CREATE TABLE offers (
    offer_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    max_quantity_per_order INTEGER NOT NULL,
    description TEXT
);

CREATE TABLE inventory (
    inventory_id TEXT PRIMARY KEY,
    offer_id TEXT NOT NULL,
    representation_id TEXT NOT NULL,
    total_stock INTEGER NOT NULL,
    available_stock INTEGER NOT NULL,
    waiting_list_open BOOLEAN DEFAULT FALSE
);

CREATE TABLE waiting_list (
    user_id TEXT,
    offer_id TEXT,
    representation_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    tickets_wanted INTEGER NOT NULL,
    status TEXT DEFAULT 'waiting',
    PRIMARY KEY (user_id,offer_id,representation_id)
);

COPY events(id,title,description,thumbnail_url,organization_id,venue_name,venue_address,timezone)
FROM '/docker-entrypoint-initdb.d/data/events.csv' DELIMITER ','  CSV HEADER;

COPY representations(id,event_id,start_datetime,end_datetime)
FROM '/docker-entrypoint-initdb.d/data/representations.csv' DELIMITER ','  CSV HEADER;

COPY offers(offer_id,event_id,name,type,max_quantity_per_order,description)
FROM '/docker-entrypoint-initdb.d/data/offers.csv' DELIMITER ','  CSV HEADER;

COPY inventory(inventory_id,offer_id,representation_id,total_stock,available_stock)
FROM '/docker-entrypoint-initdb.d/data/inventory.csv' DELIMITER ','  CSV HEADER;

UPDATE inventory
SET waiting_list_open = True WHERE available_stock = 0;