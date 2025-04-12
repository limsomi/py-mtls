# Variables for colored output
GREEN := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE := $(shell tput -Txterm setaf 7)
CYAN := $(shell tput -Txterm setaf 6)
RESET := $(shell tput -Txterm sgr0)

# Default target
.DEFAULT_GOAL := help

# Set shell explicitly
SHELL := /bin/bash

# Check if NAME is defined, throw error if not
# ifndef NAME
# $(error NAME is not set. Please specify NAME=<name> when invoking make)
# endif

# Directories
SSL_BASE_DIR := $(DIR)
SSL_DIR := $(SSL_BASE_DIR)/$(NAME)

SSL_ROOT:=./ssl/$(ROOT)
OPENSSL_CNF := /etc/pki/tls/openssl.cnf
.PHONY: all help generate_certificates clean clean-all generate_ca clean_ca

# Help target
help: ## Show this help message
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET} ${YELLOW}NAME=<name>${RESET} [${CYAN}force=(true|false)${RESET}]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} \
	      /^[a-zA-Z_-]+:.*?## .*$$/ { \
	          printf "    ${YELLOW}%-20s${GREEN}%s${RESET}\n", $$1, $$2 \
	      } \
	      /^## .*$$/ { \
	          printf "  ${CYAN}%s${RESET}\n", substr($$1, 4) \
	      }' $(MAKEFILE_LIST)

# SSL/TLS certificate generation targets
generate_cert: generate_key generate_csr sign_certificate create_nopassword_key create_pem_files ## Generate SSL/TLS certificates

generate_key: create_ssl_dir
	@if [ ! -f "$(SSL_DIR)/$(NAME).key" ] || [ "$(force)" = "yes" ]; then \
	    echo "Generating RSA key: $(SSL_DIR)/$(NAME).key"; \
	    openssl genrsa -out $(SSL_DIR)/$(NAME).key 4096; \
	else \
	    echo "RSA key $(SSL_DIR)/$(NAME).key already exists, skipping generation."; \
	fi

generate_csr: generate_key
	@if [ ! -f "$(SSL_DIR)/$(NAME).csr" ] || [ "$(force)" = "yes" ]; then \
		RANDOM_SUBJECT=$$(python3 generate_subject.py | tr -d '\n'); \
	    echo "Generating CSR with random subject: $$RANDOM_SUBJECT"; \
	    openssl req -new -key $(SSL_DIR)/$(NAME).key -out $(SSL_DIR)/$(NAME).csr -subj "$$RANDOM_SUBJECT" -config $(OPENSSL_CNF); \
	else \
	    echo "CSR $(SSL_DIR)/$(NAME).csr already exists, skipping generation."; \
	fi

sign_certificate: generate_csr
	@if [ ! -f "$(SSL_DIR)/$(NAME).crt" ] || [ "$(force)" = "yes" ]; then \
	    echo "Signing certificate: $(SSL_DIR)/$(NAME).crt"; \
	    openssl x509 -req -in $(SSL_DIR)/$(NAME).csr -CA $(SSL_ROOT)/$(ROOT).pem -CAkey $(SSL_ROOT)/$(ROOT).key -CAcreateserial -out $(SSL_DIR)/$(NAME).crt -days 1825 -sha256 -extfile $(OPENSSL_CNF) -extensions v3_req; \
	else \
	    echo "Certificate $(SSL_DIR)/$(NAME).crt already exists, skipping signing."; \
	fi

create_nopassword_key:
	@if [ ! -f "$(SSL_DIR)/nopassword.key" ] || [ "$(force)" = "yes" ]; then \
	    echo "Creating no password key: $(SSL_DIR)/nopassword.key"; \
	    openssl rsa -in $(SSL_DIR)/$(NAME).key -out $(SSL_DIR)/nopassword.key; \
	else \
	    echo "No password key $(SSL_DIR)/nopassword.key already exists, skipping creation."; \
	fi

create_pem_files: create_nopassword_key sign_certificate
	@if [ ! -f "$(SSL_DIR)/$(NAME).pem" ] || [ "$(force)" = "yes" ]; then \
	    echo "Creating PEM file: $(SSL_DIR)/$(NAME).pem"; \
	    cat $(SSL_DIR)/nopassword.key > $(SSL_DIR)/$(NAME).pem; \
	    cat $(SSL_DIR)/$(NAME).crt >> $(SSL_DIR)/$(NAME).pem; \
	    cat $(SSL_ROOT)/$(ROOT).pem >> $(SSL_DIR)/$(NAME).pem; \
		# cat ./ssl/RootCA/RootCA.pem >>  $(SSL_ROOT)/$(ROOT).pem; \
	else \
	    echo "PEM file $(SSL_DIR)/$(NAME).pem already exists, skipping creation."; \
	fi

# CA generation targets
generate_ca: generate_ca_key generate_ca_cert ## Generate CA key and certificate

generate_ca_key: create_ssl_dir
	@if [ ! -f "$(SSL_DIR)/$(NAME)" ] || [ "$(force_ca)" = "yes" ]; then \
	    echo "Generating CA key: $(SSL_DIR)/$(NAME).key"; \
	    openssl genrsa -out $(SSL_DIR)/$(NAME).key 4096; \
	else \
	    echo "CA key $(SSL_DIR)/$(NAME).key already exists, skipping generation."; \
	fi

generate_ca_cert: generate_ca_key
	@if [ ! -f "$(SSL_DIR)/$(NAME)" ] || [ "$(force_ca)" = "yes" ]; then \
	    echo "Generating CA certificate: $(SSL_DIR)/$(NAME).pem"; \
		RANDOM_SUBJECT=$$(python3 generate_subject.py | tr -d '\n'); \
	    echo "Generating CSR with random subject: $$RANDOM_SUBJECT"; \
	    openssl req -x509 -new -nodes -key $(SSL_DIR)/$(NAME).key -sha256 -days 1825 -out $(SSL_DIR)/$(NAME).pem -subj "$$RANDOM_SUBJECT"; \
	else \
	    echo "CA certificate $(SSL_DIR)/$(NAME).pem already exists, skipping generation."; \
	fi

generate_intermediate_ca: generate_ca_key generate_intermediate_ca_cert ## Generate an Intermediate CA certificate

generate_intermediate_ca_cert: generate_ca_key
	@if [ ! -f "$(SSL_DIR)/$(NAME).pem" ] || [ "$(force_ca)" = "yes" ]; then \
	    echo "Generating Intermediate CA certificate: $(SSL_DIR)/$(NAME).pem"; \
		RANDOM_SUBJECT=$$(python3 generate_subject.py | tr -d '\n'); \
	    openssl req -new -key $(SSL_DIR)/$(NAME).key -out $(SSL_DIR)/$(NAME).csr -subj "$$RANDOM_SUBJECT"; \
	    openssl x509 -req -in $(SSL_DIR)/$(NAME).csr -CA $(SSL_ROOT)/$(ROOT).pem -CAkey $(SSL_ROOT)/$(ROOT).key -CAcreateserial \
	    -out $(SSL_DIR)/$(NAME).pem -days 1825 -sha256 -extensions v3_ca -extfile $(OPENSSL_CNF); \
	else \
	    echo "Intermediate CA certificate $(SSL_DIR)/$(NAME).pem already exists, skipping generation."; \
	fi


# Create SSL directory if it does not exist
create_ssl_dir:
	@if [ ! -d "$(SSL_DIR)" ]; then \
	    mkdir -p $(SSL_DIR); \
	    echo "Created directory: $(SSL_DIR)"; \
	fi

# Clean targets
clean: ## Clean generated certificate files for $(NAME)
	rm -fr $(SSL_DIR)/

clean-all: clean ## Clean all generated files and directories
	rm -fr $(SSL_BASE_DIR)