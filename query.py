randomQuery = '''SELECT
	bookname || ' ' || arabicnumber || char(10) || char(10) || text || char(10) || char(10) || replace(replace(grades,
	' && ',
	char(10)),
	'::',
	' - ') || char(10) || 'hadithhub.com/' || shortname || ':' || hadithnumber as "hadith"
FROM
	hadith
WHERE
	length(text) > 10
	and length(hadithnumber) + length(arabicnumber) + length (text) + length (grades) + length (bookname) + length (shortname) < 280
	and "language" = "eng"
	and text not like '%chain%'
	and text not like '%authority%'
	and text not like '%same%'
	and text not like '%similar%'
	and text not like '%hadith%'
	and text not like '%above%'
ORDER BY
	RANDOM()
LIMIT 1;'''