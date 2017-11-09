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
	Existed bool
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
		bufout.WriteString("\""+r.URL+"\","+strconv.FormatBool(r.Existed)+","+strconv.FormatBool(r.Error)+"\n")
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
		return ResultRow{URL:url, Existed: false, Error: true}
	}
	defer response.Body.Close()
	data, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return ResultRow{URL: url, Existed: false, Error: true}
	}
	existed := false
	if re.FindAllIndex(data, -1) == nil {
		existed = false
	} else {
		existed = true
	}
	return ResultRow{URL:url, Existed: existed, Error: false}
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