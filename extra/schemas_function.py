
def scheme_user(user_row):
    return {
        'user_name':user_row[0],
        'first_name':user_row[1],
        'last_name':user_row[2],
        'email':user_row[3],
        'category':user_row[4],
        'phone':user_row[5],
        'disabled':user_row[6]
    }

def scheme_user_db(user_row):
    return {
        'user_name':user_row[0],
        'password':user_row[1],
        'first_name':user_row[2],
        'last_name':user_row[3],
        'email':user_row[4],
        'category':user_row[5],
        'phone':user_row[6],
        'disabled':user_row[7]
    }