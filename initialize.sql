-- initialize.sql
-- Rebuilds the users/posts schema and seed data from scratch.
-- Safe to rerun: existing tables are dropped first (posts before users,
-- since posts depends on users).

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

-- ---------------------------------------------------------------
-- Tables
-- ---------------------------------------------------------------

CREATE TABLE users (
    user_id     INT          NOT NULL PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    email       VARCHAR(100) NOT NULL UNIQUE,
    full_name   VARCHAR(100) NOT NULL,
    created_at  DATETIME     NOT NULL
);

CREATE TABLE posts (
    post_id     INT          NOT NULL PRIMARY KEY,
    user_id     INT          NOT NULL,
    title       VARCHAR(200) NOT NULL,
    body        TEXT,
    likes       INT          NOT NULL DEFAULT 0,
    posted_at   DATETIME     NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ---------------------------------------------------------------
-- Seed data: users
-- ---------------------------------------------------------------

INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (1,  'adalove',   'ada@example.com',     'Ada Lovelace',      '2026-01-05 09:15:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (2,  'ghopper',   'grace@example.com',   'Grace Hopper',      '2026-01-07 14:30:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (3,  'aturing',   'alan@example.com',    'Alan Turing',       '2026-01-10 08:00:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (4,  'kjohnson',  'katherine@example.com','Katherine Johnson', '2026-01-12 11:45:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (5,  'dknuth',    'donald@example.com',  'Donald Knuth',      '2026-01-15 16:20:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (6,  'mhamilton', 'margaret@example.com','Margaret Hamilton', '2026-01-18 10:05:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (7,  'ecodd',     'edgar@example.com',   'Edgar Codd',        '2026-01-21 13:10:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (8,  'bliskov',   'barbara@example.com', 'Barbara Liskov',    '2026-01-24 09:40:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (9,  'lpage',     'larry@example.com',   'Larry Page',        '2026-01-27 17:25:00');
INSERT INTO users (user_id, username, email, full_name, created_at) VALUES (10, 'fallen',    'frances@example.com', 'Frances Allen',     '2026-01-30 12:00:00');

-- ---------------------------------------------------------------
-- Seed data: posts (every user_id references an existing user)
-- ---------------------------------------------------------------

INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (1,  1,  'Notes on the Analytical Engine', 'The engine might compose elaborate pieces of music.',        42, '2026-02-01 10:00:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (2,  2,  'Found an actual bug',            'Moth trapped in relay #70, panel F. First actual case.',     87, '2026-02-02 15:47:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (3,  3,  'Can machines think?',            'I propose to consider the question...',                      65, '2026-02-03 09:30:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (4,  4,  'Checking the orbital math',      'Ran the trajectory numbers by hand before launch.',          53, '2026-02-04 08:15:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (5,  5,  'Premature optimization',         'It is the root of all evil (or at least most of it).',       71, '2026-02-05 13:00:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (6,  6,  'Priority displays saved Apollo', 'Error-handling in the guidance computer did its job.',       60, '2026-02-06 20:17:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (7,  7,  'A relational model of data',     'Data should be organized as relations, not hierarchies.',    48, '2026-02-07 11:11:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (8,  2,  'COBOL turns 67',                 'Programs should read like English.',                         29, '2026-02-08 16:45:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (9,  8,  'Substitutability matters',       'Subtypes must be usable wherever the base type is.',         37, '2026-02-09 10:30:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (10, 9,  'Ranking pages by links',         'A page is important if important pages link to it.',         55, '2026-02-10 14:20:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (11, 10, 'Compilers and optimization',     'Program optimization through control-flow analysis.',        33, '2026-02-11 09:05:00');
INSERT INTO posts (post_id, user_id, title, body, likes, posted_at) VALUES (12, 3,  'On computable numbers',          'Some numbers cannot be computed by any machine.',            44, '2026-02-12 12:40:00');
