

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
    ArrayList<Integer> boundaryTraversal(Node node) {
        // code here
        
        ArrayList<Integer> ans=new ArrayList<>();
        if(node==null) return ans;
        if(isLeaf(node)==false){
            ans.add(node.data);
        }
        addleft(node,ans);
        addleave(node,ans);
        addright(node,ans);
        return ans;
    }
    public static boolean isLeaf(Node node ){
        if(node!=null && node.left==null && node.right==null){
            return true;
        }
        return false;
    }
    public static void addleft(Node root,ArrayList<Integer> ans){
        Node curr=root.left;
        while(curr!=null){
            if(isLeaf(curr)==false) ans.add(curr.data);
            if(curr.left!=null){
                curr=curr.left;
            }
            else{
                curr=curr.right;
            }
        }
    }
    public static void addright(Node root,ArrayList<Integer> ans){
        Node curr=root.right;
        ArrayList<Integer> temp=new ArrayList<>();
        while(curr!=null){
            if(isLeaf(curr)==false) temp.add(curr.data);
            if(curr.right!=null){
                curr=curr.right;
            }
            else{
                curr=curr.left;
            }
        }
        for(int i=temp.size()-1;i>=0;i--){
            ans.add(temp.get(i));
        }
    }
    public static void addleave(Node root, ArrayList<Integer> ans){
        if(isLeaf(root)==true){
            ans.add(root.data);
        }
        if(root.left!=null) addleave(root.left,ans);
        if(root.right!=null) addleave(root.right,ans);
    }
    
}