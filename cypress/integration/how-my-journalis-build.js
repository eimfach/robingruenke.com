describe('The Home Page', function() {
  it('successfully loads', function() {
    cy.visit('/journal/blogging/tools/how-my-journal-is-build.html')

    cy.get('#pagetitle').should('contain', 'How my Journal is build')
  })
})