
/*Complete the function below*/

class Solution
{
    public static int maxSubsetXOR(int arr[], int N)
    {
        int index = 0;
  
        // Traverse through all bits starting from the most significant bit (31st bit)
        for (int i = 31; i >= 0; i--) {
            int maxInd = index;
            int maxEle = Integer.MIN_VALUE;
            
            // Find the maximum element with i-th bit set
            for (int j = index; j < N; j++) {
                if ((arr[j] & (1 << i)) != 0 && arr[j] > maxEle) {
                    maxEle = arr[j];
                    maxInd = j;
                }
            }
  
            // If no element has the i-th bit set, skip
            if (maxEle == Integer.MIN_VALUE) continue;
  
            // Swap max element with first element of reduced set
            int temp = arr[index];
            arr[index] = arr[maxInd];
            arr[maxInd] = temp;
  
            // XOR other elements having the i-th bit set
            for (int j = 0; j < N; j++) {
                if (j != index && (arr[j] & (1 << i)) != 0)
                    arr[j] ^= arr[index];
            }
  
            index++;
        }
  
        // Compute final XOR subset result
        int result = 0;
        for (int i = 0; i < N; i++)
            result ^= arr[i];
  
        return result;
    
    }
}