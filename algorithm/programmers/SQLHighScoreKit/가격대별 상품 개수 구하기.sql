-- 코드를 입력하세요

-- 내 풀이 case when 안나누고 어캐하지?
SELECT
    case
        when price < 10000 then 0
        when 10000 <= price and price < 20000 then 10000
        when 20000 <= price and price < 30000 then 20000
        when 30000 <= price and price < 40000 then 30000
        when 40000 <= price and price < 50000 then 40000
        when 50000 <= price and price < 60000 then 50000
        when 60000 <= price and price < 70000 then 60000
        when 70000 <= price and price < 80000 then 70000
        when 80000 <= price and price < 90000 then 80000
    end as price_group, count(*) products
from product
group by price_group
order by price_group;

-- 다른 사람 풀이
SELECT  TRUNCATE((price / 10000),0) * 10000 AS PRICE_GROUP , COUNT(PRODUCT_ID) AS PRODUCTS
FROM PRODUCT
GROUP BY PRICE_GROUP
ORDER BY PRICE_GROUP ASC

-- 다른 사람 풀이2
SELECT
    floor(price/10000)*10000 as price_group, count(product_id)
from product
group by price_group
order by price_group asc;