# Database

## User

employees

- id
- username
- Account
- Password

# Item

- id, auto increment
- BO
- X
- LPN
- title
- images: image1, ... image10
- image from: web / self
- status
- status note
- class

## Class

item class

- id
- ~~class level~~
- class name (including other class)

## Size

- id
- class
- size number

# Android

## Login Page

- Account: from database user table, add manully
- Password: from database user table, add manully

# Main Page

- Scanner
  1. Scan BO / X code
  2. Create url
  3. Check Amazon url, Home depot url, Walmart url exit or not
     - Exit
       - Input url automatically
       - Click Grab
       - Grab information from the web
     - Not Exit
       - Exit scanner and show the input box
       - Input url
       - Click Start
     - **Do we have picture that not on the Internet? How do we deal with it?**
- Grabbed Information
  - Case number: required, input manually, keep the same for one time login
  - Title: required, from web
  - Picture: required, from web, get first three pics. Add more by taking photo, **mostly taking 7 photos**
  - Status: required, selector(new, used), if used, add notes
  - Class: required, grab from web, if null, show selector
  - Size: only for shoes, clothes class
  - Price: required, grab from web, if price is like 30 - 40, use the highest value
  - Color: options 