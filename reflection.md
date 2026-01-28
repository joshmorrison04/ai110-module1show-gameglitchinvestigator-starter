# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

Glitch #1: 
  - **Expected**: Accurate feedback is given after you submit a number
  - **Actual**: Feedback is not accurate and is actually flipped. (based on the secret value) 

Glitch #2: 
  - **Expected**: You can start a new game by pressing "New Game" button after winning. 
  - **Actual**: After winning and pressing new game, guesses submitted don't work (dont recieve feedback on submission, and don't show up in history)

Glich #3: 
  - **Expected**: User can select different difficulties where the range of numbers widens.
  - **Actual**: Hard difficutly has and returns a smaller range than normal. 

Glich #4: 
  - **Expected**: When you press enter on keypad it submits your guess
  - **Actual**: Guess is not submitted when you press enter on keypad. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion you accepted and why.
- Give one example of an AI suggestion you changed or rejected and why.

I used Github Copilot and ChatGPT as my primary AI tools for ths project. One AI suggestion I accepted was moving core logix out of app.py and into test_game_logic.py to help clean up the code. One change I rejected was when CoPilot tried to create multiple new test cases in pytest following a bug that was fixed, I only wanted one new pytest specifically for the bug that was just fixed at the time. 


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

A bug was fixed if it passed it's pytest and it's corresponding feature behaved properly in the app. One pytest I ran was test_new_game_resets_game_stat() which verified that pressing "New Game" works properly. This test showed me that the bug was in the new game button handler, as it wasn't calling init_new_game() to reset teh status from "won" back to "playing", therefore blocking guess submissions after the user one their previous game. AI helped me understand why each test was needed. 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

In the original app the secerent number likely was being generated every time Streamlit ran the script from top to bottom, which happens on every user interaction. Without checking if the secret already existed in session state, the code would regenerate a new random number each rerun. So every time you typed a guess or clicked a button, a new secret was created. 
Streamlit reruns the entire script from the top every time something happens, like if you click a button or type in a textbox. 
The fix was wrapping the secret number generation in a conditional check, making it so the secret is only generated once when the game first starts. On following reruns from the user, it skips that block and uses the secret already stored in session state.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit is the effective use of AI. Being able to read and identify issues within the code and use AI to help you diagnose and solve those isses is very helpful. Next time I'd ask AI to explain or identify potential bugs in the code its generated rather than just accepting it right away even if it looks only relateivly okay/functional. This project really showed me how helpful AI-generated code can be when used properly. It can be a great foundation/starting point that you can build from to create good code. 

## Additional Notes

Agent was the most effective Copilot mode when refactoring the code. 
Providing context made a noticeable difference. It made it so that it could understand the actual strucuture of my code instead of giving generic advice. 
Keeping everything clean and organized is definitley helpful and makes it so that everything (code logic and UI) isn't overwhelming or confusing. Also having different Copilot chats for specific topics helped as well. 