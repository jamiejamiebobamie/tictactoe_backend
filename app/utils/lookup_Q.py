import csv

def convert_csv_to_Q(file_path):
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        # https://stackoverflow.com/questions/6740918/creating-a-dictionary-from-a-csv-file
        Q = dict()
        for row in reader:

            turn = row[0][1]
            if turn == "T":
                turn = True
            else:
                turn = False

            key_list = row[0][2:-1].split(",")
            board = []
            for i, entry in enumerate(key_list):
                for char in entry:
                    if char == '1':
                        board.append(1)
                        break
                    elif char == '0':
                        board.append(0)
                        break
                    elif char == 'N':
                        board.append(None)
                        break

            board_state = tuple(board)

            key = (turn, board_state)

            value = list()
            i = 1
            while i < len(row):
                new_value = float(row[i])
                value.append(new_value)
                i+=1

            Q.update( {key: value} )

    return Q
