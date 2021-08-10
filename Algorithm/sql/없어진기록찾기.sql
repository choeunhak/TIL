--첫번째 풀이

select animal_id, name
from animal_outs
where animal_id not in (
SELECT animal_id
from animal_ins)
order by animal_id

--두번째 풀이 distinct, 활용
SELECT distinct B.ANIMAL_ID, B.NAME
FROM ANIMAL_INS A, ANIMAL_OUTS B
WHERE B.ANIMAL_ID NOT IN (SELECT ANIMAL_ID FROM ANIMAL_INS)
ORDER BY ANIMAL_ID