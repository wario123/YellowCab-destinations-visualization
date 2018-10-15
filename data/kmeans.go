
package main

import (
    "bufio"
    "log"
    "os"
    "fmt"
    "strings"
    "strconv"
    "github.com/mdesenfants/gokmeans"
)

func main() {
    // Open file with the data
    file, err := os.Open("result/filtered_data.csv")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    var observations []gokmeans.Node 
    scanner := bufio.NewScanner(file)
    for scanner.Scan(){
        values := strings.Split(scanner.Text(), ",")
        long, _ := strconv.ParseFloat(values[9], 64)
        lat, _ := strconv.ParseFloat(values[10], 64)
        observations = append(observations, gokmeans.Node{long, lat})
    }

    // Get a list of centroids and output the values
    if success, centroids := gokmeans.Train(observations, 24, 2); success {
        // Show the centroids
        fmt.Println("The centroids are")
        for _, centroid := range centroids {
            fmt.Println(centroid)
        }

        // Output the clusters
//        fmt.Println("...")
//        for _, observation := range observations {
//            index := gokmeans.Nearest(observation, centroids)
//           fmt.Println(observation, "belongs in cluster", index+1, ".")
//        }
    }
}

