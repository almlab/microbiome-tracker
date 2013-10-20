drop table if exists person;
drop table if exists food;
drop table if exists wellness;

create table person (
  id_person integer primary key autoincrement,
  username text not null,
  password text not null
);

create table food (
  id_food integer primary key autoincrement,
  file_location text not null,
  time_stamp timestamp DEFAULT CURRENT_TIMESTAMP,
  location_stamp text,
  annotation text,
  trackperson int,
  FOREIGN KEY(trackperson) REFERENCES person(id_person)
);

create table wellness (
  id_wellness integer primary key autoincrement,
  wellness_index integer,
  trackperson int,
  FOREIGN KEY(trackperson) REFERENCES person(id_person)
);

insert into person (username, password) values ('admin', 'default');