
class Solution
{
    public static int generateAllSubset(int []arr,int ind,int n,int xor){
        if(ind>=n)return xor;
        int take=generateAllSubset(arr,ind+1,n,xor^arr[ind]);
        int not_take=generateAllSubset(arr,ind+1,n,xor);
        return Math.max(take,not_take);
    }
    public static int maxSubsetXOR(int arr[], int N)
    {
        //add code here.
        return generateAllSubset(arr,0,N,0);
    }
}