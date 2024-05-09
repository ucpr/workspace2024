package main

import (
	"fmt"

	"github.com/ikawaha/kagome-dict/ipa"
	"github.com/ikawaha/kagome/v2/tokenizer"
)

func main() {
	t, err := tokenizer.New(ipa.Dict(), tokenizer.OmitBosEos())
	if err != nil {
		panic(err)
	}
	/*
		// wakati
		fmt.Println("---wakati---")
		seg := t.Wakati("すもももももももものうち")
		fmt.Println(seg)

		// tokenize
		fmt.Println("---tokenize---")
		tokens := t.Tokenize("すもももももももものうち")
		for _, token := range tokens {
			features := strings.Join(token.Features(), ",")
			fmt.Printf("%s\t%v\n", token.Surface, features)
		}
	*/
	// 解析する文字列
	input := "今日は良い天気ですね。"

	// 形態素解析
	tokens := t.Tokenize(input)

	// カタカナに変換
	for _, token := range tokens {
		features := token.Features()
		if len(features) > 7 && features[7] != "*" {
			// features[7] にカタカナ表記が含まれている場合
			fmt.Printf("%s", features[7])
		}
	}
	fmt.Println()
}
