CREATE USER 'depl'@'%' IDENTIFIED BY 'depl@0369';
GRANT ALL PRIVILEGES ON test_databasee.* TO 'depl'@'%';

FLUSH PRIVILEGES;
