public class User {
	private String id;
	private String name;
	private SymbolType symbolChoosen;

	User(String name, SymbolType symbolSelected) {
		this.name = name;
		this.symbolChoosen = symbolSelected;
	}

	public String getName(){}

	public String setName(){}

	public SymbolType getSymbolChoosen(){}

}