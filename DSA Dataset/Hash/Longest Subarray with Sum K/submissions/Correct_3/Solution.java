

// User function Template for Java

class Solution {
    public int longestSubarray(int[] arr, int k) {
       
       HashMap<Integer,Integer> map=new HashMap<>();
       int sum=0,maxLen=0;

       for(int i=0;i<arr.length;i++){
           sum+=arr[i];

            if(sum==k){
                maxLen=i+1;
            }           
        if(map.containsKey(sum-k)){
            maxLen=Math.max(maxLen,i-map.get(sum-k));
        }
           
           if(!map.containsKey(sum)){
               map.put(sum,i);
           }
           
       }
return maxLen;
       }
    

    }