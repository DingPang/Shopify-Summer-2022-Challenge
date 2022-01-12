# Shopify-Summer-2022-Challenge

<!-- ABOUT THE PROJECT -->
## About The Project
Author: Ding Pang

Email: dp3129@columbia.edu

LinkedIn: https://www.linkedin.com/in/ding-pang/

Implemented Tasks:
* Basic CRUD Functionality.
    * Create inventory items [x]
    * Edit Them [x]
    * Delete Them [x]
    * View a list of them [x]
* Push a button export data to a CSV [x]


## Technologies
* Python3
* Flask
* SQLAlchemy
* PostgresSQL

## Supplements in this project
* schema.sql
    * A general schema to my psql database
* seed.sql
    * Fake data that can be used to seed the database
* ER.png
    * A database ER/Schema Diagram of my database
* Demovideo 1
    * A demo video of this application (no voiceover), only simple interactions. In unfortunate cases, this will demonstrate the application in action.
* Demovideo 2 (iBC)
    * A demo vidoe of a previous ecommerce site project (iBC) that I built for a class.

## Getting Started

This are two ways to interact with this project:
* Donwload it, and run it on a local machine
* Use my version, which is running on a google cloud machine.

I do suggest looking at my code, but use my version to view it.

WHY?

Because my seeded psql database is running on google cloud, it is tideous to set up the database on a local machine from scratch.

## My version (Easier)
Due to obvious security reasons, I cannot include my database url directly in this repo. However, when this application is submitted, I should have included that url in every possible text field (i.e "message to the hiring manager"). It should be in the form:
  ```py
  DATABASEURI = "postgresql://username:password@host/database"
  ```
Please include this line of python code in DBHelpers.py.

1. To make this process even smoother, you can try:
http://35.190.177.235:8111/.
this is a virtual machine running the same exact program. If it is not working, it is probably because I stopped the VM, since it is financially expensive to run this program without knowing when my application will be reviewed (feel free to send me an email to let me start it).
2. Same for my online psql database.


## On a Local Machine (Hard...)
1. Ensure python (with pip3) is downloaded (>3.7)

2. Clone this repo, and cd into it

3. Run following command in terminal shell (or just pip)
  ```sh
  pip3 install -r requirements.txt
  ```

4. Create a psql databse on your local machine

    * Use schema.sql, and seed.sql to seed the database

    * Add the correct databaseurl in below form into DBHelpers.py
      ```py
      DATABASEURI = "postgresql://username:password@host/database"
      ```
5. Instead of 4, you can use the url I provided in application.

6. Run it with
  ```sh
  python3 server.py
  ```

## Possible Q&A
* In DBHelpers.py, why did I have so many "Hard-coded" strings?
    * I am aware of SQL injection hacks, this is my own way of preventing it.

* Why did I pick the option of "export to csv"?
    * This is something that I haven't done, so I want to play with it. Some of other options, like "generate a report on inventory levels over time" and "Ability to create shipments and assign inventory to the shipment", I have done that in other projects like "iBC" (demo video 2).

* Future expansion? Scalability?
    * I try to make my database very simple to provide the highest flexibility. For example, I did not use advanced sql (triggers, etc.). I can certainly improve it just like demo video 2.

* Why so many try except?
    * It is not the most efficient way, but it hides many error handling troubles.






