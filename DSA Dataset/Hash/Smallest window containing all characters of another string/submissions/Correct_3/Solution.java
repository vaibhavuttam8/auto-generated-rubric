

class Solution {
    // Function to find the smallest window in the string s consisting
    // of all the characters of string p.
    public static String smallestWindow(String s1, String s2) {

        int minLen = Integer.MAX_VALUE;
        String minStr = "";
        HashMap<String, Integer> tMap, sMap;
        sMap = new HashMap<>();
        tMap = new HashMap<>();
        for(int i=0; i<s2.length(); i++){
            String ch = s2.charAt(i)+"";
            if(tMap.containsKey(ch))
                tMap.put(ch, tMap.get(ch)+1);
            else
                tMap.put(ch, 1);
        }
        for(int i=0, j=0; j<s1.length();){
            int count = 0;
            String ch = s1.charAt(j)+"";
            if(tMap.containsKey(ch)){
                if(sMap.containsKey(ch))
                    sMap.put(ch, sMap.get(ch)+1);
                else
                    sMap.put(ch, 1);
                j++;
            }
            else {
                j++;
                continue;
            }

            if(tMap.size() == sMap.size())
                for(String key : tMap.keySet()){
                    if(!sMap.containsKey(key))
                        break;
                    if(tMap.get(key) > sMap.get(key)){
                        count = -1;
                        break;
                    }
                    count++;

                    while(count == tMap.size()){
                        if(minLen > Math.min(minLen, j-i)){
                            minLen = j-i;
                            minStr = s1.substring(i, j);
                        }
                        String c = s1.charAt(i++)+"";
                        if(sMap.containsKey(c)){
                            int value = sMap.get(c)-1;
                            if(value > 0){
                                sMap.put(c, value);
                                if(sMap.get(c) < tMap.get(c))
                                    break;
                            }
                            else{
                                sMap.remove(c);
                                break;
                            }
                        }
                    }
                }
        }
        return minStr;
    }
}