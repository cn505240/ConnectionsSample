# Software Specification - Degrees of Separation Endpoint

Written by Conor McLaughlin

Created on July 25, 2020

## Background

There has been a feature request for the Connections API to add an endpoint that will allow a user to retrieve all People connected to a given Person with less than or equal to a given number of degrees of separation.
For example, a friend of a friend (or any two other ConnectionTypes) of the given Person would have a degree of separation of 2. For a better understanding of the concept, see https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon

## Endpoint Specification

This feature should be completed by adding a new REST endpoint using a **GET** request to the following route:

**/people/<person_id>/connections?degrees_of_separation=<degrees_of_separation>&limit=<limit>&offset=<offset>**

where **person_id** is an integer path variable representing the database row ID of a specific person, and **degrees_of_separation** (>= 0) is an integer query string variable.
The **limit** and **offset** query string variables are integer values that will be used to paginate the results to avoid returning too much data at one time.

If the provided **person_id** exists, the endpoint should return a list of all People within **degrees_of_separation** of the given Person, with all fields of each Person object included (verify with Product Owner).

## Technical Details

* The appropriate number of People to return will likely increase exponentially with the value of **degrees_of_separation**. Assuming a significant number of People in our database,
the number of people to return could become a prohibitively large amount of data.

    * I suggest that we impose a maximum value on the **degrees_of_separation** variable that will avoid returning
    the entire database. What exactly that value should be will need to be found through some experimentation and cleared with the Product Owner (see the Questions for Product Owner section).
    
* Finding the correct set of People to return is a non-trivial problem. I suggest employing a depth limited search (https://www.educba.com/depth-limited-search/), which is a variant of a depth first search.
  Because mutual connections are nearly certain within a Degrees of Separation network of any size, your algorithm will need to account for and avoid traversing loops within the network of Connections.
  
## Questions for Product Owner

* Are the anticipated use cases for this feature limited enough that we can assume certain pagination parameters, and thus avoid supporting those in the query string?

* Is it acceptable to impose a maximum value on the requested **degrees_of_separation**? If so, do the use cases for this feature provide any guidance on what an acceptable maximum could be?

* Which fields of the Person objects do we need to include in our returned data?
