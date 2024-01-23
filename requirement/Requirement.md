# Database

## User

employees

- id
- username
- Account
- Password

# Item

- id, auto increment
- user_id: employee id
- time: create time
- last_modify_time: time
- BO
- X
- LPN
- Code
- case_number
- item_number
- title
- images: image1, ... image10
- image from: web / self
- status
- status note
- class
- size
- color
- price
- bid_price

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
  2. Search Database, whether exist the code
  3. if not
     1. Create url
     2. Check Amazon url, Home depot url, Walmart url exit or not
       1. Exit
          1. Input url automatically
          2. Click Grab
          3. Grab information from the web
       2. Not Exit
          1. Exit scanner and show the input box
          2. Input url
          3. Click Start
       3. **Do we have picture that not on the Internet? How do we deal with it?**
  4. if has
     1. grab information from database
- Grabbed Information
  - Case number: required, input manually, keep the same for one time login
  - item_number: options, if input, check exist, if not input, create by user id range
    - from 10000 to 99999
    - recursive it
  - Title: required, from web
  - Picture: required, from web, get first three pics. Add more by taking photo, **mostly taking 7 photos**
    - name as item id_1.jpg ...
  - Status: required, selector(new, used), if used, add notes
  - Class: required, grab from web, if null, show selector
  - Size: only for shoes, clothes class
  - Color: options, grab or not
  - Price: required, grab from web, if price is like 30 - 40, use the highest value