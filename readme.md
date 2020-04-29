# Tic Tac Toe AI : Backend

This is a public Tic Tac Toe API that suggests moves. Users of the API submit the current state of the Tic Tac Toe board and the current person's turn and the API returns a new board state with the suggested, next move and the winner (if there is one) in the form of JSON.

An example query to the API is: https://play-tictactoe-ai.herokuapp.com/api/v1/turn/o/board/xox!o!!x

The public API serves up moves based on [a model](https://github.com/jamiejamiebobamie/tictactoe_ai) that has been trained with reinforcement learning.

The API also serves up random moves.

An example query to receive a random move is: https://play-tictactoe-ai.herokuapp.com/api/v1/rand/turn/o/board/xox!o!!x!

I've utilized this API in a [web app](https://tictactoe-play.herokuapp.com) that allows users to play Tic Tac Toe as well as recieve recommendations on where to move next, and can be easily integrated into your Tic Tac Toe projects.

## Sample Queries To API
Here are some example queries to the API:

Using the AI:
https://play-tictactoe-ai.herokuapp.com/api/v1/turn/o/board/xox!o!!x
https://play-tictactoe-ai.herokuapp.com/api/v1/turn/X/board/o
https://play-tictactoe-ai.herokuapp.com/api/v1/turn/o/board/oxoxO!!x!
https://play-tictactoe-ai.herokuapp.com/api/v1/turn/X/board/!


Random Moves:
https://play-tictactoe-ai.herokuapp.com/api/v1/rand/turn/o/board/xox!o!!x
https://play-tictactoe-ai.herokuapp.com/api/v1/rand/turn/X/board/o
https://play-tictactoe-ai.herokuapp.com/api/v1/rand/turn/O/board/!
https://play-tictactoe-ai.herokuapp.com/api/v1/rand/turn/x/board/!XOO!!

## Authors

* **Jamie McCrory**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
