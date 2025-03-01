

class Solution {
    static int minJumps(int[] arr) {
        int pos = 0;
        int count = 0;
        while(pos < arr.length-1 && count != -1) {
            if (pos < arr.length-1 && arr[pos] != 0) {
                pos += arr[pos];
                count+=1;
            } else if (arr[pos] == 0 && pos< arr.length-1) {
                count = -1;
            } else {
                break;
            }
        }
        return count;
    }
}