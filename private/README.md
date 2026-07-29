# Private Canvas Sources

This directory contains the source text used for the main Canvas course page, the individual lab pages, and the dedicated group-allocation schedule page.

## Contents

- `organization.md`: main course and organization page
- `lab1.md`: Lab 1 introduction page
- `lab2.md`: Lab 2 introduction page
- `lab3.md`: Lab 3 introduction page
- `group_allocation_schedule.md`: dedicated Canvas page for the group-allocation schedule and deadlines
- `Makefile`: converts the Markdown sources into Canvas-ready HTML fragments
- `compiled/`: generated HTML fragments; these files are ignored by Git

The Markdown files are the source of truth. Do not edit files under `compiled/`, because they are overwritten when the sources are compiled again.

## Requirements

Install [Pandoc](https://pandoc.org/).

On macOS with Homebrew:

```sh
brew install pandoc
```

On Ubuntu:

```sh
sudo apt update
sudo apt install pandoc
```

Verify the installation:

```sh
pandoc --version
```

## Compile All Pages

From the repository root, run:

```sh
make -C private
```

This creates:

```text
private/compiled/organization.html
private/compiled/lab1.html
private/compiled/lab2.html
private/compiled/lab3.html
private/compiled/group_allocation_schedule.html
```

Only sources that have changed since the previous compilation are rebuilt.

To compile one page, run, for example:

```sh
make -C private compiled/lab3.html
```

The generated files are HTML fragments rather than standalone web pages. They intentionally omit `<html>`, `<head>`, and `<body>` because Canvas supplies that surrounding structure.

## Copy a Page into Canvas

1. Open the corresponding page in Canvas and select **Edit**.
2. Switch the Rich Content Editor to **HTML view**.
3. Switch to the **raw HTML editor**.
4. Replace the existing page content with the contents of the corresponding file under `compiled/`.
5. Switch back to the visual editor to preview the page, then save it.

Canvas may remove unsupported HTML when the page is saved. Keep the Markdown sources limited to ordinary headings, paragraphs, lists, links, emphasis, and code blocks.

## Markdown Conventions

- Start page content with a level-two heading (`##`). Canvas supplies the page title separately, so `## Course PM` becomes `<h2>Course PM</h2>`.
- Use level-three headings (`###`) for page sections.
- Use Markdown lists instead of manually inserting bullets or numbers.
- Format commands, paths, filenames, and function names with backticks.
- Write links as `[visible text](URL)`.
- Use explicit URLs for Canvas pages and uploaded files. Labels such as `Download file` cannot be converted into working Canvas links without their destination URLs.
