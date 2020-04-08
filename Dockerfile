FROM python:3.6 as builder

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
# At run time, /credentials must be binded to a volume containing a valid
# Service Account credentials file named datacatalog-utils.json.
ENV GOOGLE_APPLICATION_CREDENTIALS=/credentials/datacatalog-utils.json

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .


# QUALITY ASSURANCE
FROM builder as qa

# Run static code checks.
RUN pip install flake8 yapf
RUN yapf --diff --recursive src tests
RUN flake8 src tests

# Run the unit tests.
RUN python setup.py test
# END OF QUALITY ASSURANCE STEPS


# RESUME THE IMAGE BUILD PROCESS
FROM builder as run

# Install the package.
RUN pip install .

ENTRYPOINT ["datacatalog-utils"]
