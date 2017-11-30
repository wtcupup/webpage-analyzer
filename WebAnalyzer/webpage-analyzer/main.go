package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"strconv"
)

const (
	maxRoutines = 20
)

type ResultRow struct {
	URL   string
	Existed int
	Error bool
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Input:")
		fmt.Println("\t" + os.Args[0] + "WORD_TO_SEARCH")
		return
	}
	target := os.Args[1]
	urls := getURLs()


	//search performed here
	result := concurrentSearch(urls, target, maxRoutines)
	for _, r := range result {
		fmt.Println("\""+r.URL+"\","+strconv.Itoa(r.Existed)+","+strconv.FormatBool(r.Error)+"\n")
	}
  fmt.Println("End")
}

func getURLs() []string {
	var urls []string

	for i := range os.Args {
		if i == 0 { continue }
		if i == 1 {continue}
		url := os.Args[1]
		urls = append(urls, url)
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
	count := 0
	if re.FindAllIndex(data, -1) == nil {
		count = 0
	} else {
		count = len(re.FindAllIndex(data, -1))
	}
	return ResultRow{URL:url, Existed: count, Error: false}
}


