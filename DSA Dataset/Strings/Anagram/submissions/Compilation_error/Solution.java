

class Solution {
    // Function is to check whether two strings are anagram of each other or not.
    public static boolean areAnagrams(String s1, String s2) {
        
        if(s1.length() != s2.length()){
            return false;
        }
        
       char[] charArr1 = s1.toCharArray();
       char[] charArr2 = s2.tocharArray();
       
       Arrays.sort(charArr1);
       Arrays.sort(charArr2);
       
       return Arrays.equals(charArr1, charArr2);
    }
}
//         char[] charArray1 =s1.toCharArray();
//         char[] charArray2 =s2.toCharArray();
        
//         Arrays.sort(charArray1);
//         Arrays.sort(charArray2);
        
        
//         return Arrays.equals(charArray1 ,charArray2);