

// User function Template for Java

class Solution {
    public int solve(String s, int i, int[] dp, boolean[][] palindrome) {
        if (i == s.length()) return 0;  
        if (dp[i] != -1) return dp[i];

        int ans = Integer.MAX_VALUE;
        for (int j = i; j < s.length(); j++) {
            if (palindrome[i][j]) {  
                ans = Math.min(ans, 1 + solve(s, j + 1, dp, palindrome));
            }
        }

        return dp[i] = ans;
    }

    public int palindromicPartition(String s) {
        int n = s.length();
        int[] dp = new int[n];  
        Arrays.fill(dp, -1); 
        boolean[][] palindrome = new boolean[n][n];

        
        for (int gap = 0; gap < n; gap++) {
            for (int i = 0, j = gap; j < n; i++, j++) {
                if (gap == 0) {
                    palindrome[i][j] = true;
                } else if (gap == 1) {
                    palindrome[i][j] = (s.charAt(i) == s.charAt(j));
                } else {
                    palindrome[i][j] = (s.charAt(i) == s.charAt(j)) && palindrome[i + 1][j - 1];
                }
            }
        }

        return solve(s, 0, dp, palindrome) - 1; 
    }
}