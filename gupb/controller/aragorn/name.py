OUR_BOT_NAME = 'Aragorn'
current_name = OUR_BOT_NAME

def get_current_name():
    global current_name
    return current_name

def set_fake_name(fake_name):
    global current_name
    current_name = fake_name

def restore_name():
    global current_name
    current_name = OUR_BOT_NAME
