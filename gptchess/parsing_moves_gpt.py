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

def extract_move_deepseek_withGPT4(resp_str):
    """
    Extract chess moves from DeepSeek's responses using GPT-4 with improved pre/post processing.
    Returns the move in standard algebraic notation (e.g., 'e4', 'Nf3', 'O-O').
    """
    try:
        from openai import OpenAI
        import os
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        if not client.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        prompt = f"""From the following text, extract the most relevant chess move in standard algebraic notation (e.g., 'e4', 'Nf3', 'O-O'). 
        There can be multiple moves in the text, so extract the last one or the one that is played or retained.
        - Return only the final move, without any extra text, numbers, or formatting.
        - Always include the promotion piece for pawn promotions (e.g., 'e8=Q').
        - Include symbols for check (+) or checkmate (#) if present.
        - If no valid move is found, return 'invalid'.
        
        Input: {resp_str}"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        
        move = response.choices[0].message.content.strip()
        
        # Post-process the extracted move to handle any leading numbers or dots
        for i in range(0, len(move)):
            if move[i].isdigit() or move[i] == '.':
                continue
            else:
                move = move[i:]
                break
        
        # Handle promotion edge case
        if move.endswith('='):
            move += 'Q'  # Default to queen promotion
            
        return move.strip()
            
    except Exception as e:
        print(f"GPT-4 extraction failed: {e}")
        
    
    return None

def extract_move_deepseek(resp_str):
    """
    Extract chess moves from DeepSeek's responses using <played_move> tags.
    Returns the move in standard algebraic notation (e.g., 'Qg4').
    """
    import re

    # Use regex to find the <played_move> tags and extract the move
    match = re.search(r'<played_move>(.*?)</played_move>', resp_str)
    if match:
        move = match.group(1).strip()  # Return the move without extra spaces
        
        # Post-process the extracted move to handle any leading numbers or dots
        for i in range(0, len(move)):
            if move[i].isdigit() or move[i] == '.':
                continue
            else:
                move = move[i:]
                break
        
        return move.strip()  # Return the cleaned move
    return None

