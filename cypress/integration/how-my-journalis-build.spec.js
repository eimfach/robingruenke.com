const helpers = require('../helpers')

describe('Page Title', function() {
  it('successfully loads', function() {
    
    cy.visit('/journal/blogging/tools/how-my-journal-is-build.html')

  })

  it('has a valid pagetitle', function () {
    cy.visit('/journal/blogging/tools/how-my-journal-is-build.html')

    cy.get('#pagetitle').should('contain', 'How my Journal is build')

    cy.get('#journal-topic-author').as('topic-author')
    cy.get('@topic-author').contains('Journal Topic of Robin Gruenke')

    cy.get('@topic-author')
      .then(function($el) {
        expect($el.find('a:only-child').first().attr('href')).to.equal('https://www.robingruenke.com')
      })
  })

  it('has golden ratio on main image', function () {
    cy.visit('/journal/blogging/tools/how-my-journal-is-build.html')

    cy.get('.main-image')
    .then(function ($el) {
      const introTextWidth = $el.outerWidth()
      const introTextHeight = $el.outerHeight();
      expect(introTextHeight).to.be.equal(helpers.goldenratio(introTextWidth, introTextHeight))
    })


  })
})