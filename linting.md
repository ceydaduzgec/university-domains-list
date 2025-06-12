# Local Linting Guide

This guide explains how to run the same linting tools locally that are used in our CI pipeline.

## Running GitHub Super-Linter Locally

Our project uses GitHub Super-Linter for code quality checks. To run it locally:

1. **Install Docker** if you don't have it already

   - [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Mac/Windows
   - [Docker Engine](https://docs.docker.com/engine/install/) for Linux

2. **Pull the Super-Linter Docker image**

   ```bash
   docker pull github/super-linter:v3.15.3
   ```

3. **Run the linter with the same configuration as our CI**
   ```bash
   docker run -e RUN_LOCAL=true \
     -e VALIDATE_PYTHON_PYLINT=false \
     -e VALIDATE_PYTHON_FLAKE8=false \
     -e VALIDATE_MARKDOWN=false \
     -e JAVASCRIPT_DEFAULT_STYLE=prettier \
     -v $(pwd):/tmp/lint \
     github/super-linter:v3.15.3
   ```

## Prettier Code Formatting

To format your code with Prettier:

1. **Install Prettier** (requires Node.js)

   ```bash
   npm install --global prettier
   ```

2. **Format your code**

   ```bash
   # Format all supported files
   prettier --write .

   # Or format specific files
   prettier --write "**/*.{js,jsx,json,md}"
   ```

Our Prettier configuration (`.prettierrc`) is set up with:

- Tab width: 2 spaces
- Line width: 100 characters
- Single quotes
- Trailing commas

## Troubleshooting

- If you encounter permission issues with Docker, you may need to run the commands with `sudo`
- Make sure you're running commands from the project root directory
- Check that your Docker daemon is running before attempting to use the Super-Linter
