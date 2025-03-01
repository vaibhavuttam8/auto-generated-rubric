

// User function Template for Java
class Solution {
    int missingNumber(int arr[]) {
        int n = arr.length+1;
        
      int xorTotal = 0, xorArray = 0;

        // XOR all numbers from 1 to n
        for (int i = 1; i <= n; i++) {
            xorTotal ^= i;
        }

        // XOR all numbers in the given array
        for (int num : arr) {
            xorArray ^= num;
        }

        // The missing number is the difference of the two XORs
        return xorTotal ^ xorArray;
    }

    public static void main(String[] args) {
        int[] arr1 = {1, 2, 3, 5};
        System.out.println(arr1);
    }
}