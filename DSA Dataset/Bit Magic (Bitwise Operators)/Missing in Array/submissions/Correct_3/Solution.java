

// User function Template for Java
class Solution {
    int missingNumber(int arr[]) {
        int xor1 = 0;
        int xor2 = 0;
        int n = arr.length;
        for(int i : arr){
            xor1 ^= i;
        }
        for(int i = 1;i<=n+1;i++){
            xor2 ^= i;
        }
        return xor1^xor2;
    }
}