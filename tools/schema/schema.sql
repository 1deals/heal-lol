CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT UNIQUE NOT NULL,
    prefix VARCHAR(5)
);

CREATE SCHEMA IF NOT EXISTS voicemaster;

CREATE TABLE IF NOT EXISTS voicemaster.configuration (
    guild_id BIGINT UNIQUE NOT NULL,
    channel_id BIGINT UNIQUE NOT NULL,
    interface_id BIGINT UNIQUE NOT NULL,
    category_id BIGINT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS voicemaster.channels (
    guild_id BIGINT  NOT NULL,
    owner_id BIGINT NOT NULL,
    channel_id BIGINT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS forcenick (
    guild_id BIGINT, 
    user_id BIGINT, 
    name TEXT,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE IF NOT EXISTS welcome (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    message TEXT
);

CREATE TABLE IF NOT EXISTS afk (
    user_id BIGINT PRIMARY KEY,
    status TEXT,
    time BIGINT
);

CREATE TABLE IF NOT EXISTS blacklist (
    user_id BIGINT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS afk (
    user_id BIGINT PRIMARY KEY,
    status TEXT,
    time BIGINT
);

CREATE TABLE IF NOT EXISTS joinping (
    guild_id BIGINT,
    channel_id BIGINT,
    PRIMARY KEY (guild_id, channel_id)
);

CREATE TABLE IF NOT EXISTS vape (
    user_id BIGINT PRIMARY KEY,
    flavor TEXT,
    hits BIGINT
);

CREATE TABLE IF NOT EXISTS premium (
    user_id BIGINT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS uwulock (
    guild_id BIGINT, 
    user_id BIGINT
);

CREATE TABLE IF NOT EXISTS selfprefix (
    user_id BIGINT PRIMARY KEY,
    prefix TEXT
);

CREATE TABLE IF NOT EXISTS globalban (
    user_id BIGINT
);

CREATE TABLE IF NOT EXISTS usage (
    amount BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS restore (
    guild_id BIGINT,
    user_id BIGINT,
    role BIGINT,
    PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE IF NOT EXISTS lastfm(
    user_id BIGINT PRIMARY KEY,
    lfuser TEXT,
    mode TEXT,
    command TEXT
);