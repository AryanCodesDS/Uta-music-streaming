# UTA - A MUSIC STREAMING APP

UTA🎵 is a multi-user desktop web application designed for music streaming and reading lyrics. It offers functionalities for both general users and creators, providing a comprehensive platform for music enthusiasts.

## Author
Aryan Tiwari  
21f1001076  
21f1001076@ds.study.iitm.ac.in  

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and set up the UTA project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/uta-music-streaming-app.git
    cd uta-music-streaming-app
    ```

2. **Set up the backend**:
    - Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    - Activate the virtual environment:
        - On Windows:
            ```bash
            venv\Scripts\activate
            ```
        - On macOS/Linux:
            ```bash
            source venv/bin/activate
            ```
    - Install the required packages:
        ```bash
        pip install -r requirements.txt
        ```
    - Set up the database:
        ```bash
        flask db init
        flask db migrate
        flask db upgrade
        ```

3. **Set up the frontend**:
    - Navigate to the frontend directory:
        ```bash
        cd frontend
        ```
    - Install the required packages:
        ```bash
        npm install
        ```

4. **Run the application**:
    - Start the backend server:
        ```bash
        flask run
        ```
    - Start the frontend development server:
        ```bash
        npm run serve
        ```

## Usage

Once the application is set up and running, you can access it at `http://localhost:8080` in your web browser. Here are some key functionalities:

- **General Users**:
  - Play songs
  - Read lyrics
  - Rate songs
  - Create and manage playlists

- **Creators**:
  - Upload songs, albums, and lyrics
  - Manage uploaded content via the dashboard
  - View statistics for uploaded songs

For a detailed walkthrough, watch the project demo [here](https://drive.google.com/file/d/16zKqG9uk5YdfBLUgrjj3ow3qcVsppQsj/view?usp=sharing).

## Contributing

We welcome contributions from the community! Here’s how you can help:

1. **Fork the repository** to your own GitHub account.
2. **Clone the repository** to your local machine:
    ```bash
    git clone https://github.com/yourusername/uta-music-streaming-app.git
    ```
3. **Create a new branch** for your feature or bugfix:
    ```bash
    git checkout -b feature-name
    ```
4. **Make your changes** and commit them with a descriptive message:
    ```bash
    git commit -m "Description of changes"
    ```
5. **Push your changes** to your forked repository:
    ```bash
    git push origin feature-name
    ```
6. **Submit a pull request** to the main repository, describing your changes in detail.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
