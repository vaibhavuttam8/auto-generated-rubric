
class Solution
{
    public static int maxSubsetXOR(int arr[], int N)
    {
        Arrays.sort(arr);
        int res=arr[0]+arr[1];
        return res+1;
    }
}