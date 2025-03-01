

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
        return node.left == null && node.right == null;
    }
    static void collectBoundaryLeft(Node root, ArrayList<Integer> res){
        if(root == null || isLeaf(root)){
            return;
        }
        res.add(root.data);
        if(root.left != null){
            collectBoundaryLeft(root.left, res);
        }
        else if(root.right != null){
            collectBoundaryLeft(root.right, res);
        }
    } 
    static void collectLeaves(Node root, ArrayList<Integer> res){
        if(root == null){
            return;
        }
        if(isLeaf(root)){
            res.add(root.data);
            return; 
        }
        collectLeaves(root.left, res);
        collectLeaves(root.right, res);
    }
    static void collectBoundaryRight(Node root, ArrayList<Integer> res){
        if(root == null || isLeaf(root))
        return;
        
        if(root.right != null){
            collectBoundaryRight(root.right, res);
        }
        else if(root.left != null){
            collectBoundaryRight(root.left, res);
        }
        res.add(root.data);
    }
    ArrayList<Integer> boundaryTraversal(Node root) {
        ArrayList<Integer> res = new ArrayList<>();
        
        if(root == null){
            return res;
        }
        if(!isLeaf(root)){
            res.add(root.data);
        }
        collectBoundaryLeft(root.left, res);
        
        collectLeaves(root, res);
        collectBoundaryRight(root.right, res);
        return res;
    }
}