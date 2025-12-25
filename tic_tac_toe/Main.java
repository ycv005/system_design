public class Main {
	public static void main(String args[]){
		User user1;
		User user2; // define them
		Playingboard playingBoard;
		PlayingGame playingGame = new PlayingGame(user1, user2, playingBoard);
		playingGame.startGame();
	}
}