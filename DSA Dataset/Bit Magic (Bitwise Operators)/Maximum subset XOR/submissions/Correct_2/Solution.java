
/*Complete the function below*/

class Solution {
    public static int maxSubsetXOR(int arr[], int N) {
        int[] basis = new int[32];
        int basisSize = 0;
        
        for (int i = 0; i < N; i++) {
            int num = arr[i];
            for (int j = 31; j >= 0; j--) {
                if ((num & (1 << j)) == 0) continue;
                if (basis[j] == 0) {
                    basis[j] = num;
                    basisSize++;
                    break;
                }
                num ^= basis[j];
            }
        }

        int result = 0;
        for (int i = 31; i >= 0; i--) {
            if ((result ^ basis[i]) > result) {
                result ^= basis[i];
            }
        }

        return result;
    }
}