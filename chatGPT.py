import random
import openai
import re

# Set up your OpenAI API credentials
openai.api_key = ''

# Define a function to interact with the ChatGPT model
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the engine (GPT-3.5)
        prompt=prompt,
        temperature=0.7,  # Controls the randomness of the output (lower values are more focused, higher values are more random)
        max_tokens=30,  # Controls the length of the response
        n=1,  # Specifies the number of responses to generate
        stop=None,  # Optionally specify a stopping sequence for the generated response
        timeout=None  # Optional timeout (in seconds) for the API call
    )

    if 'choices' in response:
        return response['choices'][0]['text'].strip()
    else:
        return "Say what?"

def extract_numbers(text):
  number = re.findall(r'\d+', text)[0]
  return int(number)

# Initialize the Tic-Tac-Toe board
board = [' '] * 9
selectedNumbers = []

# Randomly assign the player and AI symbols
player_turn = 1
player_symbol = 'X'
ai_symbol = 'O' 

# Inital prompt for chatGPT
ai_response = chat_with_gpt("Hi, let's play tic tac toe, where the board is 1-9, please response with 1-9 numbers from now on, please write how the board looks")
print("AI:", ai_response)

# Main game loop
while True:
    # Check if the game is over
    if any([
        (board[0] == board[1] == board[2] != ' '),
        (board[3] == board[4] == board[5] != ' '),
        (board[6] == board[7] == board[8] != ' '),
        (board[0] == board[3] == board[6] != ' '),
        (board[1] == board[4] == board[7] != ' '),
        (board[2] == board[5] == board[8] != ' '),
        (board[0] == board[4] == board[8] != ' '),
        (board[2] == board[4] == board[6] != ' ')
    ]):
        #last player is you
        if player_turn == -1:
            print("You won!")
        else:
            print("ChatGPT won!")
        break

    # 1 - your turn , -1 ChatGPT
    if player_turn == 1:
        print("Your turn (X).")
        while True:
          try:
            #-1 helps with the index array
            move = int(input("Enter your move (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != ' ':
              print("Invalid move! Try again.")
            else:
              break
          except ValueError:
            print("Invalid input! Try again.")

        board[move] = player_symbol
        selectedNumbers.append(move+1)

        player_turn *= -1

    # ChatGPT's turn
    else:
        print("ChatGPT's turn (O).")
        
        prompt = "player had chose {0}, what is your choice?".format(move+1)
        print(prompt)

        response = chat_with_gpt(prompt)

        try:   
            for i in range(0,2):
              print("AI:", response)
              print("AI:", extract_numbers(response))
              move = extract_numbers(response) - 1
              if board[move] != ' ':
                  print("Move already chosen, how would AI take over the world if you can't win in tic tac toe?, regenerating response")
                  prompt = "{0} had already been chosen. chose another number".format(selectedNumbers)
                  print(prompt)
                  response = chat_with_gpt(prompt)
                  continue
                
            if board[move] != ' ':
              print("ChatGPT's response was not a valid move! The game is interrupted.")
              break
            board[move] = ai_symbol
            selectedNumbers.append(move+1)
            print(selectedNumbers)

            player_turn *= -1

        except ValueError:
            print("ChatGPT's response was not a valid move! The game is interrupted.")
            break

    # Print the current board state
    print("{}|{}|{}\n-+-+-\n{}|{}|{}\n-+-+-\n{}|{}|{}\n".format(*board))
