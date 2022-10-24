package Baekjoon;

import java.util.Scanner;
public class B1543 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String docs = sc.nextLine();
        String word = sc.nextLine();

        int docs_length = docs.length();
        int word_length = word.length();
        int i=0;
        int cnt=0;
        while(true){
            if(docs_length-word_length<i){
                break;
            }
            if(docs.substring(i,i+word_length).equals(word)){
                cnt=cnt+1;
                i=i+word_length;
                continue;
            }
            i=i+1;
        }
        System.out.println(cnt);
        sc.close();

    }

}
