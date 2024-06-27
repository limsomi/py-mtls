# Proof of Concept: TLS/SSL with Python

This project demonstrates a basic implementation of Transport Layer Security (TLS) and Secure Socket Layer (SSL) communication using Python scripts. It includes scripts for both a TLS server (`server-tls.py`) and a TLS client (`client-tls.py`), as well as a Makefile (`Makefile`) for automating SSL/TLS certificate management with OpenSSL.

## Usage

### Setting Up the Environment

1. **Install Requirements**: Ensure all dependencies are installed using `pip`:

    ```bash
    pip install -r requirements.txt
    ```
2. **Generate Certificates**: Use the Makefile to generate SSL/TLS certificates. Replace <name> with the desired certificate name:

    ```bash
    make generate_cert NAME=<name>
    ```

3. **Start Server and Client**: Execute the Python scripts for the TLS server and client:

    ```bash
    python src/server-tls.py
    python src/client-tls.py
    ```

### Cleaning Up

- Clean Certificates: Remove generated certificates for a specific name:

    ```bash
    make clean NAME=<name>
    ```

- Clean All: Remove all generated certificates and files:

    ```bash
    make clean-all
    ```