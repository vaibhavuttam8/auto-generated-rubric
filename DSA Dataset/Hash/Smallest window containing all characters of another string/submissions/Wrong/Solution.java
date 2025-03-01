

class Solution {
    // Function to find the smallest window in the string s consisting
    // of all the characters of string p.
    public static String smallestWindow(String a, String b) {
        // Your code here
       String min = "";
        int min_len = Integer.MAX_VALUE;
        for (int i = 0; i < a.length()-b.length(); i++) {
            int idx = 0;
            int j = i;
            int start=-1;
            while (idx<b.length() && j<a.length()) {
                if (a.charAt(j) == b.charAt(idx)) {
                    if(start==-1)
                        start = j;
                    idx++;
                    j++;
                }else{
                    j++;
                }
            }

            if(b.length() == idx){
               if(min_len >j-start){
                min_len = j-start;
                min = a.substring(start, j);
               }
            }
        }
        return min;
    }
}