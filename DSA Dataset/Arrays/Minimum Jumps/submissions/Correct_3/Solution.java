

class Solution {
    static int minJumps(int[] arr) {
        if (arr[0] == 0) return -1;        
        
        int fuel = 1;
        int nextFuel = 0;
        int jumps = 0;
        
        for (int i = 0; i < arr.length; i++) {
            if (fuel == 1 && arr.length - 1 == i) break;
            fuel--;
            nextFuel--;
            
            nextFuel = Math.max(nextFuel, arr[i]);
            
            if (fuel == 0 && !(nextFuel <= 0)) {
                fuel = nextFuel;
                nextFuel = -1;
                jumps++;
            }
            else if (fuel == 0 && nextFuel <= 0) return -1;
        }
        
        return jumps;
    }
}