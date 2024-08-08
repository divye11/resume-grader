# Job Analyzer

Job Analyzer is a web application built with Next.js that allows users to view job listings, details, and candidate information. It provides a user-friendly interface for job seekers and recruiters to manage job applications and candidates effectively.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Contributing](#contributing)
- [License](#license)

## Features

- View job listings with detailed descriptions.
- Filter and search for jobs based on various criteria.
- View candidate profiles and their relevancy scores.
- Responsive design for mobile and desktop users.

## Getting Started

To get started with the Job Analyzer application, follow the instructions below.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/divye11/resume-grader.git
   cd resume-grader
   ```

2. **For the API**:
   - Navigate to the `api` directory:
     ```bash
     cd api
     ```
   - Use Poetry to install the dependencies:
     ```bash
     poetry install
     ```
   - Ensure you are using a virtual environment. You can create one with:
     ```bash
     conda activate <venv name>
     ```
   - Start MongoDB using Docker Compose:
     ```bash
     docker-compose up -d mongo
     ```

3. **For the App**:
   - Navigate to the `app` directory:
     ```bash
     cd ../app
     ```
   - Install the dependencies and run the application using Yarn:
     ```bash
     yarn
     ```
   - Run the application in development mode:
     ```bash
     yarn dev
     ```


4. Set up the environment variables. Create a `.env` file in the `api` directory and add the following:

   ```env
   WORKABLE_URL=<Your workable link>
   WORKABLE_API_KEY=<Your key here>
   MONGODB_URL=mongodb://admin:password@localhost:27017/
   ```

   And in the `app` directory, create a `.env` file with:

   ```env
   BASE_PATH=http://localhost:8000
   ```

5. Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to see the application in action.

## Usage

- Navigate through the sidebar to view all jobs or saved jobs.
- Click on a job title to view its details, including job description, requirements, and candidates.
- Use the search functionality to find specific jobs quickly.

## API

The application interacts with a backend API. Ensure that the API is running and accessible at the specified `BASE_PATH`. The API provides endpoints for fetching job listings, job details, and candidate information.

### Example API Endpoints

- `GET /jobs` - Retrieve a list of jobs.
- `GET /jobdetail/:id` - Retrieve details for a specific job.
- `GET /candidates` - Retrieve a list of candidates for a job.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.