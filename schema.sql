drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  username text not null,
  start_time text not NULL,
  end_time text not NULL
);

