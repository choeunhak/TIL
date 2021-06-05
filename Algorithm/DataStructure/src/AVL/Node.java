package AVL;

public class Node <Key extends Comparable<Key>, Value>{
	  Key id;
	  Value name;
	  int height;
	  Node left, right;
	  
	  public Node(Key newId, Value newName, int newHt){
	    id = newId;
	    name = newName;
	    height = newHt;
	    left = right = null;
	  }
	  
	  public Key getKey()	{return id;}
	  public Value getValue()	{return name;}
	  public Node getLeft()	{return left;}
	  public Node getRight()	{return right;}
	  public void setKey(Key newId)	{id = newId;}
	  public void setValue(Value newName)	{name = newName;}
	  public void setLeft(Node newLeft)	{left = newLeft;}
	  public void setRight(Node newRight)	{right = newRight;}
}
