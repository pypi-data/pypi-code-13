__version__ = '0.1.0'

def greet_dude_with_food(dude_name, food_today, num_question_marks):
    return "Hey {dude_name}! Want a {food_today} today{q_marks}".format(
        dude_name=dude_name,
        food_today=food_today,
        q_marks='?'*num_question_marks)
