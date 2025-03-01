

/*node class of the linked list
class Node
{
    int data;
    Node next;
    Node(int key)
    {
        data = key;
        next = null;
    }
}

*/

class Solution {
    public static Node reverseKGroup(Node head, int k) {
        // code here
        if(head==null)
        return null;
        int c=k;
        Node curr=head;
        Node prev=null;
        Node next=head;
        while(curr!=null && c>0)
        {
            next=curr.next;
            curr.next=prev;
            prev=curr;
            curr=next;
            c--;            
        }
        head.next =reverseKGroup(next,k);
        return prev;
    }
}