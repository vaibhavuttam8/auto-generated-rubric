

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
    static boolean isLeaf(Node node){
    static void collectBoundaryRight(Node root, ArrayList<Integer> res){
        if(root == null || isLeaf(root))
        return;
        
        if(root.right != null){
            collectBoundaryRight(root.right, res);
        }
        else if(root.left != null){
            collectBoundaryRight(root.left, res);
        }
        res.add(root.add);
    }
    ArrayList<Integer> boundaryTraversal(Node node) {
        ArrayList<Integer> res = new ArrayList<>();
        
        if(root == null){
            return res;
        }
        if(!isLeaf(root)){
            res.add(root.data);
        }
        collectBoundaryLeft(root.left, res);
        
        collectLeaves(root, res);
        return res;
    }
}