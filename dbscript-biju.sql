create database joycebiju;

\c joycebiju;

create table product(
	prod_id SERIAL PRIMARY KEY,
	prod_name varchar(100) NOT NULL,
	prod_description varchar(500),
	prod_collection smallint,
	prod_section smallint,
	prod_price real NOT NULL);

create table highlight(
	highlight_id SERIAL PRIMARY KEY,
	highlight_name varchar(100) NOT NULL,
	highlight_description varchar(500));

CREATE table section(
	section_id SERIAL PRIMARY KEY,
	section_name VARCHAR(50) NOT NULL);

CREATE table collection(
	collection_id SERIAL PRIMARY KEY,
	collection_name VARCHAR(50) NOT NULL);

insert into section(section_name)
values
('brinco'),
('pulseira'),
('anel'),
('colar'),
('destaque'); 

insert into collection(collection_name)
values
('colecao de verao'),
('colecao de inverno'),
('colecao de primavera'),
('colecao de outono'); 

\dt;