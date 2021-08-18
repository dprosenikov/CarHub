# CarHub - Django Template Project

## About the project
Templates project that serves to create and store cars. There is a login/register functionality for users and full CRUD operation when logged in.

## Django Template
<b>Must haves:</b><br/>
    - The application must have at least <b>10 endpoints</b><br/>
    - The application must have <b>login/register functionality</b><br/>
    - The application must have <b>public part</b><br/>
    - The application must have <b>private</b> part<br/>
    - The application must have <b>admin</b> part<br/>
    - Unauthenticated users (<b>public part</b>) have only 'get' permissions e.g., landing page, details, about page<br/>
    - Authenticated users (<b>private part</b>) have full CRUD for all their created content<br/>
    - Admins have full CRUD functionalities<br/>
    - Form validations<br/>
    - Implement <b>Error Handling</b> and <b>Data Validations</b><br/>
    - Use <b>PostgreSQL</b> as a database.<br/>
    - Write <b>tests</b> for at least 60% coverage on your business logic<br/>
    - Templates  – one and the same template could be re-used/used multiple times<br/>

<b>Bonuses:</b><br/>
    - Responsive web design<br/> 
    - Class-based views<br/>
    - Extended Django user<br/>


## Content

 <b>1. Profiles App</b>
- <b>Login/Register functionality using 'email' for authentication</b> - when user is registered, he/she is automatically logged in
- <b>CarHubUser</b> - mirrors the default User model in order to kepp the User 'clean'. Profile which relates to CarHubUser and stores the user's profile image.
- <b>Profile details</b> - where every user has the ability to update their profile picture and delete their profile. Upon deletion of the profile, the user is logged out.
- <b>List profiles</b> - superusers have the option to see all registered users and delete any of them. 
- <b>Tests</b> - check if user is successfully registered/deleted and if superusers can get list of all users. 


 <b>2. Cars App</b>

- <b>Models</b> - Car, Comment and Like models. All of them are related to the user that created them. The Car model have custom validation for the year to be no later than the current year and no earlier than the first manufactured car. It also has a predefined list of brands to choose from. All car listings throughout the app are sorted by price.
- <b>Views</b>:<br/>
  - <u>List all cars</u> - accessible by everyone. Pagination in place to show maximum 4 cars on page.
  - <u>My cars</u> - accessible by authenticated users and showing only the cars that this user created. Pagination in place to show maximum 4 cars on page.
  - <u>Search</u> - accessible by everyone. Search by brand name(case-sensitive).
  - <u>Create/Edit/Delete car</u> - create is available for authenticated users where edit and delete are available only for the owner of the car.
  - <u>Car details</u> - accessible by everyone. Option for <i>Like</i> - only for authenticated user and NOT owner of the car(because liking your own posts is not cool). Option for <i>Comment</i> - available for authenticated users.  
- <b>Tests</b> - Car year validation, Car list view(with and without cars), Car details(the 4 variations of owner and liked), Like(add/remove likes), Comment is added correctly, Create/Edit/Delete car, Search(match found and not found).
