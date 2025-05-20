describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')
  })

  it('starting out on the landing screen', () => {
    // make sure the landing page contains a header with "login"
    cy.get('h1')
      .should('contain.text', 'Login')
  })

  it('login to the system with an existing account', () => {
    // detect a div which contains "Email Address", find the input and type (in a declarative way)
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)
    // alternative, imperative way of detecting that input field
    //cy.get('.inputwrapper #email')
    //    .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert that the user is now logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)
    
    const task_title = "Learn Cypress"; 
    const youtube_key = "U_gANjtv28g"; 

  cy.get(".inputwrapper #title").type(task_title);
  cy.get(".inputwrapper #url").type(youtube_key);
  cy.get("form").submit();

  // Assert that the task is added to the list
  cy.contains(task_title).should("exist");
  
  // Assert that the YouTube thumbnail is displayed
  cy.get(`img[src*="${youtube_key}"]`).should("exist");

  cy.get(`img[src*="${youtube_key}"]`).first().click();
  cy.get(".inline-form").find("input[type=submit]").click({force: true});

  cy.wait(1000);

  cy.get("li.todo-item").should("have.length", 1);
    
  });

  // it("To add a task with valid description", () => {
  //   cy.get('.container.popup.')
      
  // });

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})
