

class Solution {
    public int minJumps(int[] arr) {
        int n = arr.length;
        int[] dp = new int[n];
        Arrays.fill(dp, -1);
        int result = jumpMemo(arr, 0, n, dp);
        return (result == Integer.MAX_VALUE) ? -1 : result;
    }

    private int jumpMemo(int[] arr, int i, int n, int[] dp) {
        if (i >= n - 1) return 0;
        if (arr[i] == 0) return Integer.MAX_VALUE;
        if (dp[i] != -1) return dp[i];

        int minSteps = Integer.MAX_VALUE;

        for (int jump = 1; jump <= arr[i]; jump++) { 
            int nextJump = jumpMemo(arr, i + jump, n, dp);
            if (nextJump != Integer.MAX_VALUE) {
                minSteps = Math.min(minSteps, 1 + nextJump);
            }
        }

        return dp[i] = minSteps;
    }
}