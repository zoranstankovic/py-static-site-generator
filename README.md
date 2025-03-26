# py-static-site-generator

A production-ready static site generator implemented in Python that enables programmatic HTML content generation with a
clean and efficient approach.

## Overview

This project provides a robust way to generate static websites using Python.
It delivers a complete solution for HTML generation with a focus on simplicity,
performance, and maintainability.

This project was developed as part of the [Boot.dev](https://boot.dev) programming learning platform.

## Features

- Convert Markdown to HTML with support for common markdown elements
- Customizable HTML templating system
- Simple and intuitive project structure
- Performance optimized for quick builds
- Minimal dependencies

## Project Structure

```
py-static-site-generator/
|__ content/            # Main Markdown content files
|__ docs/               # Generated HTML files from Markdown files
├── src/                # Main source code
│   └── ...             # Python implementation files
|__ static/             # Static files (images, CSS files)
├── test.sh             # Test execution script
├── main.sh             # Main execution script
|__ build.sh            # Main build script
|__ template.html       # Template file for HTML generation
└── .gitignore          # Git ignore configurations
```

## Requirements

* Python 3.x

## Installation

Clone the repository:

```bash
git clone https://github.com/zoranstankovic/py-static-site-generator.git
cd py-static-site-generator
```

## Usage

### Quick Start

1. Replace static files with your custom CSS and images
2. Update the existing `template.html` file to match your design
3. Create markdown files and place them in the content folder
4. Run the build script:

```bash
./main.sh
```

### Supported Markdown Features

#### Block Elements

- Headings (`#` to `######`)
- Code blocks (``` ```)
- Quote blocks (`>`)
- Unordered lists (`-`)
- Ordered lists (`1.`, `2.`, etc.)
- Paragraphs

#### Inline Elements

- Plain text
- Bold text (`**bold**`)
- Italic text (`_italic_`)
- Inline code (`` `code` ``)
- Images (`![alt text](URL)`)
- Links (`[link name](URL)`)

### Customization

To customize the generator for your specific needs:

1. Edit the `template.html` file to change the overall site structure
2. Organize your markdown files in the `content/` directory based on your desired site structure
3. Customize CSS in the `static/` directory

## Testing

The project includes comprehensive test coverage:

```bash
./test.sh
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Author

[Zoran Stankovic](https://github.com/zoranstankovic)

## Acknowledgments

- [Boot.dev](https://boot.dev) for the project guidance and learning resources