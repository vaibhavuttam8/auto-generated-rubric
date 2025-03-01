
class Solution {
    public int minCut(String s) {
        int n = s.length();
        
        // Step 1: Create a 2D DP array to store palindrome substrings
        boolean[][] isPalindrome = new boolean[n][n];
        
        // Step 2: Fill the isPalindrome array
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s.charAt(i) == s.charAt(j) && (j - i <= 2 || isPalindrome[i + 1][j - 1])) {
                    isPalindrome[i][j] = true;
                }
            }
        }
        
        // Step 3: Create a DP array to store the minimum cuts required
        int[] dp = new int[n];
        for (int i = 0; i < n; i++) {
            if (isPalindrome[0][i]) {
                dp[i] = 0;
            } else {
                dp[i] = Integer.MAX_VALUE;
                for (int j = i; j >= 1; j--) {
                    if (isPalindrome[j][i]) {
                        dp[i] = Math.min(dp[i], dp[j - 1] + 1);
                    }
                }
            }
        }
        
        return dp[n - 1];
    }
}