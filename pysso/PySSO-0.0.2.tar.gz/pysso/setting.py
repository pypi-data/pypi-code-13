#all settings 
SET_SYSTEM_NAME = 'system_name' 

def get( conn, name ):
    cursor = conn.cursor()
    sql = "select value from setting where name=%s"
    cursor.execute(sql, (name,))
    value = cursor.fetchone()
    
    return value.get( 'value' )

