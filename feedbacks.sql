DROP DATABASE IF EXISTS feedbacks;
create database feedbacks;
\c feedbacks;
DROP TABLE IF EXISTS feedbacks;
create table feedbacks(
feedback_no serial primary key,
response1 text,
response2 text,
response3 text,
response4 text
);
