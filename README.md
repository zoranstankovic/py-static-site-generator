# py-static-site-generator

A lightweight static site generator implemented in Python that allows you to programmatically generate HTML content.

## Overview

This project provides a simple way to generate static websites using Python. It focuses on providing basic HTML generation capabilities with a clean, programmatic approach.

## Features

- HTML block generation functionality
- TextNode component system with unit tests

## Project Structure

```
py-static-site-generator/
├── src/                # Main source code
│   └── ...            # Python implementation files
├── test.sh            # Test execution script
├── main.sh            # Main execution script
└── .gitignore         # Git ignore configurations
```

## Requirements

- Python 3.x

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/zoranstankovic/py-static-site-generator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd py-static-site-generator
   ```

3. Run the main script:
   ```bash
   ./main.sh
   ```

## Testing

To run the unit tests:

```bash
./test.sh
```

The test suite includes coverage for TextNode components and HTML block functionality.

## Development Status

This project is in early development. Current implementation includes:
- Basic HTML block generation
- TextNode component system
- Unit testing framework

## Contributing

Feel free to fork the repository and submit pull requests. As this is an early-stage project, all contributions are welcome.

## Author

[Zoran Stankovic](https://github.com/zoranstankovic)