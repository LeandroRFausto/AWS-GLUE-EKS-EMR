bronze_dict = {
    "customers":["id","nome","sexo","nascimento","profissao"],
    "credit_score":["customer_id","nome","provedor","credit_score"],
    "music":["customer_id","genero","instrumento","categoria"]
}

silver_dict = {
    "customers":"""
                    select 
                        id, 
                        nome, 
                        sexo, 
                        nascimento, 
                        profissao,
                        floor(datediff(now(),nascimento)/365.25) as idade, 
                        case when floor(datediff(now(),nascimento)/365.25) > 60 then 'idoso'
                             when floor(datediff(now(),nascimento)/365.25) > 30 then 'adulto'
                             when floor(datediff(now(),nascimento)/365.25) > 15 then 'jovem'
                             else 'crianca' end as categoria_idade
                    from customers
                """,
                
    "credit_score":"""
                    select
                        customer_id as id_cliente,
                        nome,
                        provedor,
                        credit_score as pontuacao,
                        case when credit_score > 800 then 'Muito_alto'
                                when credit_score > 550 then 'Alto'
                                when credit_score > 350 then 'Medio'
                                when credit_score > 150 then 'Baixo'
                                else 'Muito_baixo' end as categoria_credito
                    from credit_score
                """,

    "music":"""
                    select 
                        customer_id as id_cliente,
                        genero,
                        instrumento,
                        categoria,
                        case genero 
                        when 'Anime' then 'possivelmente'
                        else 'inconclusivo' end as geek
                    from music
            """
}

gold_list = ["mysql/lrfawsmysql/customers", "mysql/lrfawsmysql/credit_score", "mysql/lrfawsmysql/music"]


gold_dict = {
    "customers_credit":"""
                                select distinct
                                    c.id, 
                                    c.nome, 
                                    c.sexo, 
                                    c.nascimento, 
                                    c.profissao,
                                    cs.credit_score
                                from customers as c
                                left join credit_score as cs on cs.id = c.id
                """,

    "customers_music":"""
                                select distinct
                                    c.id, 
                                    c.nome, 
                                    c.sexo, 
                                    c.nascimento, 
                                    c.profissao,
                                    m.genero
                                from customers as c
                                left join music as m on m.id = c.id
                """
}
