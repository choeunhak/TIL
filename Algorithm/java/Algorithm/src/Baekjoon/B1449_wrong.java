package Baekjoon;

import java.io.*;
import java.lang.reflect.Array;
import java.util.*;

public class B1449_wrong {

    public static int stoi(String str) {
        return Integer.parseInt(str);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = stoi(st.nextToken());
        int l = stoi(st.nextToken());

        String[] input = br.readLine().split(" ");

        int[] leaks = new int[n];

        for(int i=0; i<input.length; i++)
        {
            leaks[i] = Integer.parseInt(input[i]);
        }

        Arrays.sort(leaks);

        int now_length=leaks[0];
        int cnt=1;
        double full_length = leaks[leaks.length-1]+0.5;
        int i=0;
        while(true){
            if(now_length>=full_length || i>=leaks.length){
                break;
            }
            if(now_length+0.5>=leaks[i+1]-0.5){
                now_length=now_length+l;
                while(true) {
                    System.out.println("i = " + i);
                    System.out.println("now_length = " + now_length);
                    i=i+1;
                    if (i >= leaks.length || now_length >= leaks[i]) {
                        break;
                    }
                }
                continue;
            }else{
                cnt=cnt+1;
            }
            i=i+1;
            now_length=leaks[i];
        }
//        cnt=cnt+1;
        System.out.println("cnt = " + cnt);




    }

}
