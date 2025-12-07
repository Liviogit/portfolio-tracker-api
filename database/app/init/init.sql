DROP TABLE IF EXISTS trades;
DROP TABLE IF EXISTS portfolios;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    password TEXT
);

CREATE TABLE portfolios (
    portfolio_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    last_amount NUMERIC(12, 2) NOT NULL,
    initial_amount NUMERIC(12, 2) NOT NULL,
    positions TEXT,
    positions_size TEXT,
    portfolio_name TEXT,
    portfolio_date  TIMESTAMP DEFAULT NOW(),
    cash_balance NUMERIC(12, 2) NOT NULL DEFAULT 0
);

CREATE TABLE trades (
    trade_id SERIAL PRIMARY KEY, 
    portfolio_id INT NOT NULL REFERENCES portfolios(portfolio_id) ON DELETE CASCADE,
    asset_name TEXT NOT NULL,
    action VARCHAR(4) NOT NULL CHECK (action IN ('BUY', 'SELL')),
    price NUMERIC(12, 2) NOT NULL,
    quantity NUMERIC(12, 2) NOT NULL,
    trade_date TIMESTAMP DEFAULT NOW(),
    description TEXT
);


-- Users
COPY users(user_id,first_name, last_name, username, password)
FROM '/docker-entrypoint-initdb.d/data/users.csv'
DELIMITER ','
CSV HEADER;

-- Portfolios
COPY portfolios(portfolio_id,user_id, last_amount, initial_amount, positions, positions_size, portfolio_name, portfolio_date,cash_balance)
FROM '/docker-entrypoint-initdb.d/data/portfolios.csv'
DELIMITER ','
CSV HEADER;

-- Trades
COPY trades(trade_id,portfolio_id, asset_name, action, price, quantity, trade_date, description)
FROM '/docker-entrypoint-initdb.d/data/trades.csv'
DELIMITER ','
CSV HEADER;

SELECT setval('users_user_id_seq', (SELECT MAX(user_id)+1 FROM users));
SELECT setval('portfolios_portfolio_id_seq', (SELECT MAX(portfolio_id)+1 FROM portfolios));
SELECT setval('trades_trade_id_seq', (SELECT MAX(trade_id)+1 FROM trades));