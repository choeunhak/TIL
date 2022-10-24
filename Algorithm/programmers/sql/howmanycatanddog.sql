SELECT ANIMAL_TYPE, count(animal_type) as count
from animal_ins
group by animal_type
having ANIMAL_TYPE='Dog' or ANIMAL_TYPE='Cat'
order by ANIMAL_TYPE