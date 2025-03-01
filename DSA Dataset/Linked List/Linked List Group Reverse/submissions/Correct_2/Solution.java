

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
        if(head==null) return head;
        Node curr = head;
        Node newHead = null;
        Node tail = null;
        while(curr!=null){
            Node prev=null;
            Node temp=null;
            Node groupHead = curr;
            int c=0;
            while(curr!=null&&c<k){
                temp=curr.next;
                curr.next=prev;
                prev=curr;
                curr=temp;
                c++;
            }
            if(newHead==null) newHead=prev;
            if(tail!=null) tail.next=prev;
            tail = groupHead;
        }
        return newHead;
    }
}