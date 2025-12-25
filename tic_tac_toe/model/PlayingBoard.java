public class PlayingBoard {
	private String id;
	private int row;
	private int column;
	private User[][]board; // we will save user info on board row+column to easily track them.

	Playingboard(int row, int column){ 
		this.row = row;
		this.column = column;
	}

	public boolean setBoard(int row, int column, User currentUser){
		if(board[row][column] != null){
			return false;
		}
		board[row][column] = currentUser;
		return true;
	}

	public void showCurrentBoard(){
		for(int i=0; i<row; i++){
			for(int j=0; j<column; j++){
				if(board[i][j]!= null){
					System.out.print(board[i][j].symbolChoosen +"   ");
				} else {
					System.out.print("   ");
				}
			}
			System.out.println();
		}
	}

}