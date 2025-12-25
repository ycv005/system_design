public class PlayGame {
	private	String id;
	private User firstUser;
	private User secondUser;
	private PlayingBoard playingBoard;
	private Deque<User> players;

	PlayGame(User firstUser, User secondUser, PlayingBoard playingBoard) {
		this.firstUser = firstUser;
		this.secondUser = secondUser;
		this.playingBoard = playingBoard;
		players = new LinkedList<>();
		players.add(firstUser);
		players.add(secondUser);
	}


	public void startGame(){
		boolean isGameFinish = false;

		while(!isGameFinish){
			// input from user alternatly, for row and column
			User playerTurn = players.removeFirst();

			// in case of Tie
			List<Pair<Integer, Integer>> freeCells = getFreeCells();

			if(freeCells.isEmpty()){
				isGameFinish = true;
				System.out.println("Match Tie");
			}

			System.out.println("Player Name: " + playerTurn.name + " Enter row, column- ");
			
			playingBoard.showCurrentBoard();

			Scanner inputScn = new Scanner(System.in);

			String s = inputScn.nextLine();
			String[] values = s.split(",");
            int inputRow = Integer.valueOf(values[0]);
            int inputColumn = Integer.valueOf(values[1]);

            boolean resultAddition = playingBoard.setBoard(inputRow, inputColumn);
            if(!resultAddition){
            	System.out.println("Incorrect input, try again");
            	players.addFirst(playerTurn);
            	continue;
            }
            players.addLast(playerTurn);

            boolean gotWinner = playingBoard.doWeHaveWinner(inputRow, inputColumn);
            if(!gotWinner){
            	isGameFinish = true;
            	System.out.println("player Name- " + playerTurn.name + " is winner");
            }
		}

	}
}