

def valid_int_input(msg, start = 0, end = None):
    while True:
        try:
            inp = int(input(msg))
            if start is not None and end is not None and (inp < start or inp > end):
                print(f"input must be >= {start} and <= {end}")
                continue
            return inp

            
        except ValueError:
            print("Invalid input, plz Enter a valid input: ")



def get_menu_choice(top_msg, messages):
    print(f'\n{top_msg}')

    messages = [f'{idx+1}) {msg}' for idx, msg in enumerate(messages)]
    print('\n'.join(messages))

    msg = f'Enter your choice (from 1 to {len(messages)}): '
    return valid_int_input(msg, 1, len(messages))