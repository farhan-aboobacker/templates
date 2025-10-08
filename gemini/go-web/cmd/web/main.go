package main

import (
	"context"
	"flag"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"

	"google.golang.org/genai"
)

// 🔥 FILL THIS OUT FIRST! 🔥
// Get your Gemini API key by:
// - Selecting "Add Gemini API" in the "Firebase Studio" panel in the sidebar
// - Or by visiting https://g.co/ai/idxGetGeminiKey
// This can also be provided as the API_KEY environment variable.
//
// NOTE: Make sure to `Hard Restart` the web preview in IDX
// when updating this variable, using `> Firebase Studio: Hard Restart`.
var apiKey = "TODO"

func usage() {
	fmt.Fprintf(flag.CommandLine.Output(), "usage: web [options]\n")
	flag.PrintDefaults()
	os.Exit(2)
}

var (
	addr = flag.String("addr", "localhost:8080", "address to serve")
)

func generateHandler(w http.ResponseWriter, r *http.Request, client *genai.Client) {
	if apiKey == "TODO" {
		http.Error(w, "Error: To get started, get an API key at https://makersuite.google.com/app/apikey and enter it in cmd/web/main.go and then hard restart the preview", http.StatusInternalServerError)
		return
	}

	image, prompt := r.FormValue("chosen-image"), r.FormValue("prompt")
	imageBytes, err := os.ReadFile(filepath.Join("static", "images", filepath.Base(image)))
	if err != nil {
		log.Printf("Unable to read image %s: %v\n", image, err)
		http.Error(w, "Error: unable to generate content", http.StatusInternalServerError)
		return
	}
	
	 parts := []*genai.Part{
		genai.NewPartFromBytes(imageBytes, "image/jpeg"),
		genai.NewPartFromText(prompt),
	  }
	  
	  contents := []*genai.Content{
		genai.NewContentFromParts(parts, genai.RoleUser),
	  }

	// Generate the response and aggregate the streamed response.
	for result, err := range client.Models.GenerateContentStream(
		r.Context(),
		"gemini-2.0-flash",
		contents,
		&genai.GenerateContentConfig{
			SafetySettings: []*genai.SafetySetting{
				{
					Category:  genai.HarmCategoryHarassment,
					Threshold: genai.HarmBlockThresholdBlockOnlyHigh,
				},
			},
		},
	
	) {
		if err != nil {
			log.Println(err)
		}
		for _, cand := range result.Candidates {
			if cand.Content != nil {
				for _, part := range cand.Content.Parts {
					fmt.Fprint(w, part.Text)
				}
			}
		}
		
	}

}

type Page struct {
	Images []string
}

var tmpl = template.Must(template.ParseFiles("static/index.html"))

func indexHandler(w http.ResponseWriter, r *http.Request) {
	// Load all baked goods images from the static/images directory.
	matches, err := filepath.Glob(filepath.Join("static", "images", "baked_goods_*.jpeg"))
	if err != nil {
		log.Printf("Error loading baked goods images: %v", err)
	}
	var page = &Page{Images: make([]string, len(matches))}
	for i, match := range matches {
		page.Images[i] = filepath.Base(match)
	}
	switch r.URL.Path {
	case "/":
		err = tmpl.Execute(w, page)
		if err != nil {
			log.Printf("Template execution error: %v", err)
		}
	}
}

func main() {
	// Parse flags.
	flag.Usage = usage
	flag.Parse()

	// Parse and validate arguments (none).
	args := flag.Args()
	if len(args) != 0 {
		usage()
	}

	// Get the Gemini API key from the environment.
	if key := os.Getenv("API_KEY"); key != "" {
		apiKey = key
	}
	ctx := context.Background()
	client, err := genai.NewClient(ctx, &genai.ClientConfig{
		APIKey:   apiKey,
	})
	if err != nil {
		log.Println(err)
	}

	// Serve static files and handle API requests.
	fs := http.FileServer(http.Dir("static"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))
	http.HandleFunc("/api/generate", func(w http.ResponseWriter, r *http.Request) { generateHandler(w, r, client) })
	http.HandleFunc("/", indexHandler)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
