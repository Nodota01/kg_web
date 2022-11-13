DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  phone TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password TEXT NOT NULL,
  age INTEGER NOT NULL,
  gender TEXT NOT NULL,
  email TEXT,
  address TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user (phone, name, password, age, gender, email, address) VALUES ('17688888888', '田所浩二', 'pbkdf2:sha256:260000$aDGiF8hQNDkHWtzz$80f75b5c1f286bba110476de4b75fe63e557720bf1805cb443881d2837ad4806', 24, '男', '114514@qq.com', '东京下北泽');