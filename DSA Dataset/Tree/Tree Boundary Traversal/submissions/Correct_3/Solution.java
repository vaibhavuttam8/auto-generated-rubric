

// User function Template for Java
/*
class Node
{
    int data;
    Node left, right;

    public Node(int d)
    {
        data = d;
        left = right = null;
    }
}
*/

class Solution {
    ArrayList<Integer> boundaryTraversal(Node root) {
        ArrayList<Integer> list =new ArrayList<>();
        if(isLeaf(root)){
            list.add(root.data);
            return list;
        }else{
            list.add(root.data);
        }
        addLeftBound(root,list);
        addleaves(root,list);
        addRightBound(root,list);
    return list;
    }
    public boolean isLeaf(Node node){
        if(node.left==null && node.right==null){
            return true;
        }
        return false;
    }
    public void addLeftBound(Node root,ArrayList<Integer> list){
        Node curr = root.left;   
        while(curr!=null){
            if(!isLeaf(curr)){
                list.add(curr.data);
            }
            if(curr.left!=null){
                curr=curr.left;
            }else{
                curr=curr.right;
            }
        }
        
    }
    public void addleaves(Node node,ArrayList<Integer> list){
        if(isLeaf(node)){
            list.add(node.data);
            return;
        }
        if(node.left!=null){
            addleaves(node.left,list);
        }if(node.right!=null){
            addleaves(node.right,list);
        }
    }
    public void addRightBound(Node root, ArrayList<Integer> list){
        ArrayList<Integer> temp = new ArrayList<>();
        Node curr =root.right;
        while(curr!=null){
            if(!isLeaf(curr)){
                temp.add(curr.data);
            }
            if(curr.right!=null){
                curr=curr.right;
            }else{
                curr=curr.left;
            }
        }
        for(int i=temp.size()-1;i>=0;i--){
            list.add(temp.get(i));
        }
    }
}