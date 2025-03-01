

// User function Template for Java

class Solution {
    static int palindromicPartition(String s) {
        int n = s.length();
        int[] dp = new int[n];
        Arrays.fill(dp, -1);
        return helper(s, 0, dp);
    }

    private static int helper(String s, int i, int[] dp) {
        int n = s.length() - 1;
        if(i == n) return 0;

        if(dp[i] != -1) return dp[i];

        if(isPalindrom(s, i, n)) return dp[i] = 0;

        int minCuts = Integer.MAX_VALUE;
        for(int k = i; k < n; k++) {
            if(isPalindrom(s, i, k)) {
                int cuts = 1 + helper(s, k + 1, dp);
                minCuts = Math.min(minCuts, cuts);
            } 
        }
        return dp[i] = minCuts;
    }

    private static boolean isPalindrom(String s, int i, int j) {
        while(i < j) {
            if(s.charAt(i) != s.charAt(j)) return false;
            i++;
            j--;
        }
        return true;
    }
}