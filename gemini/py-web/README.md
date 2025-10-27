# Python Web with Gemini API

This directory contains a Python web application that uses the Gemini API to generate content. The application is built with Flask and can be run locally.

## Running the Application

To run the application, you will need to have Python and Flask installed. You will also need to get a Gemini API key.

1.  **Get a Gemini API key:**
    *   Select "Add Gemini API" in the "Firebase Studio" panel in the sidebar.
    *   Or by visiting https://g.co/ai/idxGetGeminiKey.
2.  **Set the API key:**
    *   Open the `main.py` file and replace `'TODO'` with your API key.
3.  **Run the application:**
    *   Open a terminal and navigate to this directory.
    *   Run the following command:

    ```bash
    python main.py
    ```

## API

The application has one API endpoint:

*   `/api/generate`: This endpoint takes a POST request with a JSON body that contains the following fields:
    *   `model`: The name of the Gemini model to use.
    *   `contents`: The contents to generate.

The endpoint returns a server-sent event stream that contains the generated content.

## Web Interface

The application also has a web interface that can be accessed at the root of the application. The web interface allows you to enter a prompt and generate content using the Gemini API.

## Files

The following files are included in this directory:

*   `main.py`: The main Python file for the application.
*   `requirements.txt`: The requirements for the application.
*   `devserver.sh`: A shell script to run the development server.
*   `web/`: This directory contains the static files for the web interface.

### Firebase Studio Files

*   `.idx/dev.nix`: This file defines the development environment for the template using Nix. It specifies the packages and configurations needed to run the application within Firebase Studio.
*   `.idx/icon.png`: This is the icon for the template that is displayed in the Firebase Studio interface.
