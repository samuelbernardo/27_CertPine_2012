# código para geração da BD para certificados

CREATE TABLE certs (
  serialNumber varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  domainName varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  timesChecked int,
  valid int,
  PRIMARY KEY (serialNumber, issuerName),
  CHECK (timesChecked > 0)
);

CREATE TABLE certs (
  serialNumber varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  rawData varchar(5000) NOT NULL,
  PRIMARY KEY (serialNumber, issuerName),
  CHECK (timesChecked > 0)
);

