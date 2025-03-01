

class Solution {
    // Function to find the smallest window in the string s consisting
    // of all the characters of string p.
    public static boolean isFound(String s1 , String s2){
        int freq[] = new int[256];
        for(char ch : s2.toCharArray()){
            freq[ch]++;
        }
        for(char ch : s1.toCharArray()){
            if(freq[ch] > 0){
                freq[ch]--;
            }
        }
        for(int val : freq){
            if(val != 0){
                return false;
            }
        }
        return true;
    }
    public static String smallestWindow(String s1, String s2) {
        int minLen = Integer.MAX_VALUE;
        String minSubstr = "";
        for(int i=0; i<s1.length(); i++){
            for(int j=i; j<s1.length(); j+=1){
                String substr = s1.substring(i,j+1);
                if(isFound(substr,s2)){
                    int len = substr.length();
                    if(minLen > len){
                        minLen = len;
                        minSubstr = substr;
                    }
                }
            }
        }
        return minSubstr != "" ? minSubstr : "";
    }
}