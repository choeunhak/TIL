-- mysql 기준

-- 날짜 계산
year(<컬럼명>), month(<컬럼명>)

-- case when end 분기처리
SELECT name,
       CASE
           WHEN age < 18 THEN 'Child'
           WHEN age >= 18 AND age <= 64 THEN 'Adult'
           ELSE 'Senior'
       END AS age_group
FROM users;

-- truncate문