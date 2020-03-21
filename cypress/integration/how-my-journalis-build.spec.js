describe('Page Title', function() {
  it('successfully loads', function() {
    
    cy.visit('/journal/blogging/tools/how-my-journal-is-build.html')

    cy.get('#pagetitle').should('contain', 'How my Journal is build')

    cy.get('#journal-topic-author').as('topic-author')
    cy.get('@topic-author').contains('Journal Topic of Robin Gruenke')

    cy.get('@topic-author')
      .then(function($el) {
        expect($el.find('a:only-child').first().attr('href')).to.equal('https://www.robingruenke.com')
      })

  })
})