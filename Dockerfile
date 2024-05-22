FROM python:latest

# Configure timezone environment variable
ENV TZ=UTC

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR .

# Copy project files to the Docker image
COPY . .

# Install dependencies with Poetry
RUN poetry install

# Expose port 80
EXPOSE 80

# Run the application using Poetry
CMD ["poetry", "run", "python", "-m", "src.__main__"]