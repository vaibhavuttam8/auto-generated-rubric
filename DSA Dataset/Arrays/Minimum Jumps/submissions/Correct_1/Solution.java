
class Solution {
    static int minJumps(int[] arr) {
        int n = arr.length;
        if (n == 1) return 0; // Already at the last index
        if (arr[0] == 0) return -1; // Cannot move forward

        int jumps = 0;
        int current_end = 0;
        int farthest = 0;

        for (int i = 0; i < n - 1; i++) {
            farthest = Math.max(farthest, i + arr[i]);

            // If we have reached the current range's end
            if (i == current_end) {
                jumps++;
                current_end = farthest;

                // If the farthest point reaches or exceeds the last index
                if (current_end >= n - 1) {
                    return jumps;
                }
            }
        }

        return -1; // If we cannot reach the last index
    }
}