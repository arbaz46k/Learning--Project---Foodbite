# Learning--Project---Foodbite
Video link of the project :https://youtu.be/3DgHEtER8DU
## This is my submission for Internship Web development with python and Javascript Learning Project
## Introduction
I have named this project FoodBite. This is a simple Web application for ordering food online. User has a choice of selecting from multiple restaurants and order whatever they like. This project is build using Django as a backend framework bootstrap for styling and a little Javascript. This web app is mobile responsive
## Project Structure

* food_delivery - main application directory
    * static/food_delivery - contains all static content
         * images- contains images png/svg used in this project.
         * style.css- contains the styling of the project.
         * index.js -contains Javascript used in this web app. Javascript is used to just create a toggle menubar/sidebar.
     * templates/food_delivery - Contains all the templates used in this web app
         * index.html - This is the main page visible to user after login. It lists all the restaurants which are registered in this web app
         * dishes.html - This page list all the dishes of the restaurant the user has clicked on
         * cart.html - It shows all the food items in cart with the total bill and functionalities to confirm order
         * recent_orders.html - This page list all the past order user has made and the status of the order
         * partner_index.html - This page list all the orders the user has made to the restaurant and all the completed orders which restaurant has delivered. It also has a button to add new dishes to the restaurant
         * add_item.html - This page is for the restaurant partners to add new dishes to their restaurant.
         * login.html/partner_login.html - These are the templates for logining user/restaurant in
         * register.html/partner_register.html - These are the templates for registering new user/restaurant.
         * layout.html - This template consists of the layout of the web application. All the templates extends it.
     * templatetags/
         * cart.py - Contains template filters for cart
     * model.py - Contains 4 models.
         * User - User model extends standard user model and some other fields to distinguish normal user from restaurant.
         * Dishes - Models for dishes of restaurants.
         * Order - Model for Order store order details.
         * Ordered_dishes - Model to store dishes and quantity with a foreign key pointing to Order model.
     * urls.py - Contains all the urls.
     * views.py - All the application views are contained in it.
     * media/images - Database for images.
         * dishes - contains images of dishes.
         * restaurant - contains images of restaurant.
## Functionalities
* Order

   * User can order from variety of restaurants by clicking on them and choosing from vareity of dishes.
   * User can click on Add to Cart button to add dish to cart and + button to increase its quantity and - button to decrease its quantity.
* Cart

   * User can check the total bill of his/her order and confirm the order by clicking on the checkout button and filling the required information like address and contact no.
* Become a partner

   * One can register their restaurant on our website to list their restaurant on or website and get orders
   * Restaurant partners can add dishes by clicking on the Add item button after logging in.
* Order listing

   * If the customer has ordered something the corresponding restuarant will the order details in their panel.
   * Once the order is completed the restaurant partner can click on the delivered button to shift the order in the delivered section.
* Login and Register

## Justification
This project is distinct from all previous projects so far.Why?

* Completely Mobile responsive
* Uses Django model forms
* Saving Images(saves the location of the image ) in Database.
* User can order from multiple restaurant at the same time.
* Restaurants can add as many dishes as they want.
* User has the history of his/her orders in Recent orders.
