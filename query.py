def randomQuery(length):
    return '''
select
        h2.text araHadith,
        h1.text engHadith,
        h1.bookname || ' ' || h1.arabicnumber reference,
        'hadithhub.com/' || h1.shortname || ':' || h1.hadithnumber link,
        h1.grades
    from
        hadith h2 
    inner join
        (
            SELECT
                h1.text,
                h1.bookname,
                h1.shortname,
                h1.arabicnumber,
                h1.hadithnumber,
                h1.grades
            FROM
                hadith h1 
            WHERE
                length(text) > 10    
  and length(hadithnumber) + length(arabicnumber) + length (text) + length (grades) + length (bookname) + length (shortname) < {} 
                and "language" = "eng"    
                and text not like '%chain%'    
                and text not like '%authority%'    
                and text not like '%same%'    
                and text not like '%similar%'    
                and text not like '%hadith%'    
                and text not like '%above%'  
            ORDER BY
                RANDOM()  LIMIT    1
        ) h1 
            on h1.shortname = h2.shortname 
            and h1.hadithnumber = h2.hadithnumber   
    Where
        h2.language = 'ara' LIMIT 1;
'''.format(length)
