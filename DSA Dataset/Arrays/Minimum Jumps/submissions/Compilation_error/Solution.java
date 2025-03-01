

class Solution {
    public int minJumps(int[] arr) {
        int n = arr.length;
        int[] dp = new int[n];
        Arrays.fill(dp, -1);
        int result = jumpMemo(arr, 0, n, dp);
        return (result == Integer.MAX_VALUE) ? -1 : result;
    }

    private int jumpMemo(int[] arr, int ind, int n, int[] dp,jump) {
        if (ind >= n - 1) return jump;
        if (arr[ind] == 0) return Integer.MAX_VALUE;
        if (dp[ind] != -1) return dp[i];

        int minSteps = Integer.MAX_VALUE;

        for (int i = 1; i <= arr[i]; i++) { 
            
                minSteps = Math.min(minSteps,  jumpMemo(arr, i + ind, n, dp,jump+1));
            
        }

        return dp[i] = minSteps;
    }
}