

class Solution {
    // Function to find the smallest window in the string s consisting
    // of all the characters of string p.
    public static String smallestWindow(String s1, String s2) {
        int n = s1.length();
        int m = s2.length();
        
        HashMap<Character,Integer> wind = new HashMap<>();
        HashMap<Character,Integer> str2 = new HashMap<>();
        for(Character chars : s2.toCharArray()){
            str2.put(chars,str2.getOrDefault(chars,0)+1);
            wind.put(chars,0);
        }
        
        int minLen = Integer.MAX_VALUE;
        int windCnt = 0;
        int str2Cnt = s2.length();//total cnt
        int track_l = 0;
        int l = 0;
        
        for(int r=0;r<n;r++){
            if(wind.containsKey(s1.charAt(r))){
                wind.put(s1.charAt(r),wind.get(s1.charAt(r))+1);
                if(wind.get(s1.charAt(r))<=(str2.get(s1.charAt(r)))){
                    windCnt++;
                }
            }
            
            while(windCnt == str2Cnt){
                int len = r-l+1;
                if(len < minLen){
                    minLen = len;
                    track_l = l;
               }
        
               if(wind.containsKey(s1.charAt(l))){
               wind.put(s1.charAt(l),wind.get(s1.charAt(l))-1);
               if(wind.get(s1.charAt(l)) < str2.get(s1.charAt(l))){
               windCnt--;
               }
               }
               l++;
            }
        }
        return (minLen == Integer.MAX_VALUE) ?  "":s1.substring(track_l,minLen+track_l);
    }
}