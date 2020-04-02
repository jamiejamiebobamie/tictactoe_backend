This is a Tic Tac Toe API that suggests moves.
Make a query to the api in the form of:
api/v1/turn/o/board/xox!o!
From the above URL, the api will think it's O's turn
and that the board looks like this:
x o x
_ o _
_ _ _
As you can see, the trailing blank spots can be omitted.
DO NOT omit blank spots that precede an x or o.
The API will return an updated board as JSON:
{"board": "xox!o!!o!"}
(Not the prettiest to read and understand if you're a human, but perfect for your app.)
