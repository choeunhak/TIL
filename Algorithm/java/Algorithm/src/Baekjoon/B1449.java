package Baekjoon;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class B1449 {

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
        int cnt=1;
        int i=0;
        double left_val = leaks[i]-0.5;
        while(true){
            if(i>=leaks.length){
                break;
            }
            if(left_val+l<=leaks[i]-0.5){
                cnt=cnt+1;
                left_val=leaks[i]-0.5;
            }
            i=i+1;
        }
        System.out.println(cnt);
    }
}

/*
 아이디어 : 테이프의 개수를 기준으로 세면서 추가시키면 쉽게 풀린다
 정답 : 현재 테이프의 길이보다 세는 곳의 위치가 더 오른쪽에 있다면 or 현재 테이프의 길이보다 세는곳의 위치-0.5가 크거나 같다면 테이프를 추가시킴!
 틀린 아이디어 : 현재 테이프의 길이가 다음 세는 곳의 위치까지 커버를 하지 않으면 break, break 후에 코드를 짜기 어려움...
 */
