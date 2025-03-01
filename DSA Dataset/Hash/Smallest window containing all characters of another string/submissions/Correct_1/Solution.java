

class Solution {
    // Function to find the smallest window in the string s consisting
    // of all the characters of string p.
    public static String smallestWindow(String s1, String s2) {
        // Your code here
        
        if (s1.length() == 0 || s2.length() == 0) {
            return "";
        }

        // Frequency map for characters in s2
        Map<Character, Integer> charCount = new HashMap<>();
        for (char ch : s2.toCharArray()) {
            charCount.put(ch, charCount.getOrDefault(ch, 0) + 1);
        }

        int required = charCount.size(); // Number of unique characters in s2
        int formed = 0; // Number of unique characters in the current window that match the required count
        Map<Character, Integer> windowCounts = new HashMap<>(); // Frequency map for the current window

        int left = 0, right = 0; // Left and right pointers for the window
        int minLength = Integer.MAX_VALUE;
        int start = 0; // Start index of the smallest window

        while (right < s1.length()) {
            char c = s1.charAt(right);
            windowCounts.put(c, windowCounts.getOrDefault(c, 0) + 1);

            if (charCount.containsKey(c) && windowCounts.get(c).intValue() == charCount.get(c).intValue()) {
                formed++;
            }

            while (left <= right && formed == required) {
                c = s1.charAt(left);

                if (right - left + 1 < minLength) {
                    minLength = right - left + 1;
                    start = left;
                }

                windowCounts.put(c, windowCounts.get(c) - 1);
                if (charCount.containsKey(c) && windowCounts.get(c).intValue() < charCount.get(c).intValue()) {
                    formed--;
                }
                left++;
            }
            right++;
        }

        return minLength == Integer.MAX_VALUE ? "" : s1.substring(start, start + minLength);
        
    }
}