create table source_files (
	id integer PRIMARY KEY autoincrement, 
	filename varchar(255) NOT NULL, 
	processed datetime
);

create table processed_data (
	id integer PRIMARY KEY autoincrement,  
	LKG varchar(255) NOT NULL,
	target integer,
	source_file integer NOT NULL,
	CONSTRAINT fk_source_files 
	FOREIGN KEY (source_file) 
	REFERENCES source_files(id) 
	ON DELETE CASCADE
);