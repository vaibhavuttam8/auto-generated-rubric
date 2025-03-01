

/*Complete the function below*/

class Solution
{
    public static int maxSubsetXOR(int arr[], int N)
    {

        int index = 0; // Initialize index of chosen elements

        // Traverse through all bits of integer starting from the most significant bit (MSB)
        for (int bit = 31; bit >= 0; bit--) {
            // Initialize index of maximum element and the maximum element
            int maxIndex = index;
            int maxValue = Integer.MIN_VALUE;

            // Search for a maximum element with the current bit set
            for (int i = index; i < N; i++) {
                if ((arr[i] & (1 << bit)) != 0 && arr[i] > maxValue) {
                    maxValue = arr[i];
                    maxIndex = i;
                }
            }

            // If no element with the current bit set is found, continue to the next bit
            if (maxValue == Integer.MIN_VALUE) continue;

            // Swap the found maximum element with the first element
            int temp = arr[index];
            arr[index] = arr[maxIndex];
            arr[maxIndex] = temp;

            // Update maxIndex for the current bit
            maxIndex = index;

            // XOR all elements which have the current bit set, excluding the maxIndex
            for (int i = 0; i < N; i++) {
                if (i != maxIndex && (arr[i] & (1 << bit)) != 0) {
                    arr[i] ^= arr[maxIndex];
                }
            }

            // Increment index of chosen elements
            index++;


    }
}