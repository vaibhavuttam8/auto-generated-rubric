

// User function Template for Java

class Solution {
    static int palindromicPartition(String s) {
        int n = s.length();
        int[]dp = new int[n];
        Arrays.fill(dp, -1);
        return helper(s, 0, dp) -1;
    }
    public static int helper(String str, int ind, int[]dp){
        if(ind == str.length()){
            return 0;
        }
        if(dp[ind] !=-1){
            return dp[ind];
        }
        String temp = "";
        int minCost = Integer.MAX_VALUE;
        for(int j=ind; j<str.length(); j++){
            temp+=str.charAt(j);
            if(isPalindrom(temp)){
                int cost = 1 + helper(str, j+1, dp);
                minCost = Math.min(minCost, cost);
            }
        }
        return dp[ind] =minCost;
    }
    
    public static boolean isPalindrom(String temp){
        int i = 0;
        int n= temp.length()-1;
        while(i<=n){
            if(temp.charAt(i) != temp.charAt(n)){
                return false;
            }
            i++; n--;
        }
        return true;
    }
}