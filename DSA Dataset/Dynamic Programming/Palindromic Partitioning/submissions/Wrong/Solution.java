
// User function Template for Java

class Solution
{   
    static boolean pal(String str,int i,int e)
    {
       while(i<e)
       {
           if(str.charAt(i)==str.charAt(e))
           {
               i++;
               e--;
           }
           else
           {
               return false;
           }
       }
       return true;
    }
    static int func(String str,int i,int e,int count,int[][] dp)
    {
        if(pal(str,i,e))
        {
            return dp[i][e]=count;
        }
        if(dp[i][e]!=-1)
        {
            return dp[i][e];
        }
        int temp=count;
        int z=Integer.MAX_VALUE;
        for(int k=i;k<e;k++)
        {
            if(pal(str,k,e))
            {
                int x=1+func(str,i,k,temp,dp);
                temp=x;
                count=Math.min(temp,z);
                z=temp;
                temp-=x;
            }

        }
        return dp[i][e]=count;
    }
    
    static int palindromicPartition(String s)
    {
        int n=s.length();
        int [][] dp=new int [n][n];
        for(int [] arr:dp)
        {
            Arrays.fill(arr,-1);
        }
        return func(s,0,n-1,0,dp);
    }
}