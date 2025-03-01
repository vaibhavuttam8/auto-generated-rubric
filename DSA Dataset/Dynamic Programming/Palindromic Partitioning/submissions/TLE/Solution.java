

// User function Template for Java

class Solution {
    static int palindromicPartition(String s) {
        int n = s.length();
        int[][] dp = new int[n][n];

        for (int i = 0; i < n; i++) {
            Arrays.fill(dp[i], -1);
        }

        return recursion(0, n - 1, s, dp);
    }

    static int recursion(int i, int j, String str, int[][] dp) {
        if (i >= j) return 0;  // No cuts needed for a single character or empty string
        if (dp[i][j] != -1) return dp[i][j];

        if (isPalindrome(str, i, j)) return dp[i][j] = 0;  // No cuts needed if already a palindrome

        int minCuts = Integer.MAX_VALUE;

        for (int k = i; k < j; k++) {
            int left = recursion(i, k, str, dp);
            int right = recursion(k + 1, j, str, dp);
            int cuts = left + right + 1;  // 1 extra cut for partition

            minCuts = Math.min(minCuts, cuts);
        }
        
        return dp[i][j] = minCuts;
    }

    static boolean isPalindrome(String str, int i, int j) {
        while (i < j) {
            if (str.charAt(i) != str.charAt(j)) return false;
            i++;
            j--;
        }
        return true;
    }
}