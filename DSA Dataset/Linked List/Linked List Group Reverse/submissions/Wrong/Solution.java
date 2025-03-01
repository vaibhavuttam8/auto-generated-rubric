

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
        if (head == null || k == 1) return head;

        Node dummy = new Node(0);
        dummy.next = head;
        Node prevLast = dummy;
        Node temp = head;

        while (temp != null) {
            Node kthNode = findKth(temp, k);
            if (kthNode == null) {
                prevLast.next = temp; // Connect remaining nodes if not enough for k-group
                break;
            }

            Node next = kthNode.next;
            kthNode.next = null; // Break the k-group

            Node reversedHead = reverse(temp);

            prevLast.next = reversedHead; // Connect previous group to reversed part
            prevLast = temp; // Update last node of reversed group

            temp = next; // Move to the next group
        }

        return dummy.next;
    }

    static Node findKth(Node head, int k) {
        while (head != null && --k > 0) {
            head = head.next;
        }
        return head;
    }

    static Node reverse(Node head) {
        Node prev = null, curr = head;
        while (curr != null) {
            Node next = curr.next;
            curr.next = prev;
            prev = curr;
            curr = next;
        }
        return prev; // New head of the reversed list
    }
}