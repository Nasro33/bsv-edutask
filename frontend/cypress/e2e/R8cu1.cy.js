// import { wait } from "@testing-library/react";

// describe("Loggin, create task Empty ToDo", () => {
//   // define variables that we need on multiple occasions
//   let uid; // user id
//   let name; // name of the user (firstName + ' ' + lastName)
//   let email; // email of the user

//   before(function () {
//     // create a fabricated user from a fixture
//     cy.fixture("user.json").then((user) => {
//       cy.request({
//         method: "POST",
//         url: "http://localhost:5000/users/create",
//         form: true,
//         body: user,
//       }).then((response) => {
//         uid = response.body._id.$oid;
//         name = user.firstName + " " + user.lastName;
//         email = user.email;
//       });
//     });
//   });

//   beforeEach(function () {
//     // enter the main main page
//     cy.visit("http://localhost:3000");
//   });

//   it("login to the system with an existing account", () => {
//     // detect a div which contains "Email Address", find the input and type (in a declarative way)
//     cy.contains("div", "Email Address").find("input[type=text]").type(email);
//     // alternative, imperative way of detecting that input field
//     //cy.get('.inputwrapper #email')
//     //    .type(email)
//     // submit the form on this page
//     cy.get("form").submit();
//     // assert that the user is now logged in
//     cy.get("h1").should("contain.text", "Your tasks, " + name);

//     const taskTitle = "Karma Task Title";
//     const youtubeKey = "yk3prd8GER4"; // Use a valid video ID

//     cy.get(".inputwrapper #title").type(taskTitle);
//     cy.get(".inputwrapper #url").type(youtubeKey);
//     cy.get("form").submit();

//     // Verify that the task appears in the UI
//     cy.contains(taskTitle).should("exist");

//     // Verify that the thumbnail is rendered
//     cy.get(`img[src*="${youtubeKey}"]`).should("exist");

//     cy.get(`img[src*="${youtubeKey}"]`).click(); //Open detail view

//     cy.get(".inline-form").find("input[type=submit]").click();

//     // cy.get(".todo-list").contains(emptyTodo).should("exist");
//     cy.wait(1000); // Wait for the UI to updatekkk

//     cy.get("li.todo-item").should("have.length", 1); // Ensure only one todo is present
//   });

//   after(function () {
//     // clean up by deleting the user from the database
//     cy.request({
//       method: "DELETE",
//       url: `http://localhost:5000/users/${uid}`,
//     }).then((response) => {
//       cy.log(response.body);
//     });
//   });
// });