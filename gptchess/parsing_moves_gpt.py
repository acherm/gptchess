import re 

# extract the move from the response of ChatGPT
# many "tricks" and ad-hoc observations to fix the output of ChatGPT
# bonus: promotion is sometimes badly handled (eg "6... b8=" instead of b8=Q) for some reasons, so we automatically promote to Queen
def extract_move_chatgpt(resp_str, auto_promotion=True):  

    # determines when the digits end
    for i in range(0, len(resp_str)):
        if resp_str[i].isdigit():
            continue
        else:
            break
    resp_str = resp_str[i:]

    res_str = ''

    if resp_str[0:3] == '...':
        res_str = resp_str[3:].strip().split()[0]
    elif resp_str[0:1] == '.':
        # extract the substring right after the dot and stops until finding a space or the end of the string
        res_str = resp_str[1:].strip().split()[0]
    else:
        res_str = resp_str.strip().split()[0]


    if res_str.endswith('=') and auto_promotion:
        # add the promotion piece Q to the end of res_str
        res_str += 'Q'

    return res_str
    

    # match = re.match(r'^(\d+\.{1,3}\s*)?(O-O-O|O-O|[a-h][1-8]=?[a-zA-Z0-9]*|[a-zA-Z0-9]+[+#!?]?)(?=\s|\d+\.|$)', resp_str)
    # if match:
    #    return match.group(2)
    # else:
    #    return resp_str.strip().split()[0]
# print(extract_move_chatgpt("10... f7"))
# exit()