

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
    public ListNode reverseKGroup(ListNode head, int k) {
        if (k <= 1 || head == null) {
            return head;
        }

        // Count the total number of nodes
        int length = getLength(head);
        ListNode present = head;
        ListNode prev = null;

        while (length >= k) { // Only process if at least k nodes remain
            ListNode last = prev;
            ListNode newEnd = present;
            ListNode next = present.next;

            // Reverse k nodes
            for (int i = 0; present != null && i < k; i++) {
                present.next = prev;
                prev = present;
                present = next;
                if (next != null) {
                    next = next.next;
                }
            }

            if (last != null) {
                last.next = prev;
            } else {
                head = prev;
            }

            newEnd.next = present;
            prev = newEnd;
            length -= k; // Reduce length by k since k nodes have been processed
        }
        return head;
    }

    private int getLength(ListNode head) {
        int count = 0;
        while (head != null) {
            count++;
            head = head.next;
        }
        return count;
    }
}