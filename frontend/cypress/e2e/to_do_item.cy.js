describe("login and manage tasks and todos", () => {
  let uid;
  let name;
  let email;
  let task_title = "Learning Cypress";
  let youtube_key = "69SFwgWHUig"; // YouTube Video ID
  let todoDescription = "Watch video";

  before(() => {
    cy.fixture("user.json").then((user) => {
      cy.request({
        method: "POST",
        url: "http://localhost:5000/users/create",
        form: true,
        body: user,
      }).then((response) => {
        uid = response.body._id.$oid;
        name = `${user.firstName} ${user.lastName}`;
        email = user.email;
      });
    });
  });

  beforeEach(() => {
    cy.visit("http://localhost:3000");
    cy.contains("div", "Email Address").find("input[type=text]").type(email);
    cy.get("form").submit();
    cy.get("h1").should("contain.text", "Your tasks, " + name);
  });

  it("creates a task", () => {
    cy.get(".container-element").then(($items) => {
      const taskCount = $items.length;
      const newTaskTitle = `${task_title} ${taskCount}`;

      cy.get("#title").type(newTaskTitle);
      cy.get("#url").type(youtube_key);
      cy.get("form").submit();

      cy.contains(newTaskTitle).should("exist");
      cy.get(`img[src*="${youtube_key}"]`).should("exist").eq(taskCount-1).click();
    });
  });

  it("Add a new todo item", () => {
    cy.get(`img[src*="${youtube_key}"]`).click();

    cy.get("ul.todo-list li.todo-item").then(($items) => {
      const todoCount = $items.length;
      const newTodo = `Test Todo ${todoCount}`;

      cy.get(".inline-form input[type=text]").type(newTodo);
      cy.get(".inline-form input[type=submit]").click();

      cy.get("ul.todo-list").contains(newTodo).should("exist");
      cy.get("ul.todo-list li.todo-item").should("have.length", todoCount + 1);
    });
  });

  it("does not allow empty todo description (this should fail)", () => {
    cy.get(`img[src*="${youtube_key}"]`).click();

    cy.get("ul.todo-list li.todo-item").then(($items) => {
      const initialCount = $items.length;
      cy.get(".inline-form input[type=text]").clear();
      cy.get(".inline-form input[type=submit]").click();

      cy.get("ul.todo-list li.todo-item").should("have.length", initialCount + 1);
    });
  });


  it("checks a todo", () => {
    cy.get("div").find(`img[src*="${youtube_key}"]`).click();

    cy.contains("ul.todo-list li.todo-item", todoDescription).within(() => {
      cy.get(".checker").click().should("exist");
    });
  });

  it("deletes a todo", () => {
    cy.get("div").find(`img[src*="${youtube_key}"]`).click();

    cy.get('li.todo-item').contains(todoDescription)
        .parents("li.todo-item")
        .find("span.remover").click();
    

    cy.contains("ul.todo-list li.todo-item", todoDescription).should("not.exist");
  });

   after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
});
