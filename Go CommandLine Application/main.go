package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const (
	maxRoutines = 20
	inputfile = "./inputURLs.txt"
	outputfile = "./output.txt"
)

type ResultRow struct {
	URL   string
	Existed float64
	Error bool
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Input:")
		fmt.Println("\t" + os.Args[0] + "WORD_TO_SEARCH")
		return
	}
	target := os.Args[1]
	urls := getURLs(inputfile)
	out, err := os.Create(outputfile)
	if err != nil {
		fmt.Println("Erro opening output file:", err)
		return
	}
	defer out.Close()

	//search performed here
	result := concurrentSearch(urls, target, maxRoutines)

  //write into output file
	bufout := bufio.NewWriter(out)
	for _, r := range result {
		bufout.WriteString("\""+r.URL+"\","+","+strconv.FormatBool(r.Error)+"\n")
	}
  bufout.Flush()
}

func getURLs(inputfile string) []string {
	lines, err := parseFile(inputfile)
	if err != nil {
		fmt.Println("Error reading URL File:", err)
		return nil
	}
	var urls []string
	for i, l := range lines {
		if i == 0 { continue }
		entry := strings.Split(l, ",")
		url := entry[1]
		urls = append(urls, url[1 : len(url)-1])
	}
  return urls
}



//shouldn't have more than 20 HTTP requests at any given time,20 go routines at max
func concurrentSearch(urls []string, target string, maxRoutines int) []ResultRow {
    exp := regexp.MustCompile("(?i)\\b+" + target + "\\b+")
	// pipeline of three stages
	stage1 := make(chan string, maxRoutines)
	stage2 := make(chan ResultRow)
	stage3 := make(chan []ResultRow)

	go func() {
		k := 0
		tmp := make([]ResultRow, 0, len(urls))
		for s := range stage2 {
			tmp = append(tmp, s)
			k++
			if k == len(urls) { break }
		}
		stage3 <- tmp
	}()

  //max 20 go routines
	for k := 0; k < maxRoutines; k++ {
		go func() {
			for s := range stage1 {
				stage2 <- toSearch(s, exp)
			}
		}()
	}

	for _, u := range urls {
		stage1 <- "http://" + u
	}

	close(stage1)
	close(stage2)
	result := <-stage3
	close(stage3)
	return result
}

//check if a word exist on webpage
func toSearch(url string, re *regexp.Regexp) ResultRow {
	response, err := http.Get(url)
	if err != nil || response.StatusCode < 200 || response.StatusCode >= 300{
		return ResultRow{URL:url, Existed: 0, Error: true}
	}
	defer response.Body.Close()
	data, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return ResultRow{URL: url, Existed: 0, Error: true}
	}

	var score float64 = 0
	exp := regexp.MustCompile("(?i)\\b+" + "good" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.5
	exp = regexp.MustCompile("(?i)\\b+" + "better" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.3
	exp = regexp.MustCompile("(?i)\\b+" + "best" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.9
	exp = regexp.MustCompile("(?i)\\b+" + "excellent" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.8
	exp = regexp.MustCompile("(?i)\\b+" + "nice" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.5
	exp = regexp.MustCompile("(?i)\\b+" + "positive" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.5
	exp = regexp.MustCompile("(?i)\\b+" + "cool" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.4
	exp = regexp.MustCompile("(?i)\\b+" + "terrific" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.8
	exp = regexp.MustCompile("(?i)\\b+" + "fantastic" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.8
	exp = regexp.MustCompile("(?i)\\b+" + "perfect" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 1
	exp = regexp.MustCompile("(?i)\\b+" + "awesome" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * 0.8
	exp = regexp.MustCompile("(?i)\\b+" + "bad" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.5
	exp = regexp.MustCompile("(?i)\\b+" + "worse" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.4
	exp = regexp.MustCompile("(?i)\\b+" + "worst" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.9
	exp = regexp.MustCompile("(?i)\\b+" + "terrible" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.8
	exp = regexp.MustCompile("(?i)\\b+" + "horrible" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.8
	exp = regexp.MustCompile("(?i)\\b+" + "ugly" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.4
	exp = regexp.MustCompile("(?i)\\b+" + "negative" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.5
	exp = regexp.MustCompile("(?i)\\b+" + "evil" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.9
	exp = regexp.MustCompile("(?i)\\b+" + "disgrace" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.8
	exp = regexp.MustCompile("(?i)\\b+" + "disappoint" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.4
	exp = regexp.MustCompile("(?i)\\b+" + "trouble" + "\\b+")
	score += float64(len(exp.FindAllIndex(data, -1))) * -0.3
	return ResultRow{URL:url, Existed: 1.00, Error: false}
}

func parseFile(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil { return nil, err }
	defer file.Close()
	var ls []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		ls = append(ls, scanner.Text())
	}
	return ls, scanner.Err()
}
