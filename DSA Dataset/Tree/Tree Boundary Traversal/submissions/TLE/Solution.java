

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
    static boolean isLeaf(Node root)
    {
        return root.right==null && root.left==null;
    }
    
    static void collectBoundaryLeft(Node root,ArrayList<Integer> res)
    {
        if(root==null)
        {
            return;
        }
        Node curr=root;
        while(!isLeaf(curr))
        {
            res.add(curr.data);
            
            if(curr.left!=null)
            {
                curr=curr.left;
            }
            else
            {
                curr=curr.right;
            }
        }
    }
    static void collectLeaves(Node root,ArrayList<Integer> res)
    {
        Node curr=root;
        while(curr!=null)
        {
            if(curr.left==null)
            {
                if(curr.right==null)
                {
                    res.add(curr.data);
                }
                 curr=curr.right;
            }
            else
            {
                Node preced=curr.left;
                while(preced.right!=null && preced.right!=curr)
                {
                    preced=preced.right;

                }
                if(preced.right==null)
                {
                    preced.right=curr;
                    curr=curr.left;
                }
                else
                {
                    if(preced.left==null)
                    {
                        res.add(preced.data);
                        
                        preced.right=null;
                        
                        curr=curr.right;
                    }
                }
            }
           
        }
    }
    
    static void collectBoundaryRight(Node root,ArrayList<Integer> res)
    {
        if(root==null)
        {
            return;
        }
        
        Node curr=root;
        ArrayList<Integer> temp=new ArrayList<>();
        
         while(!isLeaf(curr))
        {
            res.add(curr.data);
            
            if(curr.right!=null)
            {
                curr=curr.right;
            }
            else
            {
                curr=curr.left;
            }
        }
        
        for(int i=temp.size()-1;i>=0;i--)
        {
            res.add(temp.get(i));
        }
    
    }
    ArrayList<Integer> boundaryTraversal(Node node) {
        // code here
        ArrayList<Integer> res=new ArrayList<>();
        
        if(node==null)
        {
            return res;
        }
        
        if(!isLeaf(node))
        {
            res.add(node.data);
            
            collectBoundaryLeft(node.left,res);
            collectLeaves(node,res);
             collectBoundaryRight(node.right,res);
        }
        
        return res;
    }
    
}