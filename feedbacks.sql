DROP DATABASE IF EXISTS feedbacks;
create database feedbacks;
\c feedbacks;
create table feedbacks(
feedback_no serial primary key,
response1 text,
response2 text,
response3 text
);