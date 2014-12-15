#Better Tag Application Report

Infusionsoft is a great product, however some of its reporting needs the occasional hand.  This 
is an implementation of the Tag Application Report which allows you to search by both date range
and tag.  

After you complete a search you can then apply a new, unique tag to the results so that you can find
them again in the application. 

This product is provided without warranty or guarantee. If you would like to see the most current example
you may see it at [crackbrain](http://crackbra.in)

Thanks!!


#Things to do:

- [x] Add a tag overview that displays all tags and how many contacts have each tag.    
- [ ] Clean up duplicate functionality in the application  
- [ ] Set up functionality that you can download parts of your application to a sql database  
- [ ] Set up a test order creation process  
    - [x] Created initial test process to prove that it is a doable thing.
- [ ] Create better Import functionality:    
    - [ ] Application accepts .csv file  
    - [ ] Gets all headers from csv file  
    - [ ] maps headers to correct fields  
    - [ ] for each line if the line has an Infusionsoft ID: update the correct contact record  
    - [ ] for each line if the line has an email address that is already in the system, update the correct record  
    - [ ] for each line if the line does not have a matching record, create a new record.   
- [ ] Better update with CC:  
    - [ ] ability to update contact records and add CC data to the record  
- [ ] Update server that it will get all custom fields
- [x] Set btar so that it will sort by the date that the tag was applied
