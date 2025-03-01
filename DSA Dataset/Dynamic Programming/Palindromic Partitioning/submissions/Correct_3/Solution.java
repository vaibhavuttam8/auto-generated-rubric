
//User function Template for Java

class Solution{
    static boolean isPalindrome(String s, int i, int j) {
        while (i < j) {
            if (s.charAt(i) != s.charAt(j)) 
                return false;
            i++;
            j--;
        }
        return true;
    }

    static int palPartitionRec(String s, int i, int j, int[][] memo) {
      
        if (memo[i][j] != -1) 
            return memo[i][j];

        if (i >= j || isPalindrome(s, i, j)) 
            return memo[i][j] = 0;

        int res = Integer.MAX_VALUE;

       for(int k = i;k<=j-1;k++){
           if(isPalindrome(s,i,k)){
               int cuts = 1 +palPartitionRec(s, k + 1, j, memo);
               res = Math.min(res, cuts);
           }
            
        }

        return memo[i][j] = res;
    }

    static int palindromicPartition(String s) {
        int n = s.length();
        int[][] memo = new int[n][n];
        
        // Initialize memo array with -1
        for (int[] row : memo)
            Arrays.fill(row, -1);
        
        return palPartitionRec(s, 0, n - 1, memo);
    }
}