BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "PatientStatus" (
	"SSN_ID"	INTEGER NOT NULL,
	"PatientID"	INTEGER UNIQUE,
	"Name"	VARCHAR(20) NOT NULL,
	"Age"	INTEGER,
	"DOJ"	VARCHAR(20),
	"BedType"	VARCHAR(20),
	"Address"	VARCHAR(30),
	"State"	VARCHAR(20),
	"City"	VARCHAR(20),
	"Status"	VARCHAR(20),
	PRIMARY KEY("SSN_ID")
);
CREATE TABLE IF NOT EXISTS "userstore" (
	"username"	VARCHAR(20) NOT NULL,
	"password"	VARCHAR(20),
	"timestamp"	DATETIME,
	PRIMARY KEY("username")
);
CREATE TABLE IF NOT EXISTS "DiagnosticsTable2" (
	"TestID"	INTEGER NOT NULL,
	"TestName"	VARCHAR(50) NOT NULL,
	"TestCharge"	FLOAT,
	PRIMARY KEY("TestID")
);
CREATE TABLE IF NOT EXISTS "DiagnosticsTable1" (
	"PatientID"	INTEGER NOT NULL,
	"TestID"	INTEGER UNIQUE,
	PRIMARY KEY("PatientID")
);
CREATE TABLE IF NOT EXISTS "MedicineTable2" (
	"MedicineID"	INTEGER NOT NULL,
	"MedName"	VARCHAR(50) NOT NULL,
	"AvlQty"	INTEGER,
	"Rate"	FLOAT,
	PRIMARY KEY("MedicineID")
);
CREATE TABLE IF NOT EXISTS "MedicineTable1" (
	"PatientID"	INTEGER NOT NULL,
	"MedicineID"	INTEGER UNIQUE,
	"Quantity"	INTEGER,
	PRIMARY KEY("PatientID")
);
INSERT INTO "PatientStatus" ("SSN_ID","PatientID","Name","Age","DOJ","BedType","Address","State","City","Status") VALUES (123131344,461364240,'Rajat Mohanty',21,'2020-06-27','Single room','Samantara pur','Odisha','Odisha','Active'),
 (545555555,932494473,'Deepak Pandey',21,'2020-06-02','General Ward','Samantara pur','Odisha','Odisha','Active');
INSERT INTO "userstore" ("username","password","timestamp") VALUES ('REG1234567','1234567890',NULL);
COMMIT;
