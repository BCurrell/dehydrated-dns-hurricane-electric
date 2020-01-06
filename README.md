# dehydrated-dns-hurricane-electric

Dehydrated hook for DNS verification on Hurricane Electric in Python.

Hurricane Electric does not currently provide an API for creating and removing DNS records. The closest thing they have is their dyn.dns.he.net service, which allows you to update existing dynamic DNS records.

This project has a very limited scope; it is going to create and remove ACME TXT records, however there is a future plan to spin this out in to a fully featured Python library.

## Requirements

- dehydrated
- python (3.6 or higher)
- pipenv

For the purposes of this "documentation", I'm assuming you already have these installed, or know how to install them.

## Usage

`# TODO: This`

## To-Do

- [x] Create shell project with basic dehydrated hook functionality
- [x] Authenticate with Hurricane Electric
- [x] List zones
- [x] List records
- [ ] Add DNS record
- [ ] Remove DNS record
