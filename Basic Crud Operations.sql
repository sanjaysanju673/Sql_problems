---
---@Author: v sanjay kumar
---@Date: 2024-08-22 10:00:30
---@Last Modified by: v sanjay kumar
---@Last Modified time: 2024-08-22 10:00:30
---@Title :Crud operations



---Crateing the Database

CREATE DATABASE Cruddb;

---Creating the table in database

Create TABLE EMPLOYEE(
  Employee_id int primary key,
  First_name varchar(20),
  last_name  varchar(20),
  salary     int);


---Fetching the data from database
select * from EMPLOYEE


---Insert the values into employee table

INSERT INTO EMPLOYEE(Employee_id, First_name,last_name,salary)
VALUES 
(1,'sanjay', 'kumar', 1000),
(2,'sita', 'ramaraju', 2000),
(3,'girish', 'Shekar', 3000),
(4,'ramya', 'Krishna', 4000),
(5,'rama', 'raja', 5000),
(6,'navven', 'naik', 6000),
(7,'rahul', 'j', 7000);

---Read the colomns in table
select * from EMPLOYEE


---Adding the colume
ALTER TABLE EMPLOYEE
ADD email varchar(20)

---Update the colume
UPDATE EMPLOYEE
SET email = CASE Employee_id
    WHEN 1 THEN 'san@gmail.com'
    WHEN 2 THEN 'jdfjd@gmail.com'
    WHEN 3 THEN 'r77@gmail.com'
    WHEN 4 THEN 'r2@gmail.com'
    WHEN 5 THEN 'r11@gmail.com'
    WHEN 6 THEN 'r11@gmail.com'
	WHEN 7 THEN 'ee2@gmail.com'
    ELSE email
END
WHERE Employee_id IN (1, 2, 3, 4, 5, 6,7);

---Delete The column in table

delete from Employee
where Employee_id =4

--=update the colomn
Update Employee
set First_name='raju',last_name='cr',salary=5000
where First_name='rama'
 

