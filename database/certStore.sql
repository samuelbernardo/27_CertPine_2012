# código para geração da BD para certificados

CREATE TABLE certs (
  serialNumber varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  subjectName varchar(255) NOT NULL,
  notBefore varchar(255) NOT NULL,
  notAfter varchar(255) NOT NULL,
  timesChecked int,
  valid int,
  PRIMARY KEY (serialNumber, issuerName),
  CHECK (timesChecked > 0)
);

CREATE TABLE certs (
  serialNumber varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  rawData text NOT NULL,
  PRIMARY KEY (serialNumber, issuerName),
  CHECK (timesChecked > 0)
);

