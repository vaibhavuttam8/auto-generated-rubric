
/*Complete the function below*/

class Solution {
    public static int maxSubsetXOR(int arr[], int N) {
        int[] basis = new int[32]; // Basis for the vector space
        int basisSize = 0;

        // Build the basis
        for (int num : arr) {
            for (int i = 31; i >= 0; i--) {
                if ((num & (1 << i)) == 0) continue;
                if (basis[i] == 0) {
                    basis[i] = num;
                    basisSize++;
                    break;
                }
                num ^= basis[i];
            }
        }

        // Compute the maximum XOR
        int maxXOR = 0;
        for (int i = 31; i >= 0; i--) {
            if ((maxXOR ^ basis[i]) > maxXOR) {
                maxXOR ^= basis[i];
            }
        }

        return maxXOR;
    }
}