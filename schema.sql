drop table if exists courses;
create table courses(
  id integer primary key autoincrement,
  name text not null,
  url text not null,
  description text
);