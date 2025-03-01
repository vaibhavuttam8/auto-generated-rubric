class Solution {
    // Function to find the smallest window in the string s1 consisting
    // of all the characters of string s2.
    public static String smallestWindow(String s1, String s2) {

        int len1 = s1.length();
        int len2 = s2.length();

        // if length of string s2 is greater than string s1 then we return -1.
        if (len1 < len2) {
            return "";
        }

        // using hash tables to store the count of characters in strings.
        int[] hash_pat = new int[256];
        int[] hash_str = new int[256];

        // storing the count of characters in string s2 in hash table.
        for (int i = 0; i < len2; i++) {
            hash_pat[s2.charAt(i)]++;
        }

        int start = 0;
        int start_index = -1;
        int min_len = Integer.MAX_VALUE;
        int count = 0;
        for (int j = 0; j < len1; j++) {
            // storing the count of characters in string s1 in hash table.
            hash_str[s1.charAt(j)]++;

            // if count of current character in string s1 is equal to or less
            // than in string s2, we increment the counter.
            if (hash_pat[s1.charAt(j)] != 0 &&
                hash_str[s1.charAt(j)] <= hash_pat[s1.charAt(j)]) {
                count++;
            }

            // if all the characters are matched
            if (count == len2) {
                while (hash_str[s1.charAt(start)] > hash_pat[s1.charAt(start)] ||
                       hash_pat[s1.charAt(start)] == 0) {
                    // we try to minimize the window.
                    if (hash_str[s1.charAt(start)] > hash_pat[s1.charAt(start)]) {
                        hash_str[s1.charAt(start)]--;
                    }
                    start++;
                }
                // updating window size.
                int len_window = j - start + 1;
                if (min_len > len_window) {
                    // if new minimum sub-string is found, we store value
                    // of its starting index for new found window.
                    min_len = len_window;
                    start_index = start;
                }
            }
        }
        // returning the smallest window or -1 if no such window is present.
        if (start_index == -1) {
            return ("");
        } else {
            return (s1.substring(start_index, start_index + min_len));
        }
    }
}